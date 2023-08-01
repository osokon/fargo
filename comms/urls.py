from django.contrib import admin
from django.urls import path
from .views import *
from .sms_api import *

urlpatterns = [
    path('', sms_list, name='sms'),
    path('delivery_reports', get_delivery_status, name='get_delivery_status'),
    path('manual_sms', manual_sms, name='manual_sms'),
    path('sms/<id>/resend', resend_sms, name='resend_sms'),
    path('failed_sms/', failed_sms, name='failed_sms'),
    path('failed_sms/<id>/resend/', resend_single_failed_sms, name='resend_single_failed_sms'),
    path('multiple_failed_sms/resend/', resend_multiple_failed_sms, name='resend_multiple_failed_sms'),
    path('sms_list', sms_list, name='sms_list'),
    path('failed/sms/', fetch_failed_sms, name='fetch_failed_sms'),
    path('manual_bulk_sms', manual_bulk_sms, name='manual_bulk_sms'),


]
