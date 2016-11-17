
from django.conf.urls import url
from rest.views import clasificacion_list, clasificacion_detail, sugerencia_detail, correccion_create

rest_urls = [
    url(r'^clasificacion/$', clasificacion_list, name='clasificacion_list'),
    url(r'^clasificacion/(?P<pk>[0-9]+)/$', 
		clasificacion_detail, name='clasificacion_detail'),
    url(r'^estudio/(?P<pk>[0-9.,_\ ]*)/sugerencia/$', 
		sugerencia_detail, name='sugerencia_detail'),
    url(r'^correccion/$', correccion_create, name='correccion_create'),
]
