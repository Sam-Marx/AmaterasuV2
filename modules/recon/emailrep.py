#!/usr/bin/env python3.8
#coding: utf-8
# Amaterasu project

import argparse
import cmd2
import requests
import re
import json
import concurrent.futures
import time
from huepy import *
import holehe
from prettytable import from_db_cursor

from lib.modules import *
from lib.db.sqlconnection import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('target', help='target help')
parser_target.add_argument('target', type=str)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["apis", "config"])

class EmailRep(cmd2.Cmd):
	prompt = 'amaterasu[recon/emailrep]> '

	def __init__(self):
		# terminal lock
		super().__init__()

		# db connection
		self.sql_connection = SQLiteConnection().create_connection('lib/db/amaterasu.db')

		self.target = ''

		self.leak_lookup_api_key = SQLiteConnection().select_task_by_priority(self.sql_connection, "key", "APIs", "name", "leak_lookup")[0][0]
		self.emailrep_key = SQLiteConnection().select_task_by_priority(self.sql_connection, "key", "APIs", "name", "emailrep")[0][0]
		self.fullcontact_key = SQLiteConnection().select_task_by_priority(self.sql_connection, "key", "APIs", "name", "fullcontact")[0][0]

		self.profiles = []

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'Target: {self.target}')

		if args.show == 'apis':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(self.sql_connection, 'apis')))

	def set_target(self, args):
		self.target = args.target
		print(info(f'Target set: {self.target}'))

	parser_target.set_defaults(func = set_target)
	show_parser.set_defaults(func = show)

	@cmd2.with_argparser(set_parser)
	def do_set(self, args):
		'''Used to set options.'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('set')

	@cmd2.with_argparser(show_parser)
	def do_show(self, args):
		''' Show [config, target etc.].'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('show')

	def do_back(self, args):
		'''Goes back to Amaterasu.'''
		try:
			SQLiteConnection().close_connection(self.sql_connection)
		except:
			pass
		finally:
			return True

	def do_run(self, args):
		try:
			self.profiles.clear()

			functions = [self.emailrepio,
				self.leaklookup,
				self.domainBigData,
				self.fullcontact,
				self.profile_gatherer
			]

			for function in functions:
				with concurrent.futures.ThreadPoolExecutor() as executor:
					executor.submit(function)

			for profile in sorted(set(self.profiles)):
				print(good(f'Profile found: \t{profile}'))

		except Exception as e:
			print(f'Thread error: {e}')

	def leaklookup(self):
		# https://leak-lookup.com
		if self.leak_lookup_api_key is not None:
			try:
				requestLeakLookup = requests.get('https://leak-lookup.com/api/search', data=f'key={self.leak_lookup_api_key}&type=email_address&query={self.target}', timeout=2)
				if requestLeakLookup.status_code == 200:
					leakLookupJson = requestLeakLookup.json()

					message = leakLookupJson['message']

					if leakLookupJson['error'] == True:
						print(bad(f'Leak-Lookup\t\tError: {message}'))
					else:
						for link in message:
							print(good(f'Leak-Lookup\t\tLeak found: {link}'))
				elif requestLeakLookup.status_code == 401:
					print(bad(f'Leak-Lookup\t\terror: invalid api key'))
			except:
				pass

	def fullcontact(self):
		# https://fullcontact.com
		if self.fullcontact_key is not None:
			headers = {'Content-Type':'application/json', 'Authorization':f'Bearer {self.fullcontact_key}'}
			data = json.dumps({'email':self.target})

			try:
				request_fullcontact = requests.post('https://api.fullcontact.com/v3/person.enrich', headers=headers, data=data, timeout=2)

				if request_fullcontact.status_code == 404:
					print(bad('Fullcontact\t\tProfile not found.'))

				if request_fullcontact.status_code == 401:
					print(bad('Fullcontact\t\tAPI key error. Try another key.'))

				if request_fullcontact.status_code == 429:
					print(bad('Fullcontact\t\tYou have reached your request rate limit.'))

				if request_fullcontact.status_code == 200:
					for data in ['fullName', 'gender', 'location', 'organization', 'linkedin']:
						if request_fullcontact.json()[data] is not None:
							print(good(f'Fullcontact\t\t{data.lower().capitalize()}: ' + request_fullcontact.json()[data]))

					for detail in ['emails', 'phones']:
						if request_fullcontact.json()['details'][detail] is not None:
							for data in request_fullcontact.json()['details'][detail]:
								data_to_be_shown = detail.lower().capitalize()[:-1]
								print(good(f'Fullcontact\t\t{data_to_be_shown}: ' + data))

					for profile in request_fullcontact.json()['details']['profiles']:
						self.profiles.append(request_fullcontact.json()['details']['profiles'][profile]['url'])
						if profile in self.profiles:
							self.profiles.remove(profile)
						else:
							self.profiles.append(profile)
			except:
				pass

	def emailrepio(self):
		# emailrep.io
		if self.emailrep_key is not None:
			headers = {'User-Agent':'AmaterasuV2', 'Content-Type':'application/json', 'Key':self.emailrep_key}

			try:
				requestEmailRep = requests.get(f'https://emailrep.io/{self.target}', headers=self.headers, timeout=2)

				if requestEmailRep.status_code == 200:
					emailrepJson = requestEmailRep.json()
					profiles = emailrepJson['details']['profiles']

					for detail in ['last_seen', 'first_seen', 'data_breach', 'credentials_leaked']:
						if emailrepJson['details'][detail] is not None:
							data = detail.capitalize().replace('_', ' ')
							print(good(f'EmailRep\t\t{data}: ' + str(emailrepJson['details'][detail])))

					for profile in profiles:
						self.profiles.append(profile)

				elif requestEmailRep.status_code == 400:
					print(bad('EmailRep\t\terror: invalid e-mail.'))
				elif requestEmailRep.status_code == 401:
					print(bad('EmailRep\t\terror: invalid api key'))
				elif requestEmailRep.status_code == 429:
					print(bad('EmailRep\t\terror: too many requests. Contact emailrep.io for an api key'))
			except:
				pass

	def domainBigData(self):
		try:
			for domain in domainbigdata(self.target).get_domains():
				print(good(f'DomainBigData\tDomain owned: {domain}'))
		except:
			pass

	def profile_gatherer(self):
		holehe_dict 	= {}
		einfo_dict  	= {}
		einfo_services  = [twitter, facebook, spotify, steam, pinterest, discord, instagram, pornhub, xvideos, redtube]
		holehe_services = [holehe.apple, holehe.adobe, holehe.ebay, holehe.pastebin, holehe.firefox, holehe.office365, holehe.live, holehe.lastfm, holehe.tumblr, holehe.github]

		try:
			with concurrent.futures.ThreadPoolExecutor(max_workers = len(einfo_services)) as executor:
				for service in einfo_services:
					einfo_dict[service.__name__] = executor.submit(service, self.target)

				for service, future in zip(einfo_dict.keys(), concurrent.futures.as_completed(einfo_dict.values())):
					if future.result():
						self.profiles.append(service)

		except Exception as e:
			print(bad(f'Einfo error: {e}'))

		try:
			with concurrent.futures.ThreadPoolExecutor(max_workers = len(holehe_services)) as executor:
				for service in holehe_services:
					holehe_dict[service.__name__] = executor.submit(service, self.target)

				for service, future in zip(holehe_dict.keys(), concurrent.futures.as_completed(holehe_dict.values())):
					if future.result()['exists']:
						self.profiles.append(service)

		except Exception as e:
			print(bad(f'Holehe error: {e}'))
			