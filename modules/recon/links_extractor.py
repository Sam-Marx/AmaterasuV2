#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import argparse
import cmd2
import re
import requests
from lib.checksettings import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('target', help='target help')
parser_target.add_argument('target', type=str)

parser_saveresults = set_subparsers.add_parser('saveresults', help='saveresults help')
parser_saveresults.add_argument('saveresults', type=bool)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["config"])

class LinksExtractor(cmd2.Cmd):
	prompt = 'amaterasu[recon/links_extractor]> '

	def __init__(self):
		# terminal lock
		super().__init__()
		self.__version__ = 1
		self.target = ''
		self.saveresults = False
		self.allLinks = []
		self.href_regex = re.compile('href="(.*?)"')

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'Target: {self.target}\nSave results : {self.saveresults}')

	def set_target(self, args):
		self.target = f'http://{args.target}' if not args.target.startswith('http') else args.target
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

	def do_back(self, args):
		'''Goes back to Amaterasu.'''
		return True

	def getLinks(self):
		requestTarget = requests.get(self.target).text

		for link in self.href_regex.findall(requestTarget):
			if link.startswith('/') or link.startswith('#'):
				self.allLinks.append(self.target + link)
			else:
				self.allLinks.append(link)

		self.allLinks = sorted(set(self.allLinks))

	def do_run(self, args):
		self.getLinks()

		if len(self.allLinks) != 0:
			for link in self.allLinks:
				print(f'{link} found.')
		else:
			print('Nothing was found.')