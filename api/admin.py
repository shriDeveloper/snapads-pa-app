from django.contrib import admin
from .models import Settings,Store,CustomFonts,CustomClass

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'upgrade_status','charge_id','review')

class CustomFontsAdmin(admin.ModelAdmin):
    list_display = ('store_url', 'font_name', 'public_url')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('store_token', 'h1_tag', 'h2_tag','h3_tag','h4_tag','h5_tag','h6_tag','body_tag','p_tag','block_tag','li_tag','a_tag')
# Register your models here.
admin.site.register(Settings ,SettingsAdmin)
admin.site.register(Store , StoreAdmin)
admin.site.register(CustomFonts, CustomFontsAdmin)
admin.site.register(CustomClass)