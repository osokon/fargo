import csv
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from shipments.models import Parcel, Shipment
from .models import *
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import UserGroupForm, UserForm
from .slack_api import slack_alert
from functools import reduce
import operator
import sys
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def users(request):
    users = SystemUser.objects.all()

    return render(request, 'users.html', locals())

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def export_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Users.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Username', 'Email'])

    groups = SystemUser.objects.all().values_list('id', 'first_name', 'last_name', 'username', 'email')
    for group in groups:
        writer.writerow(group)

    return response

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def roles(request):
    roles = Group.objects.all()

    return render(request, 'user_roles.html', locals())

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def user_activities(request):
    queryset = AuditEntry.objects.all()
    filter_names = ('action','time__gte','time__lte','username')

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        activities = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        activities=queryset

    return render(request, 'user_activities.html', locals())

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def user_profile(request, id):
    user = SystemUser.objects.get(id=id)
    users = SystemUser.objects.all()
    user_profile = True

    return render(request, 'user_profile.html', locals())

class UserCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView, SuccessMessageMixin):
    permission_required = 'auth.add_user'
    form_class = UserForm
    template_name = 'add_user.html'


    def form_valid(self, form):
        user = form.save()
        
        return HttpResponseRedirect(reverse('users'))

class GroupCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView, SuccessMessageMixin):
    permission_required = 'auth.add_group'
    form_class = UserGroupForm
    template_name = 'add_group.html'


    def form_valid(self, form):
        group = form.save()
        success_message = 'Role created successfully!'

        return HttpResponseRedirect(reverse('roles'))

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='student-list')
def users_filter(request):
    queryset = SystemUser.objects.all()
    filter_names = ('is_active',)

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        users = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        users=queryset
   
    return render(request, 'users.html', locals())


def server_error(request):
    channel = 'server_errors'
    subdomain = str(request.META['HTTP_HOST'].split('.')[0])
    msg = str(request.build_absolute_uri())
    type, value, tb = sys.exc_info()

    try:
        user_data = str(request.user)+' ('+str(request.user.get_full_name())+')'
    except:
        user_data = "---"
    try:
        slack_alert(channel,msg,subdomain,user_data,value)
    except Exception as e:
        messages.error(request, "Error sending slack alert: " +str(e))

    return render(request, '500.html', locals())

@login_required
def dashboard(request):
    pending_parcels = Parcel.objects.filter(status__iexact='In China WH').count()
    packed_parcels = Parcel.objects.filter(status__iexact='Packed for Shipping').count()
    shipped_parcels = Parcel.objects.filter(status__iexact='Shipped').count()
    delivered_parcels = Parcel.objects.filter(status__iexact='In TZ WH').count()

    packed_shipments = Shipment.objects.filter(status__iexact='Packed').count()
    intransit_shipments = Shipment.objects.filter(status__iexact='Shipped').count()
    delivered_shipments = Shipment.objects.filter(status__iexact='Received').count()
    return render(request, 'dashboard.html', locals())