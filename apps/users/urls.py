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
from django.urls import path, include
from django.contrib.auth.views import LoginView, logout_then_login, PasswordResetView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import *

from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)

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

    path('metricasinlineview/<int:pk>/', login_required(metricas_inline_view), name='metricas_inline'),
    path('rest/',include(router.urls)),
    path('rest/fingerprint/',FigerPrintViewSet.as_view(), name='figerprint')
]