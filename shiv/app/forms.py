from django import forms
from django.conf import settings

MARKETS = (
    ("us", "United States"), ("uk", "United Kingdom"), ("au", "Australia"),
    ("ca", "Canada"), ("de", "Germany"),
)

env = []
for m in settings.ENVIRONMENTS.keys():
    env.append((m, m))

ENVS = tuple(env)

IN_PROXIMITY_TO_RESTAURANT, CANCELLED = "IN_PROXIMITY_TO_RESTAURANT", "CANCELLED"

RELEASE_STATUSES = ((IN_PROXIMITY_TO_RESTAURANT, "In Proximity to Restaurant"),)

CANCEL_STATUSES = ((CANCELLED, "Cancelled"),)

CUSTOMER, RESTAURANT, DSP, NONE = "CUSTOMER", "RESTAURANT", "DSP", "NONE"

CANCELLING_PARTY = ((CUSTOMER, "Customer"), (RESTAURANT, "Restaurant"), (DSP, "DSP"))

PARTY_AT_FAULT = ((CUSTOMER, "Customer"), (RESTAURANT, "Restaurant"), (DSP, "DSP"), (NONE, "None"))

OTHER = "OTHER"

REASONS = ((OTHER, "Other"),)


class RequestForm(forms.Form):
    market = forms.ChoiceField(widget=forms.Select(), choices=MARKETS, label="Market")
    environment = forms.ChoiceField(choices=ENVS, widget=forms.Select(), label="Environment")
    deliveryId = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Enter delivery ID"}),
                                 label="Delivery ID")
    checkInCode = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Enter checkin code"}),
                                  label="Check-in code")

    status = forms.ChoiceField(choices=RELEASE_STATUSES, initial=IN_PROXIMITY_TO_RESTAURANT, widget=forms.Select(),
                               label="Status", disabled=True)


class CancelForm(forms.Form):
    market = forms.ChoiceField(widget=forms.Select(), choices=MARKETS, label="Market")
    environment = forms.ChoiceField(choices=ENVS, widget=forms.Select(), label="Environment")
    deliveryId = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Enter delivery ID"}),
                                 label="Delivery ID")
    checkInCode = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"placeholder": "Enter checkin code"}),
                                  label="Check-in code")
    cancellingParty = forms.ChoiceField(widget=forms.Select(), choices=CANCELLING_PARTY, label="Cancelling party")
    partyAtFault = forms.ChoiceField(widget=forms.Select(), choices=PARTY_AT_FAULT, label="Party at fault")
    reason = forms.ChoiceField(widget=forms.Select(), choices=REASONS, label="Reason")
    status = forms.ChoiceField(initial=CANCELLED, choices=CANCEL_STATUSES, widget=forms.Select(), disabled=True,
                               label="Status")
