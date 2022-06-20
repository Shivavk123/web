import datetime
import json
import uuid
import requests
from urllib.request import Request, urlopen

from django.conf import settings
from django.shortcuts import render

# Create your views here.
from app.forms import *


def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + settings.ENVIRONMENTS["US-STAG01"]["authCode"]
    }

    try:
        res = requests.post("https://na-mte.api.mcd.com/v1/security/auth/token?grantType=client_credentials",
                            headers=headers)
        data = res.json()
        if res.status_code != 200:
            raise Exception(data["response"])
        data = data["response"]

        if data is not None:
            return data["token"]
        raise Exception("No data!")
    except Exception as e:
        print(e)
        raise Exception(e)


def request_view(request):
    title, action, error = "Delivery release workflow", "Submit", None

    if request.method == "POST":
        form = RequestForm(request.POST)
        market = request.POST.get("market", None)
        environment = request.POST.get("environment", None)
        delivery_id = request.POST.get("deliveryId", None)
        checkin_code = request.POST.get("checkInCode", None)
        status = request.POST.get("status", None)

        event_id = str(uuid.uuid4())
        event_time = datetime.datetime.utcnow().isoformat()

        config = settings.ENVIRONMENTS[environment]

        try:
            token = get_token()

            body = {
                "eventId": event_id,
                "eventTime": event_time,
                "eventType": "STATUS_EVENT",
                "eventDetails": {
                    "mcdDeliveryId": delivery_id,
                    "mcdCheckinCode": checkin_code,
                    "statusEventDetails": {
                        "status": status
                    }
                }
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                'mcd-clientid': config["clientId"],
                'mcd-clientsecret': config["clientSecret"]
            }
            print(headers)
            body = json.dumps(body)
            body = body.encode("utf-8")

            print(body)
            url = config["url"] + '/exp/v1/delivery/events/na/doordash'
            print(url)
            req = Request(url, body, headers)

            urlopen(req)
            return render(request, "response.html", {
                "desc": "Delivery released successfully!",
                "icon": "2713", "cls": "success",
                "next": "/request/?token=" + token
            })
        except Exception as e:
            form.add_error(None, e)
    else:
        form = RequestForm()

    return render(request, "form.html", {"form": form, "title": title, "error": error, "action": action})


def cancel_view(request):
    title, action, error = "Delivery cancel workflow", "Cancel", None

    if request.method == "POST":
        form = CancelForm(request.POST)

        market = request.POST.get("market", None)
        environment = request.POST.get("environment", None)
        delivery_id = request.POST.get("deliveryId", None)
        checkin_code = request.POST.get("checkInCode", None)
        cancelling_party = request.POST.get("cancellingParty", None)
        party_at_fault = request.POST.get("partyAtFault", None)
        reason = request.POST.get("reason", None)
        status = request.POST.get("status", None)

        event_id = str(uuid.uuid4())
        event_time = datetime.datetime.utcnow().isoformat()

        config = settings.ENVIRONMENTS[environment]

        try:
            token = get_token()

            body = {
                "eventId": event_id,
                "eventTime": event_time,
                "eventType": "STATUS_EVENT",
                "eventDetails": {
                    "mcdDeliveryId": delivery_id,
                    "mcdCheckinCode": checkin_code,
                    "statusEventDetails": {
                        "status": status,
                        "cancellationDetails": {
                            "cancellingParty": cancelling_party,
                            "cancellationReason": reason,
                            "partyAtFault": party_at_fault
                        }
                    }
                }
            }

            print(body)

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                'mcd-clientid': config["clientId"],
                'mcd-clientsecret': config["clientSecret"]
            }

            print(headers)

            body = json.dumps(body)
            body = body.encode("utf-8")

            url = config["url"] + '/exp/v1/delivery/events/' + market + '/doordash'
            print(url)
            req = Request(url, body, headers)

            urlopen(req)
            return render(request, "response.html", {
                "desc": "Delivery cancelled successfully!",
                "icon": "2717", "cls": "danger",
                "next": "/cancel/?token=" + token
            })
        except Exception as e:
            form.add_error(None, e)
    else:
        form = CancelForm()

    return render(request, "form.html", {"form": form, "title": title, "error": error, "action": action})
