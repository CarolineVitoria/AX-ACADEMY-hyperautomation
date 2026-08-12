"""Organização dos arquivos recebidos nas pastas Documentos_OK/ ou
Documentos_Pendentes/, conforme RN05/RN06.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from .config import Config
from .models import STATUS_APROVADO, Solicitacao


def organizar_arquivos(
    solicitacao: Solicitacao, status: str, logger: logging.Logger | None = None
) -> Path:
    """Move os anexos baixados para a pasta correspondente ao status do cadastro.

    RN05: cadastro APROVADO -> Documentos_OK/<cpf>/
    RN06: cadastro PENDENTE -> Documentos_Pendentes/<cpf>/

    Retorna o diretório de destino. Anexos que não chegaram a ser baixados
    (ex.: anexo ausente na solicitação original) são simplesmente ignorados.
    """
    logger = logger or logging.getLogger("portal_fake_automacao")

    pasta_base = (
        Config.DOCUMENTOS_OK_DIR if status == STATUS_APROVADO else Config.DOCUMENTOS_PENDENTES_DIR
    )
    pasta_destino = pasta_base / solicitacao.cpf_assunto
    pasta_destino.mkdir(parents=True, exist_ok=True)

    for chave, caminho_origem in solicitacao.caminhos_anexos.items():
        if not caminho_origem.exists():
            logger.warning(
                "Anexo '%s' não encontrado em disco durante a organização de arquivos", chave
            )
            continue

        caminho_destino = pasta_destino / caminho_origem.name
        shutil.move(str(caminho_origem), str(caminho_destino))
        logger.debug("Movido '%s' -> '%s'", caminho_origem, caminho_destino)

    logger.info("Arquivos da solicitação %s organizados em '%s'", solicitacao.cpf_assunto, pasta_destino)
    return pasta_destino
