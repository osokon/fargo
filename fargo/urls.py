"""fargo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from shipments.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('administration.urls')),
    path('add_parcel', ParcelCreate.as_view(), name='create_parcel'),
    path('deliver_parcel/<id>/', deliver_parcel, name='deliver_parcel'),
    path('parcels', parcels, name='parcels'),
    path('add_shipment', create_shipment, name='create_shipment'),
    path('ship_shipment/<id>/', ship_shipment, name='ship_shipment'),
    path('receive_shipment/<id>/', receive_shipment, name='receive_shipment'),
    path('shipments', shipments, name='shipments'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('accounts/logout/', auth_views.LogoutView.as_view(),{'next': '/accounts/login'}),
    path('change_password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('logout'), template_name='change_password.html')),
    
]
