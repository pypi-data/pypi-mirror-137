from re import search
from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp.models import Model
from faabrickmap_data.models import Societe

class SocieteAdmin(DjangoLDPAdmin):
    list_display=('name', 'activity')
    search_fields=['name']

admin.site.register(Societe, SocieteAdmin)