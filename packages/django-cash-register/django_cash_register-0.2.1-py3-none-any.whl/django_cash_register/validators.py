from django.core.exceptions import ValidationError


def positive_number(value):
    """Checking the value. Must be greater than 0."""

    if value <= 0.0:
        raise ValidationError('Count must be greater than 0', params={'value': value},)
