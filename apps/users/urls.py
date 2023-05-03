"""fingerserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, register_converter
from django.contrib.auth.views import LoginView, logout_then_login, PasswordResetView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from datetime import datetime
from .views import *

from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'metricas', MetricasViewSet)

class DateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', login_required(main), name='main'),
    path('login/',
        LoginView.as_view(template_name='auth/login.html'),
        name='login'
    ),
    path('logout/',
        logout_then_login,
        name='logout'
    ),
    path('createuser/', login_required(CreateUserView.as_view()), name='create_user'),
    path('listuser/', login_required(ListUserView.as_view()), name='list_user'),
    path('constance/', login_required(ConstanceView.as_view()), name='constance'),

    path('metricasinlineview/<int:pk>/', login_required(metricas_inline_view), name='metricas_inline'),
    path('rest/',include(router.urls)),
    path('rest/fingerprint/',FigerPrintViewSet.as_view(), name='figerprint'),

    path('dateplanillas/<int:pk>', login_required(PlanillaDataView.as_view()), name='date_planillas'),
    path('planilladetail/<int:pk>/<date:fini>/<date:ffin>/', login_required(PlanillaDetailPDF.as_view()), name='planilla_detail'),
  
    path('dateplanillashc/<int:pk>', login_required(PlanillaDataHCView.as_view()), name='date_planillashc'),
    path('planilladetailhc/<int:pk>/<date:fini>/<date:ffin>/', login_required(PlanillaDetailHCPDF.as_view()), name='planilla_detailhc'),

    path('listpermisosg/', login_required(ListPermisosGView.as_view()), name='list_permisosg'),
    path('createpermisog/', login_required(CreatePermisosGView.as_view()), name='create_permisog'),
    path('updatepermisog/<int:pk>/', login_required(UpdatePermisosGView.as_view()), name='update_permisog'),

    path('listpermisos/<int:pk>/', login_required(ListPermisosView.as_view()), name='list_permisos'),
    path('createpermisos/<int:pk>/', login_required(CreatePermisosView.as_view()), name='create_permisos'),
    path('updatepermisos/<int:pk>/', login_required(UpdatePermisosView.as_view()), name='update_permisos'),
]
