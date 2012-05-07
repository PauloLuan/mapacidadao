# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.gis.db import models
#from sorl.thumbnail.fields import ImageWithThumbnailsField, ThumbnailField

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import dateformat

import time
import os
import re


class PontoStatus(models.Model):
    """docstring for PontoStatus"""
    nome = models.CharField(u'status', max_length=50)
    descricao = models.CharField(u'descricao', max_length=50)

class PontoCategoria(models.Model):
    nome = models.CharField(u'nome',max_length=20)
    descricao = models.CharField(u'descrição',max_length=200)
    icon = models.FileField(upload_to='categoria_icons', blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % ( self.nome.capitalize())
    
   

class Ponto(models.Model):
    
    categoria = models.ForeignKey(PontoCategoria, blank=True, null=True)
    titulo = models.CharField(u'título', max_length=120, blank=True, null=True)
    descricao = models.TextField(u'descrição', blank=True, null=True)
    status =  models.ForeignKey(PontoStatus, blank=True, null=True)
    ponto = models.PointField(u'ponto', srid=900913, null=True, blank=True)

    telefone = models.CharField( max_length=50, null=True, blank=True)
    site = models.URLField( null=True, blank=True)

    logradouro = models.CharField(u'logradouro', max_length=200, blank=True, null=True)
    numero = models.CharField(u'número', max_length=15, blank=True, null=True)
    complemento = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=70, blank=True, null=True)
    cep = models.CharField(u'CEP', max_length=12, blank=True, null=True)
    #municipio = models.ForeignKey(Municipio, verbose_name=u'UF - Município', blank=True, null=True)
    municipio = models.CharField(max_length=70, blank=True, null=True)


    #dados do geocode json
    route = models.CharField(u'logradouro', max_length=200, blank=True, null=True)
    street_number = models.CharField(u'número', max_length=15, blank=True, null=True)
    sublocality = models.CharField(max_length=70, blank=True, null=True)
    postal_code = models.CharField(u'CEP', max_length=12, blank=True, null=True)
    #municipio = models.ForeignKey(Municipio, verbose_name=u'UF - Município', blank=True, null=True)
    locality = models.CharField(max_length=70, blank=True, null=True)
    administrative_area_level_1 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    formatted_address = models.CharField(max_length=250, blank=True, null=True)

    objects = models.GeoManager()


    @models.permalink
    def get_absolute_url(self):
        return ('ponto-detail', [str(self.id)])
    
    def __unicode__(self):
        return self.titulo


