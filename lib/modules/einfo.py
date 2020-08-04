#!/usr/bin/env python3.7
#coding: utf-8

import requests
import re
import json

__all__ = ['twitter', 'facebook', 'spotify', 'steam', 'pinterest', 'discord', 'instagram', 'pornhub', 'xvideos', 'redtube']

'''
Made by @N0n4Me (Telegram)
Adapted by @SamMarx (Telegram)
'''

def twitter(email):
	user_agent = 'Mozilla/5.0 (Linux; U; Android 6.0; en-us; Nexus 30 Build/JOJeG) AppleWebKit/587.20 (KHTML, like Gecko) Version/3.0 Mobile Safari/5894.10'
	headers = {"User-Agent":user_agent}

	try:
		first_request = requests.get('https://twitter.com/account/begin_password_reset', headers=headers)
		value = re.findall(r'value="([\w_?-?]+)"', first_request.text)
		new_headers = {"Host": "twitter.com", "Origin": "https://twitter.com", "User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded", "Referer": "https://twitter.com/account/begin_password_reset", "Accept-Language": "en-US"}
		data = {"authenticity_token": value[0], "account_identifier": email}
		cookies = first_request.cookies.get_dict()
		last_request = requests.post('https://twitter.com/account/begin_password_reset', headers=new_headers, data=data, cookies=cookies)

		if 'Email a link to' in last_request.text:
			return True
		return False
	except:
		return False

def facebook(email):
	check_url = 'https://m.facebook.com/login/identify/?ctx=recover&search_attempts'
	headers = {"Host":"m.facebook.com",
	"Connection":"keep-alive",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0; en-us; Nexus 11 Build/JOP24G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"en-US"}

	try:
		first_request_to_facebook = requests.get('https://m.facebook.com/login/identify/?ctx=recover&c=https%3A%2F%2Fm.facebook.com%2F&multiple_results=0&ars=facebook_login&lwv=100&_rdr', headers=headers)
		values = re.findall(r'value="([\w_?-?]+)"', first_request_to_facebook.text)
		data = {'lsd':values[0], 'jazoest':values[1], 'email':email, 'first_name':'', 'last_name':'', 'did_submit':values[2]}

		headers['Referer'] = 'https://m.facebook.com/login/identify/?ctx=recover&c=https%3A%2F%2Fm.facebook.com%2F&multiple_results=0&ars=facebook_login&lwv=100&_rdr'
		headers["Cache-Control"] = "max-age=0"
		headers["Content-Length"] = "89"
		headers["Content-Type"] = "application/x-www-form-urlencoded"

		last_request_to_facebook = requests.post('https://m.facebook.com/login/identify/?ctx=recover&search_attempts=1&ars=facebook_login', data=data, headers=headers)

		if not check_url in last_request_to_facebook.url:
			return True
		return False

	except Exception as e:
		return False
		print(e)

def pornhub(email):
	headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0; en-us; Nexus 11 Build/JOP24G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}
	url = 'https://www.pornhub.com/signup'

	try:
		request_signup = requests.get(url, headers=headers)
		token = re.findall(r'data-autocomplete="token=([\w\.?\-?\_?]+)&', request_signup.text)[0]
		cookies = request_signup.cookies.get_dict()
		data = {'token': token, 'captcha_type': 'v3', 'check_what': 'email', 'taste_profile': '', 'email': email, 'username': '', 'password': ''}

		headers['Requested-With'] = 'XMLHttpRequest'
		headers['Referer'] = url
		request_create_account = requests.post(f'https://www.pornhub.com/user/create_account_check?token={token}', data=data, headers=headers, cookies=cookies)

		if 'Email has been taken' in request_create_account.text:
			return True
		return False
	except:
		return False

def xvideos(email):
	email = email.replace('@', '%40')
	headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0; en-us; Nexus 30 Build/JOJeG) AppleWebKit/587.20 (KHTML, like Gecko) Version/3.0 Mobile Safari/5894.10'}

	try:
		request_xvideos = requests.get(f'https://www.xvideos.com/account/checkemail?email={email}', headers=headers)

		if 'false' in request_xvideos.text:
			return True
		return False
	except:
		return False

def redtube(email):
	headers = {'X-Requested-With':'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0; en-us; Nexus 30 Build/JOJeG) AppleWebKit/587.20 (KHTML, like Gecko) Version/3.0 Mobile Safari/5894.10', 'Referer':'https://www.redtube.com/register', 'language':'{"lang":"en","showMsg":false}'}

	try:
		request_register = requests.get('https://www.redtube.com/register', headers=headers)
		token = re.findall(r'page_params.token = "([\w\_?\-?\.?]+.)"', request_register.text)[0]
		cookies = request_register.cookies.get_dict()
		data = {'token':token, 'redirect':'', 'check_what':'email', 'email':email}
		request_create_account = requests.post('https://www.redtube.com:443/user/create_account_check?token={}', cookies=cookies, headers=headers, data=data)

		if 'Email has been taken' in request_create_account.text:
			return True
		return False
	except:
		return False

def spotify(email):
	try:
		request_spotify = requests.get(f'https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}')

		if request_spotify.json()['status'] == 20:
			return True
		return False
	except:
		return False

def steam(email):
	headers = {'User-Agent':'IR4ndOn4605'}
	email_replaced = email.replace('@', '%40')

	try:
		request_steam_one = requests.get('https://help.steampowered.com/pt-br/wizard/HelpWithLoginInfo?issueid=404', headers=headers)
		cookies = request_steam_one.cookies.get_dict()
		session_id = cookies['sessionid']

		new_headers = {"Host":"help.steampowered.com",
			"Connection":"keep-alive",
			"Accept":"*/*",
			"X-Requested-With":"XMLHttpRequest",
			"CSP":"active",
			"User-Agent":headers['User-Agent'],
			"Referer":"https://help.steampowered.com/pt-br/wizard/HelpWithLoginInfo?issueid=406",
			"Accept-Encoding":"gzip, deflate",
			"Accept-Language":"en-US"}

		new_request = requests.get(f'https://help.steampowered.com/en/wizard/AjaxLoginInfoSearch?reset=0&lost=0&issueid=404&searches=1&search={email_replaced}&sessionid={session_id}&wizard_ajax=1', headers=new_headers, cookies=cookies)

		if "wizard" in new_request.text:
			if not "Please try again later" in new_request.text:
				return True
		return False

	except Exception as e:
		return False

def pinterest(email):
	headers = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0; en-us; Nexus 11 Build/JOP24G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}

	try:
		request_pinterest = requests.get(f'https://br.pinterest.com/resource/EmailExistsResource/get/?source_url=%2Fsignup%2Fstep1%2F&data=%7B%22options%22%3A%7B%22email%22%3A%22{email}%22%7D%2C%22context%22%3A%7B%7D%7D&_=159479985033', headers = headers)

		if request_pinterest.json()['resource_response']['data']:
			return True
		return False
	except:
		return False

def discord(email):
	headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J200BT Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36', 
	'Content-Type': 'application/json'}

	data = {'email': email, 
	'username': 'teste', 
	'password': 'password_of_email', 
	'invite': None, 
	'consent': True, 
	'gift_code_sku_id': None, 
	'captcha_key': None}

	url = 'https://discord.com/api/v6/auth/register'

	try:
		request_discord = requests.post(url, data=json.dumps(data), headers=headers)

		if 'Email is already registered.' in request_discord.text:
			return True
	except:
		return False

def instagram(email):
	headers = {"Host": "www.instagram.com", "Connection": "keep-alive", 
	"Origin": "https://www.instagram.com", "CSP": 
	"active", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", 
	"Accept-Language": "en-US", "Accept-Encoding":"gzip, deflate", 
	"User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0; en-us; Nexus 11 Build/JOP24G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"}

	try:
		first_instagram_request = requests.get("https://www.instagram.com/accounts/password/reset/", headers=headers)
		cookies = first_instagram_request.cookies.get_dict()
		rollout_hash = re.findall(r"rollout_hash\"\:\"([\w_?-?]+)\"", first_instagram_request.text)
		data = {"email_or_username": email, "recaptcha_challenge_field": ""}

		headers['Content-Length'] = '61'
		headers['Referer'] = 'https://www.instagram.com/accounts/password/reset/'
		headers['X-CSRFToken'] = cookies['csrftoken']
		headers['X-Requested-With'] = 'XMLHttpRequest'
		headers['X-Instagram-AJAX'] = rollout_hash[0]

		instagram_account_recovery_request = requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/', headers=headers, data=data, cookies=cookies)

		if not 'No users found' in instagram_account_recovery_request.text:
			return True
		return False
	except Exception as e:
		return False