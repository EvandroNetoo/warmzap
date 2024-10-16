from django.core.exceptions import ValidationError


def validate_cpf(cpf: str):
    cpf = ''.join(filter(str.isdigit, cpf or ''))

    len_cpf = 11
    if len(cpf) < len_cpf:
        return False

    if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
        return False

    calc = lambda t: int(t[1]) * (t[0] + 2)  # noqa
    d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
    d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11

    if not (str(d1) == cpf[-2] and str(d2) == cpf[-1]):
        raise ValidationError('CPF inválido')
