from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from .models import Modele, Variante, Version
from .forms import ModeleForm, VarianteForm, VersionForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict

def modele_list(request):
    modeles = Modele.objects.all().prefetch_related('tags')
    form = ModeleForm()
    for modele in modeles:
        modele.edit_form = ModeleForm(instance=modele)
    return render(request, 'modele_list.html', {'modeles': modeles, 'form': form})

def add_modele(request):
    if request.method == 'POST':
        form = ModeleForm(request.POST, request.FILES)
        if form.is_valid():
            modele = form.save()
            variante = Variante.objects.create(
                name='Variante 1.0',
                description='Description de la variante 1.0',
                modele=modele,
            )
            version = Version.objects.create(
                name='Version 1.0',
                description='Description de la version 1.0',
                variante=variante,
            )
            if 'files' in request.FILES:
                version.file = request.FILES['files']
                version.save()
            return redirect('modele_list')
    else:
        form = ModeleForm()
    return render(request, 'add_modele.html', {'form': form})

def edit_modele(request, uuid):
    modele = get_object_or_404(Modele, uuid=uuid)
    if request.method == 'POST':
        form = ModeleForm(request.POST, request.FILES, instance=modele)
        if form.is_valid():
            form.save()
            return redirect('modele_list')
    else:
        form = ModeleForm(instance=modele)
    return render(request, 'edit_modele.html', {'form': form})

def modele_detail(request, modele_uuid):
    modele = get_object_or_404(Modele, uuid=modele_uuid)
    form = VarianteForm() 
    return render(request, 'modele_detail.html', {'modele': modele, 'form': form})

@transaction.atomic
def add_variante(request, modele_uuid):
    modele = get_object_or_404(Modele, uuid=modele_uuid)
    if request.method == 'POST':
        form = VarianteForm(request.POST, request.FILES)
        if form.is_valid():
            variante = form.save(commit=False)
            variante.modele = modele
            variante.save()  
            
            version = Version.objects.create(
                name='Version 1.0',
                description='Description de la version 1.0',
                variante=variante,
            )
            if 'files' in request.FILES:
                version.file = request.FILES['files']
                version.save()
                
            return redirect('modele_tree', modele_uuid=modele_uuid)
    else: 
        form = VarianteForm()
    return render(request, 'add_variante.html', {'form': form, 'modele': modele})

def variante_detail(request, variante_uuid):
    variante = get_object_or_404(Variante, uuid=variante_uuid)
    form = VersionForm() 
    return render(request, 'variante_detail.html', {'variante': variante, 'form': form})

@transaction.atomic
def add_version(request, variante_uuid):
    variante = get_object_or_404(Variante, uuid=variante_uuid)
    modele_uuid = variante.modele.uuid 

    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES)
        if form.is_valid():
            version = form.save(commit=False)
            version.variante = variante

            if 'file' in request.FILES:
                version.file = request.FILES['file']
            
            version.save()
            return redirect('modele_tree', modele_uuid=modele_uuid)
    else:
        form = VersionForm()

    return render(request, 'modele_tree.html', {'form': form, 'variante': variante})

def version_detail(request, version_uuid):
    version = get_object_or_404(Version, uuid=version_uuid)
    return render(request, 'version_detail.html', {'version': version})


def delete_modele(request, modele_uuid):
    modele = get_object_or_404(Modele, uuid=modele_uuid)
    modele.delete()
    return redirect('modele_list')

def delete_variante(request, variante_uuid):
    variante = get_object_or_404(Variante, uuid=variante_uuid)
    variante.delete()
    return JsonResponse({'status': 'success'})

def delete_version(request, version_uuid):
    version = get_object_or_404(Version, uuid=version_uuid)
    version.delete()
    return JsonResponse({'status': 'success'})


def index(request):
    return HttpResponse("Hello, here we go again")

def edit_variante_data(request, variante_uuid):
    variante = get_object_or_404(Variante, uuid=variante_uuid)
    if request.method == 'GET':
        image_url = variante.image.url if variante.image and hasattr(variante.image, 'url') else None
        variante_data = {
            'name': variante.name,
            'description': variante.description,
            'image_url': image_url,
        }
        return JsonResponse(variante_data)
    
def edit_variante(request, variante_uuid):
    variante = get_object_or_404(Modele, uuid=variante_uuid)
    if request.method == 'POST':
        form = VarianteForm(request.POST, request.FILES, instance=variante)
        if form.is_valid():
            form.save()
            return redirect('modele_list')
    else:
        form = ModeleForm(instance=variante)
    return render(request, 'edit_variante.html', {'form': form})
    
def edit_version_data(request, version_uuid):
    version = get_object_or_404(Version, uuid=version_uuid)
    if request.method == 'GET':
        image_url = version.image.url if version.image and hasattr(version.image, 'url') else None
        version_data = {
            'name': version.name,
            'description': version.description,
            'image_url': image_url, 
        }
        return JsonResponse(version_data)

def modele_tree(request, modele_uuid):
    modele_instance = get_object_or_404(Modele, uuid=modele_uuid)
    variantes = Variante.objects.filter(modele=modele_instance).prefetch_related('versions')
    version_form = VersionForm()
    context = {
        'modele': modele_instance,
        'variantes': variantes,
        'form': version_form,
    }
    return render(request, 'modele_tree.html', context)

def version_data(request, version_uuid):
    version = get_object_or_404(Version, uuid=version_uuid)
    data = {
        'name': version.name,
        'description': version.description,
        'created_at': version.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
    }
    return JsonResponse(data)

def toggle_favorite(request, version_uuid):
    if request.method == 'POST':
        with transaction.atomic():
            version_to_favorite = get_object_or_404(Version, uuid=version_uuid)          
            modele_associated = version_to_favorite.variante.modele            
            Version.objects.filter(variante__modele=modele_associated, is_favorite=True).update(is_favorite=False)
            version_to_favorite.is_favorite = not version_to_favorite.is_favorite
            version_to_favorite.save()

        return JsonResponse({'success': True, 'is_favorite': version_to_favorite.is_favorite})