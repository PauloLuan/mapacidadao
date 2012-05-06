# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.files import File

from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.safestring import mark_safe

from django.contrib.gis.shortcuts import render_to_kml

from servico.models import Ponto

def kml(request, categoria=None, object_id=None):
    ''' carrega pontos '''
    
    if categoria:
        pontos = Ponto.objects.all()
    else:
        pontos = Ponto.objects.all()
    markers = pontos

    

    markers = [{'id':mrk.id,
                 'name': mrk.titulo, 
                 'description': mrk.descricao,
                 'kml': mrk.ponto and mrk.ponto.kml or '',
                 'categoria':mrk.categoria,
                 'icon_name':mrk.categoria.icon} for mrk in markers]
    
    return render_to_kml("placemarks.kml", {'places' : markers})

def kml_detail(request, object_id=None):
    ''' carrega pontos '''
    
    ponto = get_object_or_404(Ponto, pk=object_id)
    markers = ponto

    

    markers = [{'id':mrk.id,
                 'name': mrk.titulo, 
                 'description': mrk.descricao, 
                 'categoria':mrk.categoria,
                 'icon_name':mrk.categoria.icon_name} for mrk in markers]
    
    return render_to_kml("placemarks.kml", {'places' : markers})