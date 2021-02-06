from django.shortcuts import render,redirect
import shopify
from shopify_app.decorators import shop_login_required
from django.http import HttpResponse
from api.views import Store,Settings
from uuid import uuid4
import requests
import json
from api.models import CustomFonts,CustomClass
from django.contrib import messages

@shop_login_required
def index(request):
	shop_url = "https://"+request.session['shopify']['shop_url']
	ACTIVE_FLAG = 'INACTIVE'
	token = request.session['shopify']['access_token']
	store_token = rand_token = uuid4()
	try:
		store = Store.objects.get(name=request.session['shopify']['shop_url'])
		store_token = store.token
	except Store.DoesNotExist:

		#GET OWNERS EMAIL HERE
		response = shopify_call(shop_url+'/admin/api/2021-01/shop.json',token)
		email = json.loads(response)['shop']['email']

		#INIIAL SETUP FOR APP
		store = Store(name = request.session['shopify']['shop_url'] , token = store_token , email = email )
		settings = Settings(store_token = store_token)
		store.save()
		settings.save()

		postData = {
			"webhook":{
				"topic":"app/uninstalled",
				"address":"https://www.fontman.in/uninstall",
				"format":"json"
			}
		}

		#subscribe to web hook here
		webhook = requests.post(shop_url+"/admin/api/2021-01/webhooks.json", json = postData ,   headers = {"X-Shopify-Access-Token":token})
		print("WEBHOOK STATUS"+str(webhook.content))
		########################## ENDS HERE ##################################################################
	file_upload = request.session.get('file_upload')
	#load fonts here
	store_fonts = CustomFonts.objects.filter(store_url = request.session['shopify']['shop_url'] )
	custom_elements = CustomClass.objects.filter(store_token = store_token )
	print(store_fonts)
	if store.upgrade_status == 'active':
		ACTIVE_FLAG = 'ACTIVE'
	request.session['file_upload']='' #reset session here
	return render(request, 'home/index.html',{'store_token':token,'store_url':shop_url,'app_token':store_token,'shop_url':request.session['shopify']['shop_url'],'file_status':file_upload,'store_fonts':store_fonts,'active_flag':ACTIVE_FLAG,'custom_elements':custom_elements})

def shopify_call(url,token):
	return requests.get(url, headers={"X-Shopify-Access-Token":token}).text

@shop_login_required
def confirm(request,token):
	payment_json = ''
	rac = shopify.RecurringApplicationCharge()
	rac.name          = "FontMan Premium"
	rac.test = True
	rac.price         = 9.99
	rac.return_url    = "https://www.fontman.in/activate_charge?store_token="+token
	#rac.capped_amount = 12
	rac.terms         = "Upgrade To add Unlimited Custom Fonts To Your Shopify Store. "
	if rac.save():
		payment_json = json.loads(json.dumps(rac.attributes))
	print("PAYMENT")
	return redirect(''+payment_json['confirmation_url'])
	print(payment_json)

@shop_login_required
def activate_charge(request, *args, **kwargs):
	# After confirmation...
	charge_id = request.GET.get('charge_id')
	store_token = request.GET.get('store_token')
	rac = shopify.RecurringApplicationCharge.find(charge_id)
	rac.activate()
	Store.objects.filter(token = store_token ).update(charge_id = charge_id,upgrade_status = 'active')
	### CONFIGURE JS HERE ####
	res = shopify.ScriptTag(dict(event='onload', src='https://www.fontman.in/static/js/fontman.js')).save()
	print("Script STATUS")
	print(res)
	messages.success(request, 'Your Account Has Been Upgraded.')
	return redirect('/')

@shop_login_required
def cancel_charge(request,token):
	charge = shopify.RecurringApplicationCharge.current()
	if charge == None:
		messages.success(request, 'No Plan To Cancel.')
		#set it as inactive if there is no active plan
		Store.objects.filter(token = token ).update(charge_id = '', upgrade_status = 'inactive')
		return redirect("/")
	charge.destroy()
	if shopify.RecurringApplicationCharge.current() == None:
		Store.objects.filter(token = token ).update(charge_id = '', upgrade_status = 'inactive')
	else:
		Store.objects.filter(token = token ).update(upgrade_status = 'active')
	messages.success(request, 'Your Account Has Been Downgraded.')

	font_types = ['.woff','.woff2','.ttf','.otf']
	#reset custom elements here
	asset = shopify.Asset()
	asset.key = "snippets/fontmancustomcss.liquid"
	asset.value = ""
	success = asset.save()

	# #get store_url first
	store = Store.objects.get(token = token )
	#delete all custom fonts
	CustomFonts.objects.filter(store_url = store.name).delete()
	CustomClass.objects.filter(store_token = store.token).delete()



	request_data = {}
	#do eveything to reset custom-fonts , custom-classes and all to here. (make sure its not free)
	store_settings  = Settings.objects.get(store_token = token )
	if isCustomMan(store_settings.body_tag):
		request_data['body_tag'] = ''
	if isCustomMan(store_settings.h1_tag):
		request_data['h1_tag'] = ''
	if isCustomMan(store_settings.h2_tag):
		request_data['h2_tag'] = ''
	if isCustomMan(store_settings.h3_tag):
		request_data['h3_tag'] = ''
	if isCustomMan(store_settings.h4_tag):
		request_data['h4_tag'] = ''
	if isCustomMan(store_settings.h5_tag):
		request_data['h5_tag'] = ''
	if isCustomMan(store_settings.h6_tag):
		request_data['h6_tag'] = ''
	if isCustomMan(store_settings.p_tag):
		request_data['p_tag'] = ''
	if isCustomMan(store_settings.li_tag):
		request_data['li_tag'] = ''
	if isCustomMan(store_settings.a_tag):
		request_data['a_tag'] = ''
	if isCustomMan(store_settings.block_tag):
		request_data['block_tag'] = ''

	#after redirect you have to submit save button()

	response = requests.put("https://www.fontman.in/api/settings/"+token,data = json.dumps(request_data))

	return redirect("/")

@shop_login_required
def store_reset(request,token):
	#reset everything (both liquid files)
	asset = shopify.Asset()
	asset.key = "snippets/fontmangooglecss.liquid"
	asset.value = ""
	success = asset.save()

	asset = shopify.Asset()
	asset.key = "snippets/fontmancustomcss.liquid"
	asset.value = ""
	success = asset.save()
	CustomClass.objects.filter(store_token = token).delete()


	request_data = {
         "body_tag": '',
         "h1_tag": '',
         "h2_tag": '',
         "h3_tag": '',
         "h4_tag": '',
         "h5_tag": '',
         "h6_tag": '',
         "p_tag": '',
         "li_tag": '',
         "a_tag": '',
         "block_tag": '',
		 'custom_classes':'',
         'custom_font':'',
       }

	#post api a empty data (for reset)
	response = requests.put("https://www.fontman.in/api/settings/"+token,data = json.dumps(request_data))
	messages.success(request, 'Your Shopify Store Has Been Restored.')
	print(response.text)

	return redirect('/')

def isCustomMan(font):
	extension = ['.woff','.woff2','.ttf','.otf']
	if font!=None:
		return list(filter(font.endswith, extension)) != []
	return False

def blog(request):
	return render(request, 'landing/index.html')