from django.urls import path 
from . import views

urlpatterns  = [
    path('api/store',views.add_store,name='add_store'),
    path('api/settings/<str:token>',views.add_settings,name='add_settings'),
    path('api/fontman',views.get_settings,name='get_settings'), 
]