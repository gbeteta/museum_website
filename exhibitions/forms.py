import datetime

from django import forms
from .models import CONDITION_CHOICES

CONDITION_CHOICES_FORM = [(0, (""),)] + CONDITION_CHOICES

class SearchArtifactsForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=False)
    origin = forms.CharField(label="Country of Origin", max_length=100, required=False)
    excavation_site = forms.CharField(label="Excavation Site", max_length=150, required=False)
    discovery_year = forms.IntegerField(label="Disovery Year", min_value=1500, max_value=2018, required=False)
    condition = forms.ChoiceField(label="Condition", choices = CONDITION_CHOICES_FORM, initial='', required=False)
    material = forms.CharField(label="Material", max_length=50, required=False)
