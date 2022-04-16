from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import reverse, resolve_url, redirect

INSTITUTION_NAME = dict(
    institution_full_name=settings.COLLEGE_FULL_NAME,
    institution_short_name=settings.COLLEGE_SHORT_NAME,

)


class LandingPage(TemplateView):
    template_name = "home/landingpage.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(INSTITUTION_NAME)
        return ctx


class AboutUsPage(TemplateView):
    template_name = "home/about_us_page.html"

    def get_context_data(self, **kwargs):
        ctx = super(AboutUsPage, self).get_context_data(**kwargs)
        ctx.update(INSTITUTION_NAME)
        ctx["title"] = 'About Us'

        return ctx


class AdministratorHomePage(LoginRequiredMixin, TemplateView):
    template_name = 'home/admin/templateview.html'

    def get_login_url(self):
        return reverse('Home:login')


class LoginPage(LoginView):
    template_name = 'home/login.html'

    def get_context_data(self, **kwargs):
        ctx = super(LoginPage, self).get_context_data(**kwargs)
        ctx['title'] = 'Login - %s' % INSTITUTION_NAME['institution_short_name']
        ctx['institution_short'] = INSTITUTION_NAME['institution_short_name']
        ctx['header'] = INSTITUTION_NAME['institution_full_name']
        from crispy_forms.helper import FormHelper
        from crispy_forms.bootstrap import FormActions, StrictButton
        form_helper = FormHelper(self.get_form())
        form_helper.layout.append(
            FormActions(
                StrictButton('Reset', type='reset', css_class='btn btn-light  flex-grow-1'),
                StrictButton('Login',  type='submit', onclick='dynamicSpinner(this)',
                             css_class='btn btn-primary  flex-grow-1'),
                css_class='d-flex justify-content-end'
            )
        )
        ctx['form_helper'] = form_helper
        return ctx

    def get_success_url(self):
        next_url = self.request.GET.get(self.redirect_field_name)
        if next_url:
            return next_url
        user = self.request.user
        if user.is_admin or user.is_superuser:
            return reverse('Home:admin')
        elif user.student:
            return reverse('Student:home')
        return reverse('Home:landing_page')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # user = self.request.user
            # user.is_online = True
            # user.save()
            return redirect('Home:landing_page')
        return super(LoginPage, self).get(request, *args, **kwargs)



class LogoutPage(LogoutView):

    def get_next_page(self):
        return reverse('Home:landing_page')
