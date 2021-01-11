from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('shopify/', include('shopify_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('',include('api.urls')),
    path('',include('shopify_app.urls'))
]
