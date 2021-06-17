from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin

from .models import RecipeCategory, Recipe, Direction, \
    MeasurementUnits, RecipeIngredients


@admin.register(RecipeCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ClassInline(admin.TabularInline):
    model = Direction


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    actions = ['make_published']
    # autocomplete_fields = ['list_ingredient', 'favourites']
    list_display = ['name', 'slug', 'status']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClassInline, RecipeIngredientsInline]
    # actions = [make_published]
    autocomplete_fields = ['category']

    def make_published(self, request, queryset):
        queryset.update(status='p')

    make_published.short_description = "Mark selected stories as published"


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['order', 'text']


@admin.register(MeasurementUnits)
class MeasurementUnitsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'long_name']


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'amount', 'unit', 'ingredient']
