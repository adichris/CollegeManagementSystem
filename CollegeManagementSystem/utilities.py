from django.utils.text import slugify
from string import ascii_letters, digits
from random import choice


def random_string_gen(size=5, characters=ascii_letters + digits):
    return "".join(choice(characters) for _ in range(size))


def unique_slug_generate(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.first_name + instance.last_name)
    class_ = instance.__class__
    qs_exists = class_.objects.filter(slug=slug).exists()
    if qs_exists:
        slug = "{slug}-{random}".format(slug=slug, random=random_string_gen())
        return unique_slug_generate(instance, new_slug=slug)
    else:
        return slug


