from django.contrib import admin
from .models import *

admin.site.register(Task)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'user', 'complete', 'created_at']
