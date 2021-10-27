from django.contrib import admin
from .models import FormTypeChoicesModel, SalesOfAdmissionForms, StudentForms


@admin.register(FormTypeChoicesModel)
class FormTypeChoicesModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'timestamp')
    search_fields = ('title', 'subtitle')


@admin.register(SalesOfAdmissionForms)
class SalesOfAdmissionForms(admin.ModelAdmin):
    list_display = ('identity', 'received_from', 'amount', 'timestamp')
    readonly_fields = ('identity', 'received_from', 'amount',)


@admin.register(StudentForms)
class StudentForms(admin.ModelAdmin):
    list_display = ('serial_number', 'pin_code', 'status', 'cost')
    search_fields = ('serial_number',)

    list_filter = ('status',)

    def get_readonly_fields(self, request, obj=None):

        # if self.get_.status == 'new':
        #     return ('status', 'candidate_phone_number', 'candidate_name',
        #             'sales_agent', 'sales_point')

        return ('serial_number', 'pin_code', 'status', 'form_type', 'cost', 'candidate_phone_number', 'candidate_name',
                'sales_agent', 'sales_point',)
