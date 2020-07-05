#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import os
import cmd2
import platform
import requests
import argparse
from sqlconnection import *
from prettytable import from_db_cursor

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["modules", "apis", "banner"])
use_parser = argparse.ArgumentParser()
use_choices = list()
for item in SQLiteConnection().select_from_task(SQLiteConnection().create_connection('modules.db'), 'modules', 'modules_name'): use_choices.extend(item)
use_parser.add_argument('use', choices=use_choices)

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
			connection = SQLiteConnection().create_connection('modules.db')
			print(from_db_cursor(SQLiteConnection().select_all_from_task(connection, 'modules')))

	show_parser.set_defaults(func = show)

	versionGithub = requests.get('https://raw.githubusercontent.com/Sam-Marx/AmaterasuV2/master/version.txt').text
	version = open('version.txt', 'r').read()

	prompt = 'amaterasu> '
	intro = f'Welcome to Amaterasu v{version}.\n' if version == versionGithub else f'Welcome to Amaterasu v{version}. \nAmaterasu can be updated. New version: {str(versionGithub)}.\n'

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

	def do_clear(self, args):
		'''Clears the console.'''
		if platform.system() == 'Windows':
			os.system('cls')
		else:
			os.system('clear')

if __name__ == '__main__':
	Amaterasu().cmdloop()
