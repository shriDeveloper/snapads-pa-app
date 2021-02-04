from django.contrib import admin
from .models import Settings,Store,CustomFonts,CustomClass

# Register your models here.
admin.site.register(Settings)
admin.site.register(Store)
admin.site.register(CustomFonts)
admin.site.register(CustomClass)