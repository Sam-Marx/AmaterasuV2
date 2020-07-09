#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import os
import cmd2
import platform
import requests
import argparse
from lib.sqlconnection import *
from lib.checksettings import *
from prettytable import from_db_cursor

from modules.recon.email_extractor import *
from modules.recon.honeypot_detector import *
from modules.exploitation.atg_worm import *

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["modules", "apis", "banner"])
use_parser = argparse.ArgumentParser()
use_choices = list()
for item in SQLiteConnection().select_from_task(SQLiteConnection().create_connection('amaterasu.db'), 'modules', 'modules_name'): use_choices.extend(item)
use_parser.add_argument('use', choices=use_choices)

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

# create the parser for the "foo" subcommand
parser_api = set_subparsers.add_parser('api key', help='apikey help')
parser_api.add_argument('api', type=str)
parser_api.add_argument('key', type=str)

class Amaterasu(cmd2.Cmd):
	del cmd2.Cmd.do_edit
	del cmd2.Cmd.do_py
	#del cmd2.Cmd.do_set 
	del cmd2.Cmd.do_shortcuts
	del cmd2.Cmd.do_alias
	del cmd2.Cmd.do_history
	del cmd2.Cmd.do_macro
	del cmd2.Cmd.do_run_pyscript
	del cmd2.Cmd.do_run_script
	del cmd2.Cmd.do_shell

	def __init__(self):
		super().__init__()

	def show(self, args):
		'''methods subcommand of show command'''
		if args.show == 'banner':
			print('''
    ___                       __                                 
   /   |   ____ ___   ____ _ / /_ ___   _____ ____ _ _____ __  __
  / /| |  / __ `__ \ / __ `// __// _ \ / ___// __ `// ___// / / /
 / ___ | / / / / / // /_/ // /_ /  __// /   / /_/ /(__  )/ /_/ / 
/_/  |_|/_/ /_/ /_/ \__,_/ \__/ \___//_/    \__,_//____/ \__,_/ 
			''')
		if args.show == 'modules':
			connection = SQLiteConnection().create_connection('amaterasu.db')
			print(from_db_cursor(SQLiteConnection().select_all_from_task(connection, 'modules')))

		if args.show == 'apis':
			print(from_db_cursor(SQLiteConnection().select_all_from_task(SQLiteConnection().create_connection('amaterasu.db'), 'APIs')))

	def use(self, args):
		if args.use == 'email_extractor':
			email_extractor = EmailExtractor()
			email_extractor.cmdloop()

		if args.use == 'honeypot_detector':
			honeypot_detector = HoneypotDetector()
			honeypot_detector.cmdloop()

		if args.use == 'atg_worm':
			atgworm = ATGworm()
			atgworm.cmdloop()

		if args.use == 'links_extractor':
			linksextractor = LinksExtractor()
			linksextractor.cmdloop()

	def set_apikey(self, args):
		sql = f"""INSERT INTO APIs(name, key) VALUES('{args.api}', '{args.key}')"""
		SQLiteConnection().insert(SQLiteConnection().create_connection('amaterasu.db'), sql)
		print(f'{args.api} API key set.')

	show_parser.set_defaults(func = show)
	use_parser.set_defaults(func = use)
	parser_api.set_defaults(func = set_apikey)

	version = open('version.txt', 'r').read()

	prompt = 'amaterasu> '
	intro = f'Welcome to Amaterasu v{version}.\n{checkSettings().checkUpdate()}'

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