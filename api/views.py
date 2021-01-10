from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import random
from .models import Settings,Store
from .serializers import SettingsSerializer,StoreSerializer
from rest_framework.decorators import api_view

#REGISTER NEW STORE
@api_view(['POST'])
def add_store(request):
    if request.method == 'POST':
        store_data = JSONParser().parse(request)
        store_serializer = StoreSerializer(data=store_data)
        if store_serializer.is_valid():
            store_serializer.save()
            return JsonResponse(store_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ADD SETTINGS
@api_view(['PUT','POST','GET'])
def add_settings(request, token):
    if request.method == 'POST':
        settings_data = JSONParser().parse(request)
        settings_serializer = SettingsSerializer(data=settings_data)
        if settings_serializer.is_valid():
            settings_serializer.save()
            return JsonResponse(settings_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        store = Settings.objects.get(store_token=token)
        settings_data = JSONParser().parse(request) 
        settings_serializer = SettingsSerializer(store, data=settings_data) 
        if settings_serializer.is_valid(): 
            settings_serializer.save() 
            return JsonResponse(settings_serializer.data)
    return JsonResponse(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_settings(request):
    store_settings = Settings.objects.get(store_token=request.GET.get('store_token'))
    settings_serializer = SettingsSerializer(store_settings) 
    return JsonResponse(settings_serializer.data)