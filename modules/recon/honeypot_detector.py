#!/usr/bin/env python3.7
#coding: utf-8
#Project amaterasu

import argparse
import cmd2
import requests
from lib.sqlconnection import *
from prettytable import from_db_cursor

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('target', help='target help')
parser_target.add_argument('target', type=str)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["target", "apis", "config", "banner"])

class HoneypotDetector(cmd2.Cmd):
	prompt = 'amaterasu[recon/honeypot_detector]> '
	#del cmd2.Cmd.do_set

	def __init__(self):
		# terminal lock
		shodan_test = SQLiteConnection().select_fetchall(SQLiteConnection().create_connection('amaterasu.db'), 'SELECT key FROM apis WHERE name == "shodan"')
		super().__init__()
		self.target = ''
		if shodan_test == None:
			self.shodanAPIkey = ''
		else:
			self.shodanAPIkey = shodan_test

	def show(self, args):
		'''Shows something'''
		if args.show == 'banner':
			print('banner')

		if args.show == 'config':
			print(f'Target: {self.target}')

		if args.show == 'target':
			print(f'Target: {self.target}')

		if args.show == 'apis':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(SQLiteConnection().create_connection('amaterasu.db'), 'apis')))

	def set_target(self, args):
		self.target = args.target
		print(f'Target set: {self.target}')

	parser_target.set_defaults(func = set_target)
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

	def do_run(self, args):
		''' Runs the module.'''
		if self.target != '' or self.shodanAPIkey != '':
			requestShodan = requests.get(f'https://api.shodan.io/labs/honeyscore/{self.target}?key={self.shodanAPIkey}').text
			if float(requestShodan) > 0.5:
				print('Apparently, it is a honeypot.')
			else:
				print('It is not a honeypot, apparently.')
		else:
			print('You need to set a target and a Shodan API key.')