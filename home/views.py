from django.shortcuts import render
import shopify
from shopify_app.decorators import shop_login_required

from api.views import Store,Settings
from uuid import uuid4
import requests
import json
from api.models import CustomFonts 

@shop_login_required
def index(request):
	shop_url = "https://"+request.session['shopify']['shop_url']
	token = request.session['shopify']['access_token']
	store_token = rand_token = uuid4()
	try:
		store = Store.objects.get(name=request.session['shopify']['shop_url'])
		store_token = store.token
	except Store.DoesNotExist:

		#SET BILLING HERE
		session = shopify.Session(shop_url, token)
		shopify.ShopifyResource.activate_session(session)
		charge = shopify.RecurringApplicationCharge()
		charge.test = True
        charge.return_url = 'https://shriCoder.pythonanywhere.com'
        charge.price = 10.00
        charge.name = "Custom Plan"

		if charge.save():
			print charge.attributes 

		#INIIAL SETUP FOR APP
		store = Store(name = request.session['shopify']['shop_url'] , token = store_token)
		settings = Settings(store_token = store_token)
		store.save()
		settings.save()

		### CONFIGURE JS HERE ####
		res = shopify.ScriptTag(dict(event='onload', src='https://shricoder.pythonanywhere.com/static/js/fontman.js')).save()
		########################## ENDS HERE ##################################################################
	file_upload = request.session.get('file_upload')
	#load fonts here
	store_fonts = CustomFonts.objects.filter(store_url = request.session['shopify']['shop_url'] )
	print(store_fonts)
	request.session['file_upload']='' #reset session here
	return render(request, 'home/index.html',{'store_token':token,'store_url':shop_url,'app_token':store_token,'shop_url':request.session['shopify']['shop_url'],'file_status':file_upload,'store_fonts':store_fonts})

def shopify_call(url,token):
	return requests.get(url, headers={"X-Shopify-Access-Token":token}).text
