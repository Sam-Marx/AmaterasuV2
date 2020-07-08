#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import argparse
import cmd2
import re
import requests
import tldextract
from lib.checksettings import *
import sys

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('target', help='target help')
parser_target.add_argument('target', type=str)

parser_saveresults = set_subparsers.add_parser('saveresults', help='saveresults help')
parser_saveresults.add_argument('saveresults', type=bool)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["target", "saveresults", "config", "banner"])

class EmailExtractor(cmd2.Cmd):
	prompt = 'amaterasu[recon/email_extractor]> '

	del cmd2.Cmd.do_set

	def __init__(self):
		# terminal lock
		super().__init__()
		self.target = ''
		self.saveresults = False
		self.allEmails = []
		self.allLinks = []
		self.email_regex = re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}")
		self.href_regex = re.compile('href="(.*?)"')

	def show(self, args):
		'''Shows something'''
		if args.show == 'banner':
			print('banner')

		if args.show == 'config':
			print(f'Target : {self.target}\nSave results : {self.saveresults}')

		if args.show == 'target':
			print(f'Target: {self.target}')

		if args.show == 'saveresults':
			print(f'Save results: {self.saveresults}')
			
	def set_target(self, args):
		self.target = args.target
		print(f'Target set: {self.target}')

	def set_saveresults(self, args):
		self.saveresults = args.saveresults
		print(f'Save results set: {self.saveresults}')

	parser_target.set_defaults(func = set_target)
	parser_saveresults.set_defaults(func = set_saveresults)
	show_parser.set_defaults(func = show)

	@cmd2.with_argparser(show_parser)
	def do_show(self, args):
		''' Show [config, target etc.].'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('show')

	@cmd2.with_argparser(set_parser)
	def do_set(self, args):
		'''Used to set options.'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('set')

	def do_clear(self, args):
		'''Clears the console.'''
		if platform.system() == 'Windows':
			os.system('cls')
		else:
			os.system('clear')

	def do_run(self, args):
		'''Runs the module.'''
		if self.target != '':
			if checkSettings().checkHTTP(self.target):
				requestTarget = requests.get(self.target)
				allLinks = self.href_regex.findall(requestTarget.text)

			else:
				self.target = 'http://' + self.target
				requestTarget = requests.get(self.target)
				links = self.href_regex.findall(requestTarget.text)

				for link in links:
					self.allLinks.append(link)

			self.allLinks = sorted(set(self.allLinks))

			for link in self.allLinks:
				try:
					if link.startswith('//'):
						link = 'http:' + link
					if link.startswith('#') or link.startswith('/'):
						link = self.target + '/' + link

					requestLink = requests.get(link)

					if requestLink.status_code == 200:
						print(f'Trying to find e-mails in {link}.')

					emails = self.email_regex.findall(requestLink.text)

					for email in emails:
						self.allEmails.append(email)
				except KeyboardInterrupt:
					break
				except Exception as e:
					print(f'Error: {e}')

			del(emails)

			self.allLinks = sorted(set(self.allLinks))
			print(f'Searched in {str(len(self.allLinks))} directories.\nTrying to find e-mails in PGP.')

			try:
				domainName, suffix = tldextract.extract(self.target).domain, tldextract.extract(self.target).suffix
				domain = domainName + '.' + suffix
				requestPGP = requests.get(f'https://pgp.mit.edu/pks/lookup?search={domain}&op=index')
				
				if requestPGP.status_code == 200:
					emails = self.email_regex.findall(requestPGP.text)

					if len(emails) == 0:
						print('Found nothing in PGP.')
					else:
						print(f'Found {str(len(emails))} e-mails in PGP.')

					for email in emails:
						self.allEmails.append(email)
				else:
					print('PGP failed.')

			except KeyboardInterrupt:
				pass
			except Exception as e:
				print(f'Error: {str(e)}.')

			print(f'{len(sorted(set(self.allEmails)))} e-mails found.')

			if sorted(set(self.allEmails)) != 0:
				for email in sorted(set(self.allEmails)):
					print(f'E-mail found: {email}.')

				if self.saveresults == True:
					pass
		else:
			print('You need to set a target.')

	def do_back(self, args):
		'''Goes back to Amaterasu.'''
		return True