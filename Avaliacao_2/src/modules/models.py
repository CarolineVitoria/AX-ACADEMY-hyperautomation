"""Estruturas de dados compartilhadas entre os módulos da automação."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

#: Nomes lógicos dos três anexos obrigatórios (RN02) e o padrão de nome de
#: arquivo esperado para cada um (com {cpf} substituído pelo CPF do cliente).
ANEXOS_OBRIGATORIOS = {
    "ficha_cadastro": "Ficha_Cadastro_{cpf}.pdf",
    "documento_identificacao": "Documento_Foto_{cpf}.pdf",
    "comprovante_residencia": "Comprovante_Residencia_{cpf}.pdf",
}

STATUS_APROVADO = "APROVADO"
STATUS_PENDENTE = "PENDENTE"


@dataclass
class Solicitacao:
    """Uma solicitação de cadastro recebida por e-mail."""

    remetente: str
    assunto: str
    cpf_assunto: str
    id_mensagem: str
    caminhos_anexos: dict[str, Path] = field(default_factory=dict)


@dataclass
class ResultadoValidacao:
    """Resultado da validação de uma solicitação (RN01 a RN06)."""

    status: str
    pendencias: list[str] = field(default_factory=list)
    dados_cliente: dict | None = None

    @property
    def motivo(self) -> str | None:
        return "; ".join(self.pendencias) if self.pendencias else None

    @property
    def aprovado(self) -> bool:
        return self.status == STATUS_APROVADO
