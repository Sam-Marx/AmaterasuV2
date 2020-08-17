#!/usr/bin/env python3
#coding: utf-8
# Amaterasu project

import argparse
import cmd2
from huepy import *
import socket

from lib.checksettings import *
from lib.opt_data import *

set_parser = argparse.ArgumentParser()
set_subparsers = set_parser.add_subparsers(title='subcommands', help='subcommand help')

parser_target = set_subparsers.add_parser('TARGET', help='target help')
parser_target.add_argument('TARGET', type=str)

show_parser = argparse.ArgumentParser()
show_parser.add_argument('show', choices=["config"])

class IPdata(cmd2.Cmd):
	def __init__(self):
		# terminal lock
		super().__init__()

		self.target = None
		self.metadata = {'Description'	: 'Retrieves basic IP data.',
						'Author'	 	: 'Sam Marx <sam-marx[at]protonmail.com>',
						'Version'	 	: '1.0',
		}

		Options = Opt()
		Options.new(name='TARGET', current_setting=None, required=True, description="Target's IP/website")

		self.prompt = 'amaterasu[recon/ipdata]> '
		self.intro = f'{lightblue("Provided by:")}\n{self.metadata["Author"]}\n\n'
		self.intro += f'{lightblue("Description:")}\n{self.metadata["Description"]}\n\n'
		self.intro += f'{lightblue("Options:")}\n{Options.create_table()}\n'

	def show(self, args):
		'''Shows something'''
		if args.show == 'config':
			print(f'TARGET: {self.target}')

	def set_target(self, args):
		if checkSettings().checkHTTP(args.TARGET):
			args.TARGET = checkSettings().urltodomain(args.TARGET)
		self.target = args.TARGET
		print(info(f'TARGET set: {self.target}'))

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
		return True

	def do_run(self, args):
		try:
			if self.target is not None:
				target = socket.gethostbyname(self.target)
				request_ipapi = requests.get(f'https://ipapi.co/{target}/json')

				ip_data = ['ip', 'city', 'region', 'region_code', 'country_name', 
						'country', 'postal', 'latitude', 'longitude', 'timezone', 
						'utc_offset', 'asn', 'org'
				]

				print(info(f'{"Banner":20}{checkSettings().get_banner(self.target, 22)}'))

				for data in ip_data:
					if request_ipapi.json()[data] is not None:
						print(good(f'{checkSettings().clearstring(data):20}{request_ipapi.json()[data]}'))

			else:
				print(bad('You have to set a TARGET.'))
		except Exception as e:
			print(bad(f'Request error: {e}'))