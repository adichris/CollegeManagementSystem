import datetime
from django.db.models import TextChoices


def get_admission_steps(admission_status):
    from admission.models import FormStatusChoice
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
    return 1,


class AcademicYear:
    FROM_YEAR = 2000
    TO_YEAR = datetime.date.today().year

    def __iter__(self):
        self.choices()

    @classmethod
    def default(cls):
        return cls.TO_YEAR - 1, cls.TO_YEAR

    @classmethod
    def choices(cls):
        if cls.FROM_YEAR > cls.TO_YEAR:
            raise ValueError('FROM_YEAR > TO_YEAR')
        return (
            (f'{x - 1}/{x}', f'{x - 1}/{x}') for x in range(cls.TO_YEAR, cls.FROM_YEAR, -1)
        )

    @classmethod
    def default(cls):
        return cls.TO_YEAR-1, cls.TO_YEAR


class SemesterChoice(TextChoices):
    SEMESTER_1 = 'First Semester', 's1'
    SEMESTER_2 = 'Second Semester', 's2'
