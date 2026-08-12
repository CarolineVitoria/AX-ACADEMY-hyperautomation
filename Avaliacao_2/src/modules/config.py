"""Configurações e caminhos centrais da automação.

Concentra a leitura de variáveis de ambiente (.env) e a definição dos
caminhos usados pelos demais módulos, evitando strings de caminho
espalhadas pelo código.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Raiz do projeto: .../Avaliacao_2
RAIZ_PROJETO = Path(__file__).resolve().parents[2]

load_dotenv(RAIZ_PROJETO / ".env")


class Config:
    """Configurações de execução carregadas do ambiente (.env)."""

    EMAIL_PROVEDOR: str = os.getenv("EMAIL_PROVEDOR", "gmail").lower()
    PLAYWRIGHT_HEADLESS: bool = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"

    # Padrão do assunto do e-mail de solicitação (RN01).
    # Ex.: "Cadastro Portal Fake - 123.456.789-09"
    PADRAO_ASSUNTO_PREFIXO: str = "Cadastro Portal Fake -"

    # Caminhos do projeto
    PROJETO_AUTOMACAO_DIR = RAIZ_PROJETO / "Projeto_Automacao"
    DOCUMENTOS_OK_DIR = PROJETO_AUTOMACAO_DIR / "Documentos_OK"
    DOCUMENTOS_PENDENTES_DIR = PROJETO_AUTOMACAO_DIR / "Documentos_Pendentes"
    PLANILHA_MESTRA_PATH = PROJETO_AUTOMACAO_DIR / "Planilha_Mestra.xlsx"

    DOWNLOADS_TEMP_DIR = RAIZ_PROJETO / "src" / "arquivos_auxiliares" / "downloads_temp"
    LOGS_DIR = RAIZ_PROJETO / "logs"

    # Sessão autenticada (cookies) salva pelo login manual único (ver
    # arquivos_auxiliares/login_manual.py) e reaproveitada pela automação,
    # evitando o login automatizado repetido que o Google/Microsoft bloqueiam
    # por suspeita de automação ("Este navegador ou app pode não ser seguro").
    AUTH_STATE_PATH = RAIZ_PROJETO / "src" / "arquivos_auxiliares" / "auth_state.json"

    @classmethod
    def garantir_diretorios(cls) -> None:
        """Cria os diretórios usados pela automação, caso não existam."""
        for diretorio in (
            cls.DOCUMENTOS_OK_DIR,
            cls.DOCUMENTOS_PENDENTES_DIR,
            cls.DOWNLOADS_TEMP_DIR,
            cls.LOGS_DIR,
        ):
            diretorio.mkdir(parents=True, exist_ok=True)
