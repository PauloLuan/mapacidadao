from django.contrib.gis import admin
from servico.models import Ponto, PontoCategoria, PontoStatus


admin.site.register(PontoCategoria)
admin.site.register(PontoStatus)
admin.site.register(Ponto, admin.OSMGeoAdmin )

