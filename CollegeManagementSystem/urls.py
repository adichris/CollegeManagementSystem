"""CollegeManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('admission/', include('admission.urls')),
    path('accounts/', include('accounts.urls')),
    path('student/', include('student.urls')),
    path('address/', include('address.urls')),
    path('employmentHistory/', include('empoymentHistory.urls')),
    path('sponsor/', include('sponsor.urls')),
    path('faculty/', include('faculty.urls')),
    path('department/', include('department.urls')),
    path('institution/', include('INSTITUTION.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('system/', include('system.urls')),
    path('course/', include('course.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

