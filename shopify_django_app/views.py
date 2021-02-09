from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import requests
import json
from api.models import CustomFonts
import shutil
import re

def simple_upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		print(request)
		myfile = request.FILES['myfile']
		shop_url = request.POST.get('shop_url')
		store_token = request.POST.get('store_token')
		myfile.name = "".join(myfile.name.split())
<<<<<<< HEAD
		myfile.name = re.sub('[^a-zA-Z.]+', '',myfile.name)
=======
>>>>>>> 7235926782865d219df545ee8cd36ab7388c8f3f
		name, ext = os.path.splitext(myfile.name)
		#name = re.sub('[^A-Za-z0-9]+', '', name)
		if ext not in ['.ttf','.otf','.woff2','.woff']:
			messages.error(request,"Please Upload Valid Font File.")
			return redirect('/')
		try:
			my_custom_font = CustomFonts.objects.get(font_name =  name+ext )
		except CustomFonts.DoesNotExist:
			fs = FileSystemStorage(location='/home/shriCoder/shopify_django_app/media/'+shop_url+'/fonts/')
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			#get shopify theme here
			themes=shopify_call("https://"+shop_url+"/admin/api/2020-10/themes.json",store_token)
			for theme in json.loads(themes)['themes']:
				if theme['role']=='main':
					theme_id = theme['id']

			custom_font_url = {
				"asset":{
					"key":"assets/"+name+ext,
					"src":"https://www.fontman.in/media/"+shop_url+"/fonts/"+name+ext
				}
			}

			headers = {
    			# 'Accept': 'application/json',
    			"X-Shopify-Access-Token": store_token,
    			# "Content-Type": "application/json; charset=utf-8",
			}

			#save font to Shopify CDN here
			upload_status = requests.put("https://"+shop_url+"/admin/api/2021-01/themes/"+str(theme_id)+"/assets.json", json = custom_font_url, headers= headers)
			#add entry in database
			custom_font = CustomFonts(store_url=shop_url,font_name=name+""+ext,public_url = json.loads(upload_status.content)['asset']['public_url'] )
			custom_font.save()
			#delete the uploaded file
			#shutil.rmtree('media/shristorey.myshopify.com/fonts/')
		messages.info(request,"Font Uploaded Successfully")
		return redirect('/')
	request.session['file_upload'] ='failure'
	return redirect('/')

def shopify_call(url,token):
	return requests.get(url, headers={"X-Shopify-Access-Token":token}).text
def path_to_page(request,path):
	if path == 'faq':
		return render(request,"blog/faq.html")
	if path == 'privacy-policy':
		return render(request,"blog/privacy-policy.html")
	if path == 'pricing':
		return render(request,"blog/pricing.html")
	if path == 'contact-us':
		return render(request,"blog/contact-us.html")
	return HttpResponse("INvalid")