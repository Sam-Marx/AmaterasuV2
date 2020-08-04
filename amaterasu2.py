#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import os
import cmd2
import platform
import requests
import argparse

from prettytable import from_db_cursor
from huepy import *

from lib.db.sqlconnection import *
from lib.checksettings import *
from lib._banner import banner
from modules import *

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["modules", "apis", "banner"])
use_parser = argparse.ArgumentParser()
use_choices = list()
for item in SQLiteConnection().select_from_task(SQLiteConnection().create_connection('lib/db/amaterasu.db'), 'modules', 'modules_name'): use_choices.extend(item)
use_parser.add_argument('use', choices=use_choices)

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_api = set_subparsers.add_parser('api key', help='apikey help')
parser_api.add_argument('api', type=str, choices=['emailrep', 'shodan', 'leak_lookup', 'fullcontact'])
parser_api.add_argument('key', type=str)

class Amaterasu(cmd2.Cmd):
	version = open('version.txt', 'r').read()

	prompt = 'amaterasu> '
	intro = f'{banner()} Welcome to Amaterasu v{version}.\n{checkSettings().checkUpdate()}'

	del cmd2.Cmd.do_edit
	del cmd2.Cmd.do_py
	del cmd2.Cmd.do_shortcuts
	del cmd2.Cmd.do_alias
	del cmd2.Cmd.do_history
	del cmd2.Cmd.do_macro
	del cmd2.Cmd.do_run_pyscript
	del cmd2.Cmd.do_run_script
	del cmd2.Cmd.do_shell

	def __init__(self):
		super().__init__()

		# db connection
		self.sql_connection = SQLiteConnection().create_connection('lib/db/amaterasu.db')

	def show(self, args):
		'''methods subcommand of show command'''
		if args.show == 'banner':
			print(banner())

		if args.show == 'modules':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(self.sql_connection, 'modules')))

		if args.show == 'apis':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(self.sql_connection, 'APIs')))

	def use(self, args):
		try:
			modules = {'email_extractor':EmailExtractor().cmdloop,
				'honeypot_detector':HoneypotDetector().cmdloop,
				'atg_worm':ATGworm().cmdloop,
				'links_extractor':LinksExtractor().cmdloop,
				'emailrep':EmailRep().cmdloop,
				'cve_2020_5902':cve_2020_5902().cmdloop
			}

			modules[args.use.lower()]()
		except Exception as e:
			print(e)
			

	def set_apikey(self, args):
		try:
			sql = f"""INSERT INTO APIs(name, key) VALUES('{args.api}', '{args.key}')"""
			SQLiteConnection().insert(self.sql_connection, sql)
			print(info(f'{args.api} API key set.'))
		except Exception as e:
			print(bad(f'Error: {e}'))

	show_parser.set_defaults(func = show)
	use_parser.set_defaults(func = use)
	parser_api.set_defaults(func = set_apikey)

	@cmd2.with_argparser(show_parser)
	def do_show(self, args):
		''' Show [modules, APIs, banner].'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('show')

	@cmd2.with_argparser(use_parser)
	def do_use(self, args):
		''' Use [module].'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('use')
	
	@cmd2.with_argparser(parser_api)
	def do_set(self, args):
		''' Set [API key].'''
		func = getattr(args, 'func', None)

		if func is not None:
			func(self, args)
		else:
			self.do_help('use')

	def do_clear(self, args):
		'''Clears the console.'''
		if platform.system() == 'Windows':
			os.system('cls')
		else:
			os.system('clear')

if __name__ == '__main__':
	Amaterasu().cmdloop()