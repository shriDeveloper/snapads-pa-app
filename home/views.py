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
		

		print(themes)
		#theme settings
		assets = shopify_call(shop_url+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=layout/theme.liquid",token)
		assets = json.loads(assets)['asset']['value']
		snippet = "{% include 'fontmancss' %}"
		head_tag = "</head>"
		
		fontman_api = snippet+head_tag
		
		if fontman_api not in assets:
			theme_liquid = assets.replace(head_tag,fontman_api)
			asset = shopify.Asset()
			asset.key = "layout/theme.liquid"
			asset.value = theme_liquid
			success = asset.save()
			print("Asset Added")

		fontman_css = ''
		snippet = shopify.Asset()
		snippet.key = "snippets/fontmancss.liquid"
		snippet.value = fontman_css
		success = snippet.save()
		print("Assets saved Liqued")
		
		########################## ENDS HERE ##################################################################
	file_upload = request.session.get('file_upload')
	#load fonts here
	store_fonts = CustomFonts.objects.filter(store_url = request.session['shopify']['shop_url'] )
	print(store_fonts)
	request.session['file_upload']='' #reset session here
	return render(request, 'home/index.html',{'store_token':token,'store_url':shop_url,'app_token':store_token,'shop_url':request.session['shopify']['shop_url'],'file_status':file_upload,'store_fonts':store_fonts})

def shopify_call(url,token):
	return requests.get(url, headers={"X-Shopify-Access-Token":token}).text
