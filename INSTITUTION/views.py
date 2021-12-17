from django.http.response import JsonResponse
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form


class JsonResponseMixin:
    """
        Mixin to add JSON support to a form.
        Must be used with an object-based FormView (CreateView, UpdateView)
    """

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(self.get_success_data())
        return response

    def get_success_data(self):
        return {
            'success': True,
        }

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            ctx = {}
            ctx.update(csrf(self.request))
            form_html = render_crispy_form(form, context=ctx)
            return JsonResponse({'form_html': form_html, 'success': 'false'}, status=400)
        else:
            return response
