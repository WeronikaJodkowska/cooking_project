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


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

    # fields = ('get_ingredients_by_disease', 'id', 'user', 'disease', 'self_ingredients')

    # def get_ingredients_by_disease(self, obj):
    #     return "\n".join([p.list_ingredient for p in obj.Disease.all()])


