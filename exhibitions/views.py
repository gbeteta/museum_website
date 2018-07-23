from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db.models import Func, F
from django.views.decorators.cache import cache_page

from .forms import SearchArtifactsForm, SearchArtworkForm, SearchFossilForm, SearchOrganismForm
from .models import *

def index(request):
    return render(request, 'exhibitions/index.html', {})

def galleries(request):
    galleries = Gallery.objects.all()
    gallery_exhibitions = []

    for g in galleries:
        gallery_exhibitions.append((g, list(Exhibition.objects.filter(gallery=g))))

    return render(request, 'exhibitions/galleries.html', {"galleries": gallery_exhibitions})

def exhibitions(request):
    exhibitions = Exhibition.objects.all()
    exhibition_items = []

    for e in exhibitions:
        exhibition_items.append((e, list(Item.objects.filter(exhibition=e)[:10])))
    
    return render(request, 'exhibitions/exhibitions.html', {"exhibitions": exhibition_items})

def gallery(request, gallery_id):
    if Gallery.objects.filter(pk=gallery_id).exists():
        g = Gallery.objects.get(pk=gallery_id)
    else:
        raise Http404("Item not found")

    exhibitions = Exhibition.objects.filter(gallery=g)

    return render(request, 'exhibitions/gallery.html', {"gallery": g, "exhibitions": exhibitions})

@cache_page(60 * 15)
def exhibition(request, exhibition_id):
    if Exhibition.objects.filter(pk=exhibition_id).exists():
        e = Exhibition.objects.get(pk=exhibition_id)
    else:
        raise Http404("Item not found")

    items = list(Item.objects.filter(exhibition=e).order_by('name'))

    return render(request, 'exhibitions/exhibition.html', {"exhibition": e, "items": items})

@cache_page(60 * 30)
def item(request, item_id):
    if Item.objects.filter(pk=item_id).exists():
        item = Item.objects.get_subclass(pk=item_id)
    else:
        raise Http404("Item not found")

    def name_similarity(name1, name2):
        if name1 in name2 or name2 in name1:
            return 0

        diff = abs(len(name2) - len(name1))
        for i in range(min(len(name1), len(name2))):
            if name1.lower()[i] != name2.lower()[i]:
                diff += 1
        
        return diff

    suggested = []

    if isinstance(item, Artifact):
        partial_list = Artifact.objects.extra(select={'abs_diff': 'ABS(`discovery_year` - %s)',}, select_params=(item.discovery_year,)).order_by('abs_diff').exclude(pk=item.pk)[:100]
        suggested = list(map(list, zip([0 for i in range(len(partial_list))], partial_list)))
        
        for i in range(len(suggested)):
            item2 = suggested[i][1]

            name_score = name_similarity(item.name, item2.name)
            exhibition_score = 1 if item.exhibition.pk != item2.exhibition.pk else 0
            
            origin_score = 1 if item.country_origin != item2.country_origin else 0
            excavation_score = 1 if item.excavation_site != item2.excavation_site else 0
            year_score = abs(item.discovery_year - item2.discovery_year)
            condition_score = 1 if item.condition != item2.condition else 0
            material_score = 1 if item.material != item2.material else 0

            total_score = name_score + (exhibition_score * 2)
            total_score += (origin_score * 5) + (year_score // 2)
            total_score += (condition_score * 3) + (material_score * 2)
            suggested[i][0] = total_score

        suggested = list(sorted(suggested, key=lambda tup: tup[0]))[:10]

    elif isinstance(item, Organism):
        suggested = list(map(list, zip([0 for i in range(Organism.objects.all().count())], Organism.objects.all().exclude(pk__exact=item.pk))))

        for i in range(len(suggested)):
            item2 = suggested[i][1]

            name_score = name_similarity(item.name, item2.name)
            exhibition_score = 1 if item.exhibition.pk != item2.exhibition.pk else 0
            
            sci_name_score = 1 if item.sci_name_score != item2.sci_name_score else 0
            condition_score = 1 if item.condition != item2.condition else 0

            total_score = name_score + (exhibition_score * 2)
            total_score += sci_name_score + (condition_score * 2)
            suggested[i][0] = total_score

        suggested = list(sorted(suggested, key=lambda tup: tup[0]))[:10]

    elif isinstance(item, Fossil):
        partial_list = Fossil.objects.extra(select={'abs_diff': 'ABS(`discovery_year` - %s)',}, select_params=(item.discovery_year,)).order_by('abs_diff').exclude(pk=item.pk)[:100]
        suggested = list(map(list, zip([0 for i in range(len(partial_list))], partial_list)))

        for i in range(len(suggested)):
            item2 = suggested[i][1]

            name_score = name_similarity(item.name, item2.name)
            exhibition_score = 1 if item.exhibition.pk != item2.exhibition.pk else 0
            
            origin_score = 1 if item.country_origin != item2.country_origin else 0
            excavation_score = 1 if item.excavation_site != item2.excavation_site else 0
            year_score = abs(item.discovery_year - item2.discovery_year)
            period_score = 1 if item.period != item2.period else 0

            total_score = name_score + (exhibition_score * 2)
            total_score += (origin_score * 5) + (year_score // 2)
            total_score += (period_score * 10)
            suggested[i][0] = total_score

        suggested = list(sorted(suggested, key=lambda tup: tup[0]))[:10]

    elif isinstance(item, Artwork):
        partial_list = Artwork.objects.extra(select={'abs_diff': 'ABS(`year` - %s)',}, select_params=(item.year,)).order_by('abs_diff').exclude(pk=item.pk)[:100]
        suggested = list(map(list, zip([0 for i in range(len(partial_list))], partial_list)))

        for i in range(len(suggested)):
            item2 = suggested[i][1]

            name_score = name_similarity(item.name, item2.name)
            exhibition_score = 1 if item.exhibition.pk != item2.exhibition.pk else 0
            
            type_score = 1 if item.art_type != item2.art_type else 0
            author_score = 1 if item.author != item2.author else 0
            year_score = abs(item.year - item2.year)

            total_score = name_score + (exhibition_score * 2)
            total_score += (type_score * 5) + (year_score // 2)
            total_score += (author_score * 5)
            suggested[i][0] = total_score

        suggested = list(sorted(suggested, key=lambda tup: tup[0]))[:10]
    
    return render(request, "exhibitions/item.html", {"item": item, "type": item.__class__.__name__, "suggestions": suggested})

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

            return render(request, 'exhibitions/search_artifacts.html', {'form': form, 'results': results[:250]})
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

            if form.cleaned_data["art_type"]:
                results = results.filter(art_type__icontains=form.cleaned_data["art_type"])

            return render(request, 'exhibitions/search_artworks.html', {'form': form, 'results': results[:250]})
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

            return render(request, 'exhibitions/search_fossils.html', {'form': form, 'results': results[:250]})
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

            return render(request, 'exhibitions/search_organisms.html', {'form': form, 'results': results[:250]})
    else:
        form = SearchOrganismForm()

    return render(request, 'exhibitions/search_organisms.html', {'form': form, 'results':{}})
