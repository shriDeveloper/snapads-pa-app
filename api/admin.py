from django.contrib import admin
from .models import Settings,Store,CustomFonts,CustomClass

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'upgrade_status','charge_id')

# Register your models here.
admin.site.register(Settings)
admin.site.register(Store , StoreAdmin)
admin.site.register(CustomFonts)
admin.site.register(CustomClass)