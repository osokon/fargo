from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from simple_history.models import HistoricalRecords
from django_currentuser.db.models import CurrentUserField

# Create your models here.
class SmsConfig(models.Model):
    sms_enabled = models.BooleanField(default=False)
    provider = models.CharField(max_length=50, default="nextsms")
    sender_id = models.CharField(max_length=11, default="Skuli App")
    headers_authorization = models.CharField(max_length=200, default="GDS")
    live_endpoint = models.CharField(max_length=100, default="https://messaging-service.co.tz/api/sms/v1/text/single")
    balance_endpoint = models.CharField(max_length=100, default="https://messaging-service.co.tz/api/sms/v1/balance")
    delivery_status_endpoint = models.CharField(max_length=100, default="https://messaging-service.co.tz/api/sms/v1/reports?")
    beem_sender_id = models.CharField(max_length=11, default="Skuli")
    beem_headers_authorization = models.CharField(max_length=200, default="GDS")
    beem_live_endpoint = models.CharField(max_length=100, default="GDS")
    beem_balance_endpoint = models.CharField(max_length=100, default="GDS")
    beem_delivery_status_endpoint = models.CharField(max_length=100, default="GDS")
    added_by = CurrentUserField(editable=False)
    added_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        app_label = 'comms'

    def __str__(self):
        return '{} - {}' .format(self.provider, self.sender_id)

class MyModelAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    # if there's already an entry, do not allow adding
    count = SmsConfig.objects.all().count()
    if count == 0:
      return True

    return False


class Sms(models.Model):
    date = models.DateTimeField(auto_now_add=True, editable=False)
    source = models.CharField(max_length=100)
    destination = models.BigIntegerField()
    text = models.CharField(max_length=1000)
    mno = models.CharField(max_length=20, blank=True, null=True, verbose_name="Mobile Network Operator")
    sms_count = models.PositiveIntegerField(null=True)
    delivery_status = models.CharField(max_length=100)
    status_description = models.CharField(max_length=100)
    messageId = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True, editable=False)
    sent_by = CurrentUserField(editable=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, editable=False)

    class Meta:
        app_label = 'comms'

    def __str__(self):
        return self.text

class SmsTemplate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    added_by = CurrentUserField(editable=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'comms'

class DepletionAlert(models.Model):
    date = models.DateField(auto_now_add=True)
    sms_count = models.PositiveIntegerField()
    alerts = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date} -> {self.sms_count}'

    class Meta:
        app_label = 'comms'
