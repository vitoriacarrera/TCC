"""Proteções da API (OWASP API Security Top 10, 2023).

- Limite de tamanho do corpo (API4: consumo irrestrito de recursos).
- Limite de requisições por cliente, em memória e sem gravar nada (API4 e API6: fluxo de contribuição).
- Cabeçalhos de segurança e `Cache-Control: no-store`, porque as respostas trazem dados financeiros (API8).
- Comprovante HMAC: a contribuição só é aceita com as mesmas respostas de uma simulação feita há pouco (API6),
  o que impede gravar contribuições inventadas sem passar pela simulação. O comprovante não é armazenado e não
  contém nada além de um resumo criptográfico das respostas e do prazo de validade (ADR-005).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from collections import OrderedDict, deque

from starlette.types import ASGIApp, Message, Receive, Scope, Send

LIMITE_CORPO_BYTES = 32 * 1024            # o maior pedido legítimo (média empresa, 52 respostas) tem cerca de 2 KB
VALIDADE_COMPROVANTE_S = 2 * 60 * 60      # 2 horas para decidir contribuir

# (máximo de requisições, janela em segundos) por rota
LIMITES = {
    "/simulacoes": (30, 60),
    "/questionario": (60, 60),
    "/contribuicoes": (5, 3600),
}
_MAX_CLIENTES = 10_000                    # memória limitada: os clientes mais antigos são esquecidos
INSTANCIAS: list[LimiteRequisicoes] = []  # para os testes zerarem as janelas


def _resposta_simples(status: int, corpo: dict, extra: list[tuple[bytes, bytes]] | None = None):
    dados = json.dumps(corpo, ensure_ascii=False).encode()
    cab = [(b"content-type", b"application/json"), (b"content-length", str(len(dados)).encode())] + (extra or [])

    async def enviar(send: Send) -> None:
        await send({"type": "http.response.start", "status": status, "headers": cab})
        await send({"type": "http.response.body", "body": dados})
    return enviar


class LimiteCorpo:
    """Recusa (413) corpos acima do limite, com ou sem Content-Length (corpo em partes)."""

    def __init__(self, app: ASGIApp, limite: int = LIMITE_CORPO_BYTES) -> None:
        self.app, self.limite = app, limite

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        declarado = dict(scope.get("headers", [])).get(b"content-length")
        if declarado is not None and (not declarado.isdigit() or int(declarado) > self.limite):
            return await _resposta_simples(413, {"detail": "pedido grande demais"})(send)
        recebido = 0

        async def receber() -> Message:
            nonlocal recebido
            msg = await receive()
            if msg["type"] == "http.request":
                recebido += len(msg.get("body", b""))
                if recebido > self.limite:
                    raise _CorpoGrande
            return msg

        try:
            await self.app(scope, receber, send)
        except _CorpoGrande:
            await _resposta_simples(413, {"detail": "pedido grande demais"})(send)


class _CorpoGrande(Exception):
    pass


class LimiteRequisicoes:
    """Janela deslizante por (rota, cliente). O endereço fica só na memória do processo, nunca em log ou disco."""

    def __init__(self, app: ASGIApp, limites: dict[str, tuple[int, int]] | None = None) -> None:
        self.app = app
        self.limites = LIMITES if limites is None else limites
        self.janelas: OrderedDict[tuple[str, str], deque[float]] = OrderedDict()
        INSTANCIAS.append(self)

    def _permitir(self, rota: str, cliente: str) -> int | None:
        """None se permitido; senão, segundos até liberar."""
        maximo, janela = self.limites[rota]
        agora = time.monotonic()
        chave = (rota, cliente)
        fila = self.janelas.pop(chave, deque())
        while fila and agora - fila[0] > janela:
            fila.popleft()
        self.janelas[chave] = fila
        while len(self.janelas) > _MAX_CLIENTES:
            self.janelas.popitem(last=False)
        if len(fila) >= maximo:
            return int(janela - (agora - fila[0])) + 1
        fila.append(agora)
        return None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        rota = scope.get("path", "")
        if scope["type"] == "http" and scope.get("method") == "POST" and rota in self.limites:
            cliente = (scope.get("client") or ("?", 0))[0]
            espera = self._permitir(rota, cliente)
            if espera is not None:
                return await _resposta_simples(
                    429, {"detail": "muitas tentativas seguidas; aguarde um pouco e tente de novo"},
                    [(b"retry-after", str(espera).encode())])(send)
        await self.app(scope, receive, send)


CABECALHOS = [
    (b"x-content-type-options", b"nosniff"),
    (b"cache-control", b"no-store"),
    (b"referrer-policy", b"no-referrer"),
    (b"x-frame-options", b"DENY"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
    (b"cross-origin-resource-policy", b"same-site"),
    (b"strict-transport-security", b"max-age=31536000; includeSubDomains"),
]
CSP_API = (b"content-security-policy", b"default-src 'none'; frame-ancestors 'none'")


class CabecalhosSeguranca:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        documentacao = scope.get("path", "").startswith(("/docs", "/redoc", "/openapi.json"))

        async def enviar(msg: Message) -> None:
            if msg["type"] == "http.response.start":
                cab = [(k, v) for k, v in msg.get("headers", []) if k.lower() != b"server"]
                cab += CABECALHOS + ([] if documentacao else [CSP_API])
                msg = {**msg, "headers": cab}
            await send(msg)

        await self.app(scope, receive, enviar)


# ------------------------------------------------------------------ comprovante da simulação (HMAC)
def _segredo() -> bytes:
    v = os.environ.get("RISKPME_SEGREDO")
    return v.encode() if v else _SEGREDO_PROCESSO


_SEGREDO_PROCESSO = secrets.token_bytes(32)     # sem RISKPME_SEGREDO: vale até o servidor reiniciar


def _mensagem(expira: int, setor: str, porte: int, respostas: dict[str, int | None]) -> bytes:
    return json.dumps([expira, setor, porte, respostas], sort_keys=True, separators=(",", ":")).encode()


def emitir_comprovante(setor: str, porte: int, respostas: dict[str, int | None], agora: float | None = None) -> str:
    expira = int((agora or time.time()) + VALIDADE_COMPROVANTE_S)
    mac = hmac.new(_segredo(), _mensagem(expira, setor, porte, respostas), hashlib.sha256).hexdigest()
    return f"{expira}.{mac}"


def comprovante_valido(comprovante: str, setor: str, porte: int, respostas: dict[str, int | None],
                       agora: float | None = None) -> bool:
    try:
        expira_txt, mac = comprovante.split(".", 1)
        expira = int(expira_txt)
    except ValueError:
        return False
    if expira < (agora or time.time()):
        return False
    esperado = hmac.new(_segredo(), _mensagem(expira, setor, porte, respostas), hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, mac)
