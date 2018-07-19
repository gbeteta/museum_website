import datetime

from django import forms
from .models import CONDITION_CHOICES, CONDITION_CHOICES_ORGANISM

CONDITION_CHOICES_FORM = [(0, (""),)] + CONDITION_CHOICES
CONDITION_CHOICES_FORM_ORGANISM = [(0, (""),)] + CONDITION_CHOICES_ORGANISM

class SearchArtifactsForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=False)
    origin = forms.CharField(label="Country of Origin", max_length=100, required=False)
    excavation_site = forms.CharField(label="Excavation Site", max_length=150, required=False)
    discovery_year = forms.IntegerField(label="Disovery Year", min_value=1500, max_value=2018, required=False)
    condition = forms.ChoiceField(label="Condition", choices = CONDITION_CHOICES_FORM, initial='', required=False)
    material = forms.CharField(label="Material", max_length=50, required=False)


class SearchFossilForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=False)
    origin = forms.CharField(label="Country of Origin", max_length=100, required=False)
    excavation_site = forms.CharField(label="Excavation Site", max_length=150, required=False)
    discovery_year = forms.IntegerField(label="Disovery Year", min_value=1500, max_value=2018, required=False)
    period = forms.CharField(label="Period", max_length=50, required=False)

class SearchOrganismForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=False)
    scientific_name = forms.CharField(label="Scientific Name", max_length=100, required=False)
    condition = forms.ChoiceField(label="Condition", choices = CONDITION_CHOICES_FORM_ORGANISM, initial='', required=False)

class SearchArtworkForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=False)
    art_type = forms.CharField(label="Style", max_length=50, required=False)
    author = forms.CharField(label="Author", max_length=100, required=False)
    year = forms.IntegerField(label="Year", min_value=1, max_value=2018, required=False)