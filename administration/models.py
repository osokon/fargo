from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from fargo import settings
from django_currentuser.db.models import CurrentUserField


#from django.contrib.gis.geoip2 import GeoIP2

# Create your models here.
status_choices = (
    ('Active', 'Active'),
    ('Disabled', 'Disabled'),
)

gender_choices = (
    ('male', 'Male'),
    ('female', 'Female'),
)



class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)
    added_by = CurrentUserField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SystemUser(AbstractUser):
    primary_phone = models.PositiveBigIntegerField(blank=True, null=True)
    secondary_phone = models.PositiveBigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=gender_choices, default='male')
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='supervisee')
    added_by = CurrentUserField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # If you don't need any additional fields, you can leave this empty
    # pass

class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    username = models.CharField(max_length=256, null=True)
    ip = models.GenericIPAddressField(null=True)
    city = models.CharField(max_length=256, null=True)
    device_type = models.CharField(max_length=256, null=True)
    browser_type = models.CharField(max_length=256, null=True)
    browser_version = models.CharField(max_length=256, null=True)
    os_type = models.CharField(max_length=256, null=True)
    os_version = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    class Meta:
        verbose_name = 'Audit Entry'
        verbose_name_plural = 'Audit Entries'


# @receiver(user_logged_in)
# def logged_in_callback(sender, request, user, **kwargs):
#     ip = request.META.get('REMOTE_ADDR')
#     #ip = request.META['HTTP_X_FORWARDED_FOR']
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
    
#     if request.user_agent.is_mobile:
#         device_type = "Mobile"
#     if request.user_agent.is_tablet:
#         device_type = "Tablet"
#     if request.user_agent.is_pc:
#         device_type = "PC"
    
#     browser_type = request.user_agent.browser.family
#     browser_version = request.user_agent.browser.version_string
#     os_type = request.user_agent.os.family
#     os_version = request.user_agent.os.version_string
  
#     #g = GeoIP2()
#     #city = g.city(ip)['city']
#     AuditEntry.objects.create(action='logged_in', ip=ip, username=user.username, device_type=device_type, browser_type=browser_type, browser_version=browser_version, os_type=os_type, os_version=os_version)


# @receiver(user_logged_out)
# def logged_out_callback(sender, request, user, **kwargs):
#     #ip = request.META.get('REMOTE_ADDR')
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     #g = GeoIP2()
#     #city = g.city(ip)['city']

#     if request.user_agent.is_mobile:
#         device_type = "Mobile"
#     if request.user_agent.is_tablet:
#         device_type = "Tablet"
#     if request.user_agent.is_pc:
#         device_type = "PC"
    
#     browser_type = request.user_agent.browser.family
#     browser_version = request.user_agent.browser.version_string
#     os_type = request.user_agent.os.family
#     os_version = request.user_agent.os.version_string

#     AuditEntry.objects.create(action='logged_out', ip=ip, username=user.username, device_type=device_type, browser_type=browser_type, browser_version=browser_version, os_type=os_type, os_version=os_version)


# @receiver(user_login_failed)
# def login_failed_callback(sender, credentials, **kwargs):
#     AuditEntry.objects.create(action='login_failed', username=credentials.get('username', None))

class AuditTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity_name + ' ' + str(self.created_at)

    class Meta:
        verbose_name = 'Audit Trail'
        verbose_name_plural = 'Audit Trails'


