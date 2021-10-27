from .views import LandingPage, AboutUsPage, INSTITUTION_NAME, LoginPage, LogoutPage, AdministratorHomePage
from django.urls import path

app_name = 'Home'
urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
    path('about'+INSTITUTION_NAME.get('institution_short_name').lower(), AboutUsPage.as_view(), name="about_institution"),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('administration/', AdministratorHomePage.as_view(), name='admin'),
]
