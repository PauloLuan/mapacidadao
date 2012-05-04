# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import get_model, DateField, DateTimeField
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils.safestring import mark_safe

def home(request):
    return render(request, 'home.html')