#!/usr/bin/env python3
#coding: utf-8
# Amaterasu project

import os
import functools
import operator
import requests
import re
import socket
from typing import Optional

from cmd2 import ansi

class checkSettings:
	'''This class is used to check settings, targets etc.'''

	def __init__(self):
		pass

	def checkHTTP(self, website: str) -> bool:
		if website.startswith('http://') or website.startswith('https://'):
			return True
		return False

	def checkReportsFolder(self) -> bool:
		if os.path.isdir('reports') is False:
			return False
		return True

	def clearstring(self, string: str) -> str:
		return string.replace('_', ' ').capitalize()

	def tupleToString(self, tuple_arg: tuple) -> str:
		return functools.reduce(operator.add, (tuple_arg))

	def removeHTTP(self, website: str) -> str:
		if self.checkHTTP(website):
			return website.replace('http://', '').replace('https://', '')

	def urltodomain(self, url: str) -> str:
		return re.sub(r'(/[^\/]+$)', '', self.removeHTTP(url))

	def checkUpdate(self):
		try:
			versionGithub = requests.get('https://raw.githubusercontent.com/Sam-Marx/AmaterasuV2/master/version.txt').text
			version = open('version.txt', 'r').read()

			if float(versionGithub) != float(version):
				return f"Amaterasu can be updated. New version: {versionGithub}"
			return None
		except Exception as e:
			return "Could not check Github's version."

	def ansi_print(self, text: str):
		'''Wraps style_aware_write so style can be stripped if needed'''
		ansi.style_aware_write(sys.stdout, f'{text}\n\n')

	def get_banner(self, ip_address: str, port: int, timeout: Optional[int] = 5) -> str:
		socket.setdefaulttimeout(timeout)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			sock.connect((ip_address, port))

			banner = sock.recv(1024)
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()

			return banner.decode("utf-8")
		except:
			return "Unable to get server's banner."
