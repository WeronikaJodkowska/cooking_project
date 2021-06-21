from django.contrib import admin

from .models import *


@admin.register(DiseaseCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['list_ingredient']

    # def clean_name(self):
    #     """
    #     ensure that name is always lower case.
    #     """
    #     return self.cleaned_data['name'].lower()


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


