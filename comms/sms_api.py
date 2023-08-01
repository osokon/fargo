from django.shortcuts import render
from base64 import b64encode
import requests, json
import base64
from requests.api import request
from requests.auth import HTTPBasicAuth
from administration.slack_api import slack_alert
from django.contrib import messages

from crm import settings
from .models import *
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from datetime import date

today = date.today()


#import environ
#environ.Env.read_env()

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# ###### Basic sms configurations #######
try:
    configs = SmsConfig.objects.all().first()
    provider = configs.provider
except:
    configs = 'test'
    provider = 'test'
    sms_enabled = False

if configs and provider == 'nextsms':
    sender_id = configs.sender_id
    headers_authorization = configs.headers_authorization
    live_endpoint = configs.live_endpoint
    balance_endpoint = configs.balance_endpoint
    delivery_status_endpoint = configs.delivery_status_endpoint
    headers={"Authorization": headers_authorization,"Content-Type": "application/json", "Accept": "application/json"}

elif configs and provider == 'beem':
    sender_id = configs.beem_sender_id
    headers_authorization = configs.beem_headers_authorization
    live_endpoint = configs.beem_live_endpoint
    balance_endpoint = configs.beem_balance_endpoint
    delivery_status_endpoint = configs.beem_delivery_status_endpoint
    headers={"Authorization": headers_authorization,"Content-Type": "application/json", "Accept": "application/json"}

else:
    sms_enabled = False
    sender_id = 'test'
    headers_authorization = 'headers_authorization'
    live_endpoint = 'live_endpoint'
    balance_endpoint = 'balance_endpoint'
    delivery_status_endpoint = 'delivery_status_endpoint'
    headers={"Authorization": headers_authorization,"Content-Type": "application/json", "Accept": "application/json"}


# ###### End basic sms configurations ########

def send_sms(custom_sms, destination):
    try:
        configs = SmsConfig.objects.all().first()
        sms_enabled = configs.sms_enabled
    except:
        sms_enabled = False

    if sms_enabled and provider == 'nextsms':
        payload={"from":sender_id, "to":destination,  "text": custom_sms}
        try:
            response = session.post(live_endpoint, headers=headers, params=payload)
            response = response.json()
            print(response)
            response_dct = {}
            for item in response['messages']:
                response_dct.update(item)
            messageId = response_dct['messageId']
            status = flatten_dict(response_dct['status'])
            delivery_status = status['name']
            sms_count = response_dct['smsCount']
            status_description = status['description']
            
            try:
                Sms.objects.create(source=sender_id,destination=destination,text=custom_sms,messageId=messageId,sms_count=sms_count, delivery_status=delivery_status,status_description=status_description )
            except Exception as e:
                print(e)
            return response

        except Exception as e:
            print(e)
            messages = 'We were unable to send your SMS. please recheck the destination phone number or Sms Package not configured properly'
            pass

    elif sms_enabled and provider == 'beem':
        payload_plain={"source_addr":sender_id,"schedule_time":"","encoding":"0","message":custom_sms,"recipients":[{"recipient_id":1,"dest_addr":str(destination)}]}
        payload = json.dumps(payload_plain, indent=4)
        
        try:
            response = session.post(live_endpoint, headers=headers, data=payload)
            response = response.json()
            print(response)
            messageId = response['request_id']
            status = response['successful']
            delivery_status = "PENDING_ENROUTE"
            status_description = response['message']

            Sms.objects.create(source=sender_id,destination=destination,text=custom_sms,messageId=messageId, delivery_status=delivery_status,status_description=status_description,sent_by=settings.AUTH_USER_MODEL.objects.get(id=1) )

        except:
            messages = 'We were unable to send your SMS. please recheck the destination phone number'
            #pass

    else:
        Sms.objects.create(source=sender_id,destination=destination,text=custom_sms,messageId='messageId', delivery_status='Draft',status_description='Test Message',sent_by=settings.AUTH_USER_MODEL.objects.get(id=1) )

def send_failed_sms(custom_sms, destination, id):
    try:
        configs = SmsConfig.objects.all().first()
        sms_enabled = configs.sms_enabled
    except:
        sms_enabled = False

    if sms_enabled and provider == 'nextsms':
        payload={"from":sender_id, "to":destination,  "text": custom_sms}
        try:
            response = session.post(live_endpoint, headers=headers, params=payload)
            response = response.json()
            print(response)
            response_dct = {}
            for item in response['messages']:
                response_dct.update(item)
            messageId = response_dct['messageId']
            status = flatten_dict(response_dct['status'])
            delivery_status = status['name']
            sms_count = response_dct['smsCount']
            status_description = status['description']
            
            try:
                Sms.objects.filter(id=id).update(source=sender_id,destination=destination,text=custom_sms,messageId=messageId,sms_count=sms_count, delivery_status=delivery_status,status_description="Resent" )
                print('The message has been successfully sent')
            except Exception as e:

                print(e)

        except Exception as e:
            print(e)
            messages = 'We were unable to send your SMS. please recheck the destination phone number or Sms Package not configured properly'
            pass

    elif sms_enabled and provider == 'beem':
        payload_plain={"source_addr":sender_id,"schedule_time":"","encoding":"0","message":custom_sms,"recipients":[{"recipient_id":1,"dest_addr":str(destination)}]}
        payload = json.dumps(payload_plain, indent=4)
        
        try:
            response = session.post(live_endpoint, headers=headers, data=payload)
            response = response.json()
            print(response)
            messageId = response['request_id']
            status = response['successful']
            delivery_status = "PENDING_ENROUTE"
            status_description = response['message']

            Sms.objects.create(source=sender_id,destination=destination,text=custom_sms,messageId=messageId, delivery_status=delivery_status,status_description=status_description,sent_by=settings.AUTH_USER_MODEL.objects.get(id=1) )

        except:
            messages = 'We were unable to send your SMS. please recheck the destination phone number'
            #pass


def flatten_dict(dd, separator ='_', prefix =''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

def get_sms_balance():
    if provider == 'nextsms':
        try:
            response = session.get(balance_endpoint, headers=headers).json()
            return response['sms_balance']
        except:
            messages = 'Messages package not configured properly'

    elif provider == 'beem':
        try:
            response = session.get(balance_endpoint, headers=headers).json()
            status = flatten_dict(response['data'])
            return status['credit_balance']
        except:
            messages = 'Messages package not configured properly'

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def get_delivery_status(request):
    pending_sms = Sms.objects.filter(delivery_status='PENDING_ENROUTE')

    for sms in pending_sms:
        if provider == 'nextsms':
            try:
                payload = {'messageId':sms.messageId}
                response = requests.get(delivery_status_endpoint, headers=headers, params=payload).json()
                response_dct = {}
                for item in response['results']:
                    response_dct.update(item)
                print(response_dct)
                messageId = response_dct['messageId']
                status = flatten_dict(response_dct['status'])
                delivery_status = status['name']
                status_description = status['description']
                Sms.objects.filter(messageId=sms.messageId).update(delivery_status=delivery_status,status_description=status_description)
            except Exception as e:
                messages.error(request, 'Failed to get delivery status for: '+str(sms.destination))
                pass
        elif provider == 'beem':
            dest_addr = sms.destination
            request_id = sms.messageId

            endpoint = str(delivery_status_endpoint).format(dest_addr=dest_addr,request_id=request_id)

            try:
                response = requests.get(endpoint, headers=headers).json()

                response_dct = {}
                for item in response:
                    response_dct.update(item)

                messageId = response_dct['request_id']
                status = response_dct['status']
                delivery_status = status
                status_description = status
                Sms.objects.filter(messageId=sms.messageId).update(delivery_status=delivery_status,status_description=status_description)
            except Exception as e:
                messages.error(request, 'Failed to get delivery status for: '+str(sms.destination))
                pass

    return HttpResponseRedirect(reverse('sms_list'))

@login_required
@permission_required('comms.add_sms', raise_exception=True)
def fetch_failed_sms(request):
    endpoint = "https://messaging-service.co.tz/api/sms/v1/logs?sentSince={send_date}"
    
    try:
        response = requests.get(endpoint.format(send_date=today), headers=headers).json()
        response_list = response['results']
        response_dct = {}
        i=1
        for r in response_list:
            # print(response['results'])
            response_dct.update(r)
            print(r)
            messageId = response_dct['messageId']
            status = flatten_dict(response_dct['status'])
            delivery_status = status['name']
            sms_count = response_dct['smsCount']
            destination = response_dct['to']
            custom_sms = response_dct['text']
            sender_id = response_dct['from']
            date = response_dct['sentAt']
            status_description = status['description']
            print('date:',date,'custom_sms:',custom_sms,'destination:',destination)
            
            check = Sms.objects.filter(text=custom_sms,destination=destination,date__date=today)
            
            if not check:
                Sms.objects.create(source=sender_id,destination=destination,text=custom_sms,messageId=messageId,sms_count=sms_count, delivery_status=delivery_status,status_description=status_description )
                
                i += 1
        
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong when fetching failed sms')
        pass

    sms_list = Sms.objects.filter(date__date=today,delivery_status__iexact='REJECTED_NOT_ENOUGH_CREDITS')
    sms_count = sms_list.count()

    return render(request, 'comms/failed_sms.html', locals())
