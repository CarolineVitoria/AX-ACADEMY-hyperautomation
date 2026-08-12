"""Configuração compartilhada dos testes: garante que os módulos em src/
sejam importáveis (ex.: `from modules.cpf_validator import ...`) e fornece
fixtures reutilizáveis, como a geração de PDFs de exemplo para os testes de
extração de documentos.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
SRC_DIR = RAIZ_PROJETO / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pytest
from reportlab.pdfgen import canvas


@pytest.fixture
def gerar_pdf(tmp_path):
    """Gera um PDF simples com uma linha de texto por item de `linhas`."""

    def _gerar_pdf(nome_arquivo: str, linhas: list[str]) -> Path:
        caminho = tmp_path / nome_arquivo
        pdf = canvas.Canvas(str(caminho))
        posicao_y = 800
        for linha in linhas:
            pdf.drawString(50, posicao_y, linha)
            posicao_y -= 20
        pdf.save()
        return caminho

    return _gerar_pdf
