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
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('listquejas/', permission_required('users.users')(login_required(ListQuejasView.as_view())), name='list_quejas'),
    path('listaquejaspersonales/', login_required(ListQuejasPersonalesView.as_view()), name='list_quejas_personales'),
    path('quejascreate/', login_required(QuejasCreateView.as_view()), name='create_queja'),
    path('quejaupdate/<int:pk>/', login_required(QuejasUpdateView.as_view()), name='update_queja'),

    path('requerimientopersonaleslist/', permission_required('users.requerimientos')(login_required(ListRequerimientoView.as_view())), name='list_requerimiento_personales'),
    path('requerimientopersonalescreate/', permission_required('users.requerimientos')(login_required(RequerimientoCreateView.as_view())), name='create_requerimiento'),
    path('requerimientopersonalesupdate/<int:pk>/', permission_required('users.requerimientos')(login_required(RequerimientoUpdateView.as_view())), name='update_requerimiento')
]
