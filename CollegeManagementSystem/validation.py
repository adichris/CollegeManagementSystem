from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_alphanumberic_space(value):
    if not re.match(r'[\w\s\d]+', value):
        raise ValidationError(
            _("This field should only contains alphanumeric, space. But it has %(value)s"),
            code='errAlphaNumber1',
            params={'value': value}
        )


def is_safe_query(query): return re.match(r'[\w\s\d]+', str(query))
