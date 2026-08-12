"""Validação de CPF (formato e dígitos verificadores).

Implementa a regra de negócio RN03 do Mini PDD: "O CPF informado deve ser
válido (formato e dígitos verificadores) e coincidir em todos os documentos
enviados."
"""

from __future__ import annotations

import re


def limpar_cpf(cpf: str) -> str:
    """Remove tudo que não for dígito de uma string de CPF."""
    return re.sub(r"\D", "", cpf or "")


def cpf_e_valido(cpf: str) -> bool:
    """Valida um CPF conferindo formato (11 dígitos) e dígitos verificadores."""
    cpf_numeros = limpar_cpf(cpf)

    if len(cpf_numeros) != 11:
        return False

    # CPFs com todos os dígitos iguais (ex.: 111.111.111-11) são inválidos,
    # apesar de matematicamente "passarem" no cálculo do dígito verificador.
    if cpf_numeros == cpf_numeros[0] * 11:
        return False

    return _calcular_digito_verificador(cpf_numeros[:9]) == cpf_numeros[9] and (
        _calcular_digito_verificador(cpf_numeros[:10]) == cpf_numeros[10]
    )


def _calcular_digito_verificador(base: str) -> str:
    peso_inicial = len(base) + 1
    soma = sum(int(digito) * peso for digito, peso in zip(base, range(peso_inicial, 1, -1)))
    resto = (soma * 10) % 11
    return "0" if resto == 10 else str(resto)


def formatar_cpf(cpf: str) -> str:
    """Formata um CPF de 11 dígitos como 'XXX.XXX.XXX-XX'."""
    cpf_numeros = limpar_cpf(cpf)
    if len(cpf_numeros) != 11:
        return cpf
    return f"{cpf_numeros[0:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:11]}"
