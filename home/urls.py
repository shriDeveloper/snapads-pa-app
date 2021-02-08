from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='root_path'),
    path('blog/',views.blog,name='blog_path'),
    path('confirm_payment/<str:token>',views.confirm,name='confirm_payment'),
    path('activate_charge',views.activate_charge,name='activate_charge'),
    path('cancel_charge/<str:token>',views.cancel_charge,name='cancel_charge'),
    path('reset/<str:token>',views.store_reset,name='store_reset'),
]
