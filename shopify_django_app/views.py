from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from api.models import CustomFonts

def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		print(request)
		myfile = request.FILES['myfile']
		shop_url = request.POST.get('shop_url')
		name, ext = os.path.splitext(myfile.name)
		#check extension here
		print("EXTENSION IS "+ext)
		print("NAME IS "+name)
		fs = FileSystemStorage(location='media/'+shop_url+'/fonts/')
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		request.session['file_upload'] ='success'
		#add entry in database
		custom_font = CustomFonts(store_url=shop_url,font_name=name+""+ext)
		custom_font.save()
		return redirect('/')
	request.session['file_upload'] ='failure'
	return redirect('/')
