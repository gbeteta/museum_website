from django.shortcuts import render
from django.http import HttpResponse, Http404

from .forms import SearchArtifactsForm, SearchArtworkForm, SearchFossilForm, SearchOrganismForm
from .models import *

def index(request):
    return render(request, 'exhibitions/index.html', {})

def get_item(request, item_id):
    if Item.objects.filter(pk=item_id).count():
        item = Item.objects.get(pk=item_id)
    else:
        raise Http404("Item not found")

    if item.artifact:
        item = item.artifact
    elif item.organism:
        item = item.organism
    elif item.fossil:
        item = item.fossil
    elif item.artword:
        item = item.artwork
    
    return render(request, "exhibitions/item.html", {"item": item, "type": item.__class__.__name__})

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

            return render(request, 'exhibitions/search_artifacts.html', {'form': form, 'results': results})
    else:
        form = SearchArtifactsForm()

    return render(request, 'exhibitions/search_artifacts.html', {'form': form, 'results':{}})

def search_artworks(request):
    if request.method == 'POST':
        form = SearchArtworkForm(request.POST)

        if form.is_valid():
            results = Artwork.objects.all()

            if form.cleaned_data["name"]:
                results = results.filter(name__icontains=form.cleaned_data["name"])

            if form.cleaned_data["year"]:
                results = results.filter(year__exact=form.cleaned_data["year"])
            
            if form.cleaned_data["author"]:
                results = results.filter(author__icontains=form.cleaned_data["author"])

            if form.cleaned_data["style"]:
                results = results.filter(art_type__icontains=form.cleaned_data["style"])

            return render(request, 'exhibitions/search_artworks.html', {'form': form, 'results': results})
    else:
        form = SearchArtworkForm()

    return render(request, 'exhibitions/search_artworks.html', {'form': form, 'results':{}})

def search_fossils(request):
    if request.method == 'POST':
        form = SearchFossilForm(request.POST)

        if form.is_valid():
            results = Fossil.objects.all()

            if form.cleaned_data["name"]:
                results = results.filter(name__icontains=form.cleaned_data["name"])
            
            if form.cleaned_data["origin"]:
                results = results.filter(country_origin__icontains=form.cleaned_data["origin"])

            if form.cleaned_data["excavation_site"]:
                results = results.filter(excavation_site__icontains=form.cleaned_data["excavation_site"])

            if form.cleaned_data["discovery_year"]:
                results = results.filter(discovery_year__exact=form.cleaned_data["discovery_year"])

            if form.cleaned_data["period"]:
                results = results.filter(period__icontains=form.cleaned_data["period"])

            return render(request, 'exhibitions/search_fossils.html', {'form': form, 'results': results})
    else:
        form = SearchFossilForm()

    return render(request, 'exhibitions/search_fossils.html', {'form': form, 'results':{}})

def search_organisms(request):
    if request.method == 'POST':
        form = SearchOrganismForm(request.POST)

        if form.is_valid():
            results = Organism.objects.all()

            if form.cleaned_data["name"]:
                results = results.filter(name__icontains=form.cleaned_data["name"])

            if form.cleaned_data["scientific_name"]:
                results = results.filter(scientific_name__icontains=form.cleaned_data["scientific_name"])

            if form.cleaned_data["condition"] != '0':
                results = results.filter(condition__exact=int(form.cleaned_data["condition"]))

            return render(request, 'exhibitions/search_organisms.html', {'form': form, 'results': results})
    else:
        form = SearchOrganismForm()

    return render(request, 'exhibitions/search_organisms.html', {'form': form, 'results':{}})
