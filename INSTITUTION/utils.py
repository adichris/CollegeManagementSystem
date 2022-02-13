from django.forms import ValidationError
import datetime
from django.db.models import TextChoices
from django.http.response import Http404
from django.shortcuts import render
import os


def get_admission_steps(admission_status):
    from admission.models import FormStatusChoice
    if admission_status in (FormStatusChoice.SUBMITTED, FormStatusChoice.ACCEPTED, FormStatusChoice.REJECTED):
        raise Http404('You can not edit your admission form again!')
    if FormStatusChoice.AT_PROFILE == admission_status:
        return 1,
    elif admission_status == FormStatusChoice.AT_ADDRESS:
        return range(1, 3)
    elif admission_status == FormStatusChoice.AT_EMPLOYMENT:
        return range(1, 4)
    elif admission_status == FormStatusChoice.AT_SPONSOR:
        return range(1, 5)
    elif admission_status == FormStatusChoice.AT_PROGRAMME:
        return range(1, 6)
    elif admission_status == FormStatusChoice.AT_CERTIFICATION:
        return range(1, 7)
    elif admission_status == FormStatusChoice.AT_EDUCATION:
        return range(1, 8)
    elif admission_status == FormStatusChoice.COMPLETED:
        return range(1, 9)
    return 1,


class AcademicYear:
    FROM_YEAR = 2000
    TO_YEAR = datetime.date.today().year

    def __iter__(self):
        self.choices()

    @classmethod
    def default(cls):
        return cls.formulate_academic_year(cls.TO_YEAR)

    @classmethod
    def choices(cls):
        if cls.FROM_YEAR > cls.TO_YEAR:
            raise ValueError('FROM_YEAR > TO_YEAR')
        return (
            (cls.formulate_academic_year(x), cls.formulate_academic_year(x)) for x in range(cls.TO_YEAR, cls.FROM_YEAR, -1)
        )

    @classmethod
    def formulate_academic_year(cls, year):
        """
        :param year: the current year
        :return:  last_year/this_year
        """
        return f'{year - 1}/{year}'

    @classmethod
    def extract_academic_year(cls, date_admitted):
        return cls.formulate_academic_year(date_admitted)


class SemesterChoice(TextChoices):
    SEMESTER_1 = 'First Semester', 's1'
    SEMESTER_2 = 'Second Semester', 's2'


def get_not_allowed_render_response(request, message="Your not allowed to access this page because of your profile"):
    return render(request, "institution/status_not_allowed.html", {
        "reason": message,
        'back_url': request.GET.get('back')
    })


def get_back_url(request):
    back_url = request.GET.get('back')
    if back_url:
        return back_url
    return request.session.get('back_url')


def get_next_url(request):
    next_url = request.GET.get('next')
    if next_url:
        return next_url


MINIMUM_USER_AGE = 10
PASSPORT_PICTURE_SIZE = (600, 600)


def file_size_validator(file, maximum=PASSPORT_PICTURE_SIZE):
    picture = file
    a, b = maximum
    file_size = a * b
    if picture.size > file_size:
        from django.template.defaultfilters import filesizeformat
        raise ValidationError(f'The file size should be less than {filesizeformat(file_size)}. You uploaded {filesizeformat(picture.size)} ')


def pdf_ext_validator(filename):
    if not os.path.splitext(filename)[1] == '.pdf':
        raise ValidationError('The file format is not supported. Must be .PDF format')
