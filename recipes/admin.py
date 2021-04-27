from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin

from .models import Category, Recipe, Direction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ClassInline(admin.TabularInline):
    model = Direction


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    actions = ['make_published']
    autocomplete_fields = ['list_ingredient', 'favourites']
    list_display = ['name', 'slug', 'status']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClassInline, ]
    # actions = [make_published]

    def make_published(self, request, queryset):
        queryset.update(status='p')

    make_published.short_description = "Mark selected stories as published"


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['text']
