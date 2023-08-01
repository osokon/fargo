from unicodedata import name
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from datetime import date
from django.contrib.auth.models import User, Group
from requests.api import request

from .models import *
from .sms_api import *
from functools import reduce
import operator
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_q.tasks import async_task

#your views here

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def manual_sms(request):
    destination = request.POST.get('destination')
    custom_sms = request.POST.get('text')

    send_sms(custom_sms, destination)

    return HttpResponseRedirect(reverse('sms_list'))

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def resend_sms(request, id):
    sms_obj = Sms.objects.get(id=id)
    destination = sms_obj.destination
    custom_sms = sms_obj.text

    send_sms(custom_sms, destination)

    return HttpResponseRedirect(reverse('sms_list'))

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def resend_single_failed_sms(request, id):
    sms_obj = Sms.objects.get(id=id)
    destination = sms_obj.destination
    custom_sms = sms_obj.text

    send_failed_sms(custom_sms, destination, id)


    return HttpResponseRedirect(reverse('failed_sms'))

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def resend_multiple_failed_sms(request):
    sms_obj = Sms.objects.get(id=id)
    destination = sms_obj.destination
    custom_sms = sms_obj.text

    async_task(send_sms, custom_sms, destination)

    return HttpResponseRedirect(reverse('sms_list'))

@login_required
@permission_required('comms.view_sms', raise_exception=True)
def failed_sms(request):
    balance = get_sms_balance()
    queryset = Sms.objects.filter(delivery_status__iexact = 'REJECTED_NOT_ENOUGH_CREDITS').order_by('-id')
    filter_names = ('date__lte', 'date__gte', 'destination')

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        sms_list = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        sms_list=queryset
            
    sms_count = queryset.count()
    
    return render(request, 'comms/failed_sms.html', locals())


@login_required
@permission_required('comms.view_sms', raise_exception=True)
def sms_list(request):
    balance = get_sms_balance()
    queryset = Sms.objects.all().order_by('-id')
    statuses = Sms.objects.values_list('delivery_status', flat=True).distinct()
    filter_names = ('date__lte', 'date__gte', 'delivery_status__iexact', 'source', 'destination')

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        sms_list = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        sms_list=queryset[:100]
            
    sms_count = queryset.aggregate(total=Sum(F('sms_count')))['total']
    
    return render(request, 'comms/sms.html', locals())

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def manual_bulk_sms(request):
    # if request.POST:
    #     destinations = request.POST.get('destinations')
    #     msg = request.POST.get('text')

    #     if destinations == 'teachers':
    #         employees = Employee.objects.filter(designation__name__iexact='teacher', status__iexact='active')
    #         for e in employees:
    #             destination = e.phone
    #             if len(str(destination))==12:
    #                 msg2 = msg.format(teacher=e)
    #                 async_task(send_sms,msg2,destination)

    #         messages.success(request, 'The system is processing and sending ' +str(employees.count())+ ' messages to parents in the background')

    #     elif destinations == 'staffs':
    #         employees = Employee.objects.filter(status__iexact='active')
    #         for e in employees:
    #             destination = e.phone
    #             if len(str(destination))==12:
    #                 msg2 = msg.format(staff=e)
    #                 async_task(send_sms,msg2,destination)

    #         messages.success(request, 'The system is processing and sending ' +str(employees.count())+ ' messages to staffs in the background')

    #     elif destinations == 'all_classes':
    #         parents = Parent.objects.filter(student__current_status='active').distinct()
    #         for p in parents:
    #             destination = p.phone_number
    #             student_name = (s for s in p.student_set.all()[:1])
    #             for s in student_name:
    #                 if len(str(destination))==12:
    #                     msg2 = msg.format(student=s,parent=p)
    #                     async_task(send_sms,msg2,destination)

    #         messages.success(request, 'The system is processing and sending ' +str(parents.count())+ ' messages to parents in the background')
    #     else:
    #         parents = Parent.objects.filter(student__current_status='active',student__in=Student.objects.filter(current_class=destinations)).distinct()
    #         for p in parents:
    #             destination = p.phone_number
    #             student_name = (s for s in p.student_set.all()[:1])
    #             for s in student_name:
    #                 if len(str(destination))==12:
    #                     msg2 = msg.format(student=s,parent=p)
    #                     async_task(send_sms,msg2,destination)
                        
    #         messages.success(request, 'The system is processing and sending ' +str(parents.count())+ ' messages to parents in the background')

    return HttpResponseRedirect(reverse('sms_list'))
