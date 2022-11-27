import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = datetime.datetime.now().year
    if value < 0 or value > current_year:
        raise ValidationError(
            f'Неверный год (0 - {current_year})'
        )
    return value
