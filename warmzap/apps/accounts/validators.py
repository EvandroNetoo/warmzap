import re

from django.core.exceptions import ValidationError


def validate_cpf(value):
    cpf = re.sub(r'[^0-9]', '', str(value))

    cpf_len = 11

    if len(cpf) != cpf_len:
        raise ValidationError('CPF deve conter 11 dígitos.')

    if len(set(cpf)) == 1:
        raise ValidationError('CPF inválido.')

    soma = 0
    peso = 10

    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % cpf_len
    digito1 = 0 if resto < 2 else cpf_len - resto  # noqa

    if int(cpf[9]) != digito1:
        raise ValidationError('CPF inválido.')

    soma = 0
    peso = cpf_len

    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % cpf_len
    digito2 = 0 if resto < 2 else cpf_len - resto  # noqa

    if int(cpf[10]) != digito2:
        raise ValidationError('CPF inválido.')
