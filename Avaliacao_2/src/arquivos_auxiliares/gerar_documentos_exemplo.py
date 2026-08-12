"""Utilitário auxiliar (não faz parte do fluxo da automação) para gerar os
3 PDFs de exemplo usados no teste manual descrito no README ("Envie um
e-mail de teste"): Ficha_Cadastro_CPF.pdf, Documento_Foto_CPF.pdf e
Comprovante_Residencia_CPF.pdf.

Uso:
    python src/arquivos_auxiliares/gerar_documentos_exemplo.py <CPF>

Exemplo:
    python src/arquivos_auxiliares/gerar_documentos_exemplo.py 52998224725
"""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.pdfgen import canvas


def _gerar_pdf(caminho: Path, linhas: list[str]) -> None:
    pdf = canvas.Canvas(str(caminho))
    posicao_y = 800
    for linha in linhas:
        pdf.drawString(50, posicao_y, linha)
        posicao_y -= 20
    pdf.save()
    print(f"Gerado: {caminho}")


def gerar_documentos_exemplo(cpf: str, pasta_destino: Path) -> None:
    pasta_destino.mkdir(parents=True, exist_ok=True)

    _gerar_pdf(
        pasta_destino / f"Ficha_Cadastro_{cpf}.pdf",
        [
            "Nome: Maria da Silva",
            f"CPF: {cpf}",
            "Data de Nascimento: 10/05/1990",
            "Endereco: Rua das Flores, 123 - Manaus/AM",
        ],
    )
    _gerar_pdf(
        pasta_destino / f"Documento_Foto_{cpf}.pdf",
        ["Nome: Maria da Silva", f"CPF: {cpf}", "Data de Nascimento: 10/05/1990"],
    )
    _gerar_pdf(
        pasta_destino / f"Comprovante_Residencia_{cpf}.pdf",
        ["Endereco: Rua das Flores, 123 - Manaus/AM"],
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python gerar_documentos_exemplo.py <CPF>")
        sys.exit(1)

    cpf_informado = sys.argv[1]
    destino = Path(__file__).resolve().parent / "documentos_exemplo"
    gerar_documentos_exemplo(cpf_informado, destino)
