# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.files import File

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe

from django.contrib.gis.shortcuts import render_to_kml

from servico.models import Ponto
from servico.forms import PontoFileForm



def ponto_crud(request, ponto_id=None):
    form = PontoFileForm(request.POST or None, request.FILES or None,instance = None, user=request.user)
    if request.method == "POST":
        if form.is_valid():

            ponto = form.save ()
        else:
            print form.errors


    return render_to_response('ponto_form.html', 
        {'form':form}, 
       context_instance=RequestContext(request)
       )


def kml(request, queryset=None):
    ''' carrega pontos '''

    print "has key query===== %s " % (request.GET.has_key('query'));
    if request.GET.has_key('query'):
        print request.GET['query']

    print "has key ===== %s " % (request.GET.has_key('categoria'));
    if request.GET.has_key('categoria'):
        categoria = request.GET['categoria']


        markers = Ponto.objects.filter(categoria=categoria)
        print "-------------------"
    else:
        markers = Ponto.objects.all()

    markers = [{'id':mrk.id,
                 'name': mrk.titulo, 
                 'description': mrk.logradouro  ,
                 'telefone': mrk.telefone or "",
                 'site': mrk.site or "",
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
                 'description': "--xxxx---",
                 'categoria':mrk.categoria,
                 'icon_name':mrk.categoria.icon_name} for mrk in markers]
    
    return render_to_kml("placemarks.kml", {'places' : markers})


