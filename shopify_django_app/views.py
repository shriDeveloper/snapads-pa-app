from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		print(request)
		myfile = request.FILES['myfile']
		shop_url = request.POST.get('shop_url')
		name, ext = os.path.splitext(myfile.name)
		#check extension here
		print("EXTENSION IS "+ext)
		fs = FileSystemStorage(location='media/'+shop_url+'/fonts/')
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return render(request,'home/index.html',{'error':'Great'})
	return render(request, 'home/index.html',{'error':'nope'})