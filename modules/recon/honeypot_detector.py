#!/usr/bin/env python3.7
#coding: utf-8
#Project amaterasu

import argparse
import cmd2
import requests
from prettytable import from_db_cursor
from huepy import *

from lib.db.sqlconnection import *
from lib.opt_data import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('target', help='target help')
parser_target.add_argument('target', type=str)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["apis", "config"])

class HoneypotDetector(cmd2.Cmd):
	def __init__(self):
		# terminal lock
		super().__init__()

		# db connection
		self.sql_connection = SQLiteConnection().create_connection('lib/db/amaterasu.db')
		self.target = None
		self.shodanAPIkey = SQLiteConnection().select_task_by_priority(self.sql_connection, "key", "APIs", "name", "shodan")[0][0]
		self.metadata = {'Description'	: 'Scans target for honeypot using Shodan.',
						'Author'	 	: 'Sam Marx <sam-marx[at]protonmail.com>',
						'Version'	 	: '1.0',
		}

		Options = Opt()
		Options.new(name='target', current_setting=self.target, required=True, description="Website target")
		Options.new(name='shodan', current_setting=self.shodanAPIkey, required=True, description='Shodan API key')

		self.prompt = 'amaterasu[recon/honeypot_detector]> '
		self.intro = f'{lightblue("Provided by:")}\n{self.metadata["Author"]}\n\n'
		self.intro += f'{lightblue("Description:")}\n{self.metadata["Description"]}\n\n'
		self.intro += f'{lightblue("Options:")}\n{Options.create_table()}\n'

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'Target: {self.target}\nShodan API key: {self.shodanAPIkey}')

		if args.show == 'apis':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(self.sql_connection, 'apis')))

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
		if self.target is None or self.shodanAPIkey is not None:
			requestShodan = requests.get(f'https://api.shodan.io/labs/honeyscore/{self.target}?key={self.shodanAPIkey}')

			if requestShodan.status_code == 401:
				print(bad('Unauthorized request. You need a valid API key to use this module.'))
			if requestShodan.status_code == 200:
				if float(requestShodan.text) > 0.5:
					print(bad(f'Apparently, it is a honeypot.\n\tScore: {requestShodan.text}'))
				else:
					print(good(f'It is not a honeypot, apparently.\n\tScore: {requestShodan.text}'))
		else:
			print(bad('You need to set a target and a Shodan API key.'))