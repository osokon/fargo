# pip install slack_sdk
import requests, json
from requests.api import request
from requests.adapters import HTTPAdapter
from administration.serializers import AgentSerializer
from requests.packages.urllib3.util.retry import Retry
from django.db.models import Case, Value, When
from django.db.models import CharField
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
headers={"Content-Type": "application/json", "Accept": "application/json"}


script_alerts = "https://hooks.slack.com/services/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"
backup_alerts = "https://hooks.slack.com/services/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"
server_errors = "https://hooks.slack.com/services/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"

def slack_alert(channel,link,subdomain,user_data,error_detail):
    
    if channel=='server_errors':
        url = "https://hooks.slack.com/services/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"
        payload=json.dumps(
        {
          "channel": "CBR2V3XEX",
          "attachments": [
              {
                  "color": "#FF0000",
                  "pretext": "A server error has occuried",
                  "author_name": subdomain,
                  "author_icon": "https://emoji.slack-edge.com/T02GH83EV/alert/d44c52346d0143c2.png",
                  "title": link,
                  "title_link": link,
                  "text":" ` "+str(error_detail)+" ` \n _[user: "+user_data+"]_"
              }
          ]
        }
        )
    elif channel == 'backup_alerts':
        url = "https://hooks.slack.com/services/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"
    elif channel == 'script_alerts':
        url = "https://hooks.slack.com/services/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"
    
    if channel == 'backup_alerts' or channel == 'script_alerts':
        payload=json.dumps(
            {
            "channel": "CBR2V3XEX",
            "attachments": [
                {
                    "color": "#007f00",
                    "pretext": link,
                    "author_name": subdomain,
                    "author_icon": "https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-large/1f382@2x.png",
                    # "title": link,
                    # "title_link": link,
                    "text":" ` "+str(error_detail)+" ` \n _[user: "+user_data+"]_"
                }
            ]
            }
            )

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getAgents(request):
    agents = User.objects.all()

    serializer = AgentSerializer(agents, context={'request': None}, many=True)

    return Response(serializer.data)