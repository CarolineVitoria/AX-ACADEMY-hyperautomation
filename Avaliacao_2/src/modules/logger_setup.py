"""Configuração centralizada de logging da automação.

Todo o processo registra em log as ações realizadas em cada solicitação
processada (PDD, seção 3 - Saídas: "Registro/log de execução do robô"),
tanto no console quanto em arquivo, para fins de auditoria e testes.
"""

from __future__ import annotations

import logging
from datetime import datetime

from .config import Config


def configurar_logger(nome: str = "portal_fake_automacao") -> logging.Logger:
    """Cria (ou reaproveita) o logger da automação com saída em console e arquivo."""
    logger = logging.getLogger(nome)

    if logger.handlers:
        # Já configurado (evita handlers duplicados em chamadas repetidas).
        return logger

    Config.garantir_diretorios()

    logger.setLevel(logging.DEBUG)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)

    nome_arquivo = datetime.now().strftime("execucao_%Y-%m-%d.log")
    arquivo_handler = logging.FileHandler(
        Config.LOGS_DIR / nome_arquivo, encoding="utf-8"
    )
    arquivo_handler.setLevel(logging.DEBUG)
    arquivo_handler.setFormatter(formato)

    logger.addHandler(console_handler)
    logger.addHandler(arquivo_handler)

    return logger
