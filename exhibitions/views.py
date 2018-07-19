from django.shortcuts import render
from django.http import HttpResponse

from .forms import SearchArtifactsForm
from .models import *

def index(request):
    return render(request, 'exhibitions/index.html', {})

def search_artifacts(request):
    if request.method == 'POST':
        form = SearchArtifactsForm(request.POST)

        if form.is_valid():
            results = Artifact.objects.all()

            if form.cleaned_data["name"]:
                results = results.filter(name__icontains=form.cleaned_data["name"])
            
            if form.cleaned_data["origin"]:
                results = results.filter(country_origin__icontains=form.cleaned_data["origin"])

            if form.cleaned_data["excavation_site"]:
                results = results.filter(excavation_site__icontains=form.cleaned_data["excavation_site"])

            if form.cleaned_data["discovery_year"]:
                results = results.filter(discovery_year__exact=form.cleaned_data["discovery_year"])
            
            if form.cleaned_data["condition"] != '0':
                results = results.filter(condition__exact=int(form.cleaned_data["condition"]))

            if form.cleaned_data["material"]:
                results = results.filter(material__iexact=form.cleaned_data["material"])

            return render(request, 'exhibitions/results_artifacts.html', {'form': form, 'results': results})
    else:
        form = SearchArtifactsForm()

    return render(request, 'exhibitions/search_artifacts.html', {'form': form})
