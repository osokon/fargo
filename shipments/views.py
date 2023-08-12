from django.shortcuts import render, redirect
from functools import reduce
import operator
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from shipments.models import Parcel, Shipment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from datetime import datetime, timezone
from django.contrib import messages
from django.db import transaction
import pytz

east_africa_tz = pytz.timezone('Africa/Nairobi')

# Create your views here.
class ParcelCreate(CreateView):
    model = Parcel
    template_name = 'base.html'  # Path to your template
    fields = '__all__'  # Use specific fields if needed
    success_url = reverse_lazy('parcels')


@login_required
@permission_required('parcel.view_parcel', raise_exception=True)
def parcels(request):
    queryset = Parcel.objects.all().order_by('-id')
    filter_names = ('date__lte', 'date__gte', 'delivery_status__iexact', 'source', 'destination')

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        parcels = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        parcels=queryset
            
    
    return render(request, 'parcels.html', locals())

def create_shipment(request):
    if request.method == 'POST':
        print(request.POST)
        # Retrieve data from the POST request
        try: 
            data = {
                'shipment_no': request.POST.get('shipment_no'),
                # 'shipped_on': request.POST.get('shipped_on'),
                # 'eta': request.POST.get('eta'),
            }
            
            with transaction.atomic():
                shipment = Shipment.objects.create(**data)
                parcels_list = request.POST.getlist('parcels')

                for p in Parcel.objects.filter(id__in=parcels_list):
                    if not p.shipment:
                        p.shipment = shipment
                        p.status = 'Packed for Shipping'
                        p.packed_on = datetime.now(east_africa_tz)
                        p.save()
                    else:
                        messages.error(request, "This parcel {parcel} has already been packed in a shipment".format(parcel=p.tracking_no))
                
            return redirect('shipments')
        except Exception as e:
            print(e)
    
    return redirect('shipments')

def ship_shipment(request, id):
    shipment = Shipment.objects.get(id=id)
    if shipment.status.lower() == 'packed':
        try:
            data = {
                'shipped_on': request.POST.get('shipped_on'),
                'eta': request.POST.get('eta'),
            }
            with transaction.atomic():
                update_shipment = Shipment.objects.filter(id=id).update(**data,status='Shipped')
                try:
                    shipped_parcels = Parcel.objects.filter(shipment=shipment).update(status='Shipped',shipped_on=datetime.now(east_africa_tz))
                except Exception as e:
                    print(e)
            
        except Exception as e:
            messages.error(request, e)
    else:
        messages.error(request, 'You cannot ship a shipment that is not in packed state')
    
    return redirect('shipments')

def receive_shipment(request, id):
    shipment = Shipment.objects.get(id=id)
    if shipment.status.lower() == 'shipped':
        try:
            data = {
                'received_on': request.POST.get('received_on'),
            }

            update_shipment = Shipment.objects.filter(id=id).update(**data, status='Received')
            received_parcels = Parcel.objects.filter(shipment=shipment).update(status='In TZ WH',landed_on=datetime.now(east_africa_tz))

        except Exception as e:
            messages.error(request, e)
    else:
        messages.error(request, 'You cannot receive a shipment that is not in shipped state')
    
    return redirect('shipments')

def deliver_parcel(request, id):
    parcel = Parcel.objects.get(id=id)
    if parcel.status.lower() == 'in tz wh':
        try:
            shipment = Parcel.objects.filter(id=id).update(status='Delivered to Client', delivered_on=datetime.now(east_africa_tz))
            
        except Exception as e:
            messages.error(request, e)
    else:
        messages.error(request, 'You cannot deliver a parcel that is not in TZ WH')
    
    return redirect('parcels')

@login_required
@permission_required('comms.view_sms', raise_exception=True)
def shipments(request):
    queryset = Shipment.objects.all().order_by('-id')
    filter_names = ('date__lte', 'date__gte', 'delivery_status__iexact', 'source', 'destination')

    filter_clauses = [Q(**{filter:request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]
    if filter_clauses:
        shipments = queryset.filter(reduce(operator.and_, filter_clauses))

    else:
        shipments=queryset
            
    
    return render(request, 'shipments.html', locals())