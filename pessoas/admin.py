from django.contrib import admin

from .models import Pessoa

class ListandoPessoas(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
        'email'
    )
    list_display_links = (
        'id',
        'nome',
        'email'
    )
    search_fields = (
        'nome',
        'email'
    )
    list_per_page = 10

admin.site.register(Pessoa, ListandoPessoas)

