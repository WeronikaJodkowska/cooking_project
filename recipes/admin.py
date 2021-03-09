from django.contrib import admin

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    actions = ['make_published']

    list_display = ['name', 'slug', 'status']
    prepopulated_fields = {'slug': ('name',)}
    # actions = [make_published]

    def make_published(self, request, queryset):
        queryset.update(status='p')
    make_published.short_description = "Mark selected stories as published"
