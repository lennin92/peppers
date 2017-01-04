from django.contrib import admin

from rest.models import Clasificacion


class ClasificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'etiqueta', 'descripcion')

admin.site.register(Clasificacion, ClasificacionAdmin)