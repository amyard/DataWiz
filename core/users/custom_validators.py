from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class MinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=4):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Пароль должен состоять как минимум из %(min_length)d символов."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Пароль должен состоять как минимум из %(min_length)d символов."
            % {'min_length': self.min_length}
        )
