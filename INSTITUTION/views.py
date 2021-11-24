from django.http.response import JsonResponse


class JsonResponseMixin:
    """
        Mixin to add JSON support to a form.
        Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.accept('text/html'):
            return response
        else:
            return JsonResponse(self.get_success_data())

    def get_success_data(self):
        return {
            'pk': self.object.pk,
        }

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)