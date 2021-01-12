from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('shopify/', include('shopify_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('',include('api.urls')),
    path('',include('shopify_app.urls')),
    path('font_upload/',views.simple_upload,name='font_upload'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
