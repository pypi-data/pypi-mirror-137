from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def password_strength_validate(value):
    """Validates that a password is as least 7 characters long and has at least
       1 digit and 1 letter.
       """
    min_length = 7

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))
