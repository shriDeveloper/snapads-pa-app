from django.shortcuts import render
import shopify
from shopify_app.decorators import shop_login_required

from api.views import Store,Settings
from uuid import uuid4
import requests
import json

@shop_login_required
def index(request):
	shop_url = "https://"+request.session['shopify']['shop_url']
	token = request.session['shopify']['access_token']
	store_token = rand_token = uuid4()
	try:
		store = Store.objects.get(name=request.session['shopify']['shop_url'])
	except Store.DoesNotExist:
		#INIIAL SETUP FOR APP
		store = Store(name = request.session['shopify']['shop_url'] , token = store_token)
		settings = Settings(store_token = store_token)
		store.save()
		settings.save()
		
		############################### THEME MODIFICATION CODE HERE #########################################
		themes=shopify_call(shop_url+"/admin/api/2020-10/themes.json",token)
		for theme in json.loads(themes)['themes']:
			if theme['role']=='main':
				theme_id = theme['id']
		
		#theme settings
		assets = shopify_call(shop_url+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=layout/theme.liquid",token)
		assets = json.loads(assets)['asset']['value']
		snippet = "{% include 'fontmanjs' %}"
		body_tag = "</body>"
		
		fontman_api = snippet+body_tag
		
		if fontman_api not in assets:
			theme_liquid = assets.replace(body_tag,fontman_api)
			asset = shopify.Asset()
			asset.key = "layout/theme.liquid"
			asset.value = theme_liquid
			success = asset.save()

		fontman_js = '<script type="text/javascript" src="http://localhost:8000/static/js/fontman.js"></script><script type="text/javascript">loadFontMan("'+str(store_token)+'");</script>'
		snippet = shopify.Asset()
		asset.key = "snippets/fontmanjs.liquid"
		asset.value = fontman_js
		success = asset.save()
		
		########################## ENDS HERE ##################################################################
	return render(request, 'home/index.html',{'store_token':store.token})

def shopify_call(url,token):
	return requests.get(url, headers={"X-Shopify-Access-Token":token}).text
