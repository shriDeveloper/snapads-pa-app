from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.template import RequestContext
from django.apps import apps
import hmac, base64, hashlib, binascii, os
import shopify
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from datetime import datetime


from api.models import Store,CustomFonts,Settings

from home.views import shopify_call

import requests

def _new_session(shop_url):
    api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION
    return shopify.Session(shop_url, api_version)

# Ask user for their ${shop}.myshopify.com address
def login(request):
    # If the ${shop}.myshopify.com address is already provided in the URL,
    # just skip to authenticate
    if request.GET.get('shop'):
        return authenticate(request)
    return render(request, 'shopify_app/login.html', {})

def authenticate(request):
    shop_url = request.GET.get('shop', request.POST.get('shop')).strip()
    if not shop_url:
        messages.error(request, "A shop param is required")
        return redirect(reverse(login))
    scope = apps.get_app_config('shopify_app').SHOPIFY_API_SCOPE
    redirect_uri = request.build_absolute_uri(reverse(finalize))
    print("FINALIZE IS HERE")
    print(redirect_uri)
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    request.session['shopify_oauth_state_param'] = state
    permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
    return redirect(permission_url)

def finalize(request):
    api_secret = apps.get_app_config('shopify_app').SHOPIFY_API_SECRET
    params = request.GET.dict()
    if request.session['shopify_oauth_state_param'] != params['state']:
        messages.error(request, 'Anti-forgery state token does not match the initial request.')
        return redirect(reverse(login))
    else:
        request.session.pop('shopify_oauth_state_param', None)

    myhmac = params.pop('hmac')
    line = '&'.join([
        '%s=%s' % (key, value)
        for key, value in sorted(params.items())
    ])
    h = hmac.new(api_secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
    if hmac.compare_digest(h.hexdigest(), myhmac) == False:
        messages.error(request, "Could not verify a secure login")
        return redirect(reverse(login))

    try:
        shop_url = params['shop']
        session = _new_session(shop_url)
        request.session['shopify'] = {
            "shop_url": shop_url,
            "access_token": session.request_token(request.GET)
        }
    except Exception:
        messages.error(request, "Could not log in to Shopify store.")
        return redirect(reverse(login))
    messages.info(request, "Logged in to shopify store.")
    request.session.pop('return_to', None)
    return redirect(request.session.get('return_to', reverse('root_path')))

def logout(request):
    request.session.pop('shopify', None)
    messages.info(request, "Successfully logged out.")
    return redirect(reverse(login))

@csrf_exempt
def submit(request):
    API_URL = 'https://www.fontman.in'
    if request.method == "POST":
        font_data = request.POST.get('font_data')
        store_data = request.POST.get('store_data')

        font_json = json.loads(font_data)
        store_json = json.loads(store_data)

        themes=shopify_call(store_json['store_url']+"/admin/api/2020-10/themes.json",store_json['store_token'])
        print(themes)
        for theme in json.loads(themes)['themes']:
            if theme['role']=='main':
                theme_id = theme['id']


        assets = shopify_call(store_json['store_url']+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=layout/theme.liquid",store_json['store_token'])
        assets = json.loads(assets)['asset']['value']

        #theme settings
        snippet = "{% include 'fontmangooglecss' %}"
        head_tag = "</head>"

        fontman_api = snippet+head_tag

        if snippet not in assets:
            theme_liquid = assets.replace(head_tag,fontman_api)
            asset = shopify.Asset()
            asset.key = "layout/theme.liquid"
            asset.value = theme_liquid
            success = asset.save()

        fontman_css = ''
        snippet = shopify.Asset()
        snippet.key = "snippets/fontmangooglecss.liquid"
        snippet.value = fontman_css
        success = snippet.save()

        #theme settings
        assets = shopify_call(store_json['store_url']+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=snippets/fontmangooglecss.liquid",store_json['store_token'])
        assets = json.loads(assets)['asset']['value']

        #improved algorithm

        #settings for google fonts
        google_fonts = set()
        custom_fonts = set()

        font_link = ""
        fontman_css = '<style type="text/css" id="fontmangoogle_css">'
        if font_json['body_tag'] != "":
            fontman_css = fontman_css + 'body,span,h1,h2,h3,h4,h5,h6,blockquote,div,p,a,li{font-family:\''+fontmanFamily(font_json['body_tag'])+'\' !important;}'
            if isCustomFont(font_json['body_tag']):
                custom_fonts.add(font_json['body_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['body_tag']))
        if font_json['h1_tag'] != "":
            fontman_css = fontman_css + 'h1{font-family:\''+fontmanFamily(font_json['h1_tag'])+'\' !important;}'
            if isCustomFont(font_json['h1_tag']):
                custom_fonts.add(font_json['h1_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h1_tag']))
        if font_json['h2_tag'] != "":
            fontman_css = fontman_css + 'h2{font-family:\''+fontmanFamily(font_json['h2_tag'])+'\' !important;}'
            if isCustomFont(font_json['h2_tag']):
                custom_fonts.add(font_json['h2_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h2_tag']))
        if font_json['h3_tag'] != "":
            fontman_css = fontman_css + 'h3{font-family:\''+fontmanFamily(font_json['h3_tag'])+'\' !important;}'
            if isCustomFont(font_json['h3_tag']):
                custom_fonts.add(font_json['h3_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h3_tag']))
        if font_json['h4_tag'] != "":
            fontman_css = fontman_css + 'h4{font-family:\''+fontmanFamily(font_json['h4_tag'])+'\' !important;}'
            if isCustomFont(font_json['h4_tag']):
                custom_fonts.add(font_json['h4_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h4_tag']))
        if font_json['h5_tag'] != "":
            fontman_css = fontman_css + 'h5{font-family:\''+fontmanFamily(font_json['h5_tag'])+'\' !important;}'
            if isCustomFont(font_json['h5_tag']):
                custom_fonts.add(font_json['h5_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h5_tag']))
        if font_json['h6_tag'] != "":
            fontman_css = fontman_css + 'h6{font-family:\''+fontmanFamily(font_json['h6_tag'])+'\' !important;}'
            if isCustomFont(font_json['h6_tag']):
                custom_fonts.add(font_json['h6_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['h6_tag']))
        if font_json['p_tag'] != "":
            fontman_css = fontman_css + 'p{font-family:\''+fontmanFamily(font_json['p_tag'])+'\' !important;}'
            if isCustomFont(font_json['p_tag']):
                custom_fonts.add(font_json['p_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['p_tag']))
        if font_json['block_tag'] != "":
            fontman_css = fontman_css + 'blockquote{font-family:\''+fontmanFamily(font_json['block_tag'])+'\' !important;}'
            if isCustomFont(font_json['block_tag']):
                custom_fonts.add(font_json['block_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['block_tag']))
        if font_json['li_tag'] != "":
            fontman_css = fontman_css + 'li{font-family:\''+fontmanFamily(font_json['li_tag'])+'\' !important;}'
            if isCustomFont(font_json['li_tag']):
                custom_fonts.add(font_json['li_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['li_tag']))
        if font_json['a_tag'] != "":
            fontman_css = fontman_css + 'a{font-family:\''+fontmanFamily(font_json['a_tag'])+'\' !important;}'
            if isCustomFont(font_json['a_tag']):
                custom_fonts.add(font_json['a_tag'])
            else:
                google_fonts.add(slugifyFont(font_json['a_tag']))
        fontman_css = fontman_css + "</style>"

        #construct google font links
        for my_google_font in google_fonts:
            font_link = font_link + "<link rel='stylesheet' href='//fonts.googleapis.com/css?family="+my_google_font+"'/>"
        #construct custom fonts link
        for my_custom_font in custom_fonts:
            font_link = font_link + "<style>@font-face{ font-family: '"+fontmanFamily(my_custom_font)+"'; src: url("+getCustomFontURL(my_custom_font)+") format('"+getFontType(my_custom_font)+"');}</style>"

        markup = font_link + fontman_css

        snippet = shopify.Asset()
        snippet.key = "snippets/fontmangooglecss.liquid"
        snippet.value = markup
        success = snippet.save()

        #finally update db
        response = requests.put("https://www.fontman.in/api/settings/"+font_json['store_token'],data = font_data)
        print("RESPONSE IS HERE")
        print(response.text)

        #ends here
        return HttpResponse(response.text)
        #return JsonResponse({},safe=False)
    return JsonResponse({},safe=False)

@csrf_exempt
def csubmit(request):
    API_URL = 'https://www.fontman.in/api/settings/'
    if request.method == "POST":
        custom_css = '<style type="text/css" id="fontmancustom_css">'
        custom_data = request.POST.get('custom_data')
        custom_json = json.loads(custom_data)
        custom_classes = custom_json['custom_classes']
        custom_ele_font = custom_json['custom_font']
        store_url = custom_json['store_url']
        store_token = custom_json['store_key']

        #check what font it is
        if isCustomFont(custom_ele_font):
            custom_font = "<style>@font-face{ font-family: '"+fontmanFamily(custom_ele_font)+"'; src: url("+getCustomFontURL(custom_ele_font)+") format('"+getFontType(custom_ele_font)+"');}</style>"
        else:
            custom_font = "<link rel='stylesheet' href='//fonts.googleapis.com/css?family="+slugifyFont(custom_ele_font)+"'/>"

        #assign the font to elements now
        for classes in custom_classes:
            custom_css = custom_css + ''+str(classes).strip()+'{font-family:\''+fontmanFamily(custom_ele_font)+'\' !important;}'
        custom_css = custom_css + "</style>"
        #we need to save the data to template now (add everything just before </head>)
        themes=shopify_call("https://"+store_url+"/admin/api/2020-10/themes.json",store_token)
        print(themes)
        for theme in json.loads(themes)['themes']:
            if theme['role']=='main':
                theme_id = theme['id']

        assets = shopify_call("https://"+store_url+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=layout/theme.liquid",store_token)
        assets = json.loads(assets)['asset']['value']


        #theme settings
        snippet = "{% include 'fontmancustomcss' %}"
        head_tag = "</head>"

        fontman_api = snippet + head_tag

        if snippet not in assets:
            theme_liquid = assets.replace(head_tag,fontman_api)
            asset = shopify.Asset()
            asset.key = "layout/theme.liquid"
            asset.value = theme_liquid
            success = asset.save()

        markup = custom_font + custom_css
        #here;s the append code
        assets = shopify_call("https://"+store_url+"/admin/api/2020-10/themes/"+str(theme_id)+"/assets.json?asset[key]=snippets/fontmancustomcss.liquid",store_token)
        if not assets:
            assets = ""
        else:
            assets = json.loads(assets)['asset']['value']
        snippet = shopify.Asset()
        snippet.key = "snippets/fontmancustomcss.liquid"
        snippet.value = assets + markup
        success = snippet.save()

        return HttpResponse("Great")
    return JsonResponse({},safe=False)

@csrf_exempt
def uninstall(request):
    store_token= ''
    if request.method == "POST":
        print("CORRET MAN")
        body_json = json.loads(request.body)
        store_url = body_json['domain']
        print("DOMAIN IS HERE MAN "+str(store_url))
        #delete entries from table
        try:
            store = Store.objects.get(name = store_url)
            store_token = store.token
        except Store.DoesNotExist:
            pass

        #delete all db entries please
        # Store.objects.get(name = store_url).delete()
        # Settings.objects.get(store_token = store_token).delete()
        # CustomFonts.objects.filter(store_url = store_url).delete()

        for session in Session.objects.all():
            store = SessionStore(session_key= session.session_key)
            if store.get('shopify'):
                if store.get('shopify')['shop_url'] == store_url:
                    store.delete()
        #do changes to theme
        return JsonResponse({'data':'Payload Received'},safe=False)
    return HttpResponse("<b>NO Access Allowed</b>")


def slugifyFont(font):
    return "+".join(font.split(":")[0].split())

def fontmanFamily(font):
    if isCustomFont(font):
        return customifyFont(font)
    return font.split(":")[0]

def isCustomFont(font):
    extension = ['.woff','.woff2','.ttf','.otf']
    return list(filter(font.endswith, extension)) != []

def customifyFont(font):
    return font.split('.')[0]

def getFontType(font):
    extension = font.split('.')[1]
    if extension == "ttf":
        return "truetype"
    if extension == "woff" or extension == "woff2":
        return extension
    if extension == "otf":
        return "opentype"
    return ""
def getCustomFontURL(font):
    try:
        my_custom_font = CustomFonts.objects.get(font_name =  font )
    except CustomFonts.DoesNotExist:
        pass
    return str(my_custom_font.public_url)


