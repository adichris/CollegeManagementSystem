from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag(name='institutionFullName')
def get_institution_fullname_name():
    return settings.COLLEGE_FULL_NAME


@register.simple_tag(name='institutionShortName')
def get_institution_short_name():
    return settings.COLLEGE_SHORT_NAME
