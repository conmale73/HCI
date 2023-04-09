from django.contrib import admin
from .models import Postnew

# Register your models here.
class PostnewAdmin(admin.ModelAdmin):
    list_display = ('postname', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields={'slug': ('postname',)}

admin.site.register(Postnew, PostnewAdmin)