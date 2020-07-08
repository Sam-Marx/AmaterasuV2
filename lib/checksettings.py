#!/usr/bin/env python3.7
#coding: utf-8
# Amaterasu project

import os
import functools
import operator
import requests

class checkSettings:
	'''This class is used to check settings, targets etc.'''
	def __init__(self):
		pass

	def checkHTTP(self, website):
		if website.startswith('http://') or website.startswith('https://'):
			return True

	def checkReportsFolder(self):
		if os.path.isdir('reports') is False:
			return False
		return True

	def tupleToString(self, tuple_arg):
		return functools.reduce(operator.add, (tuple_arg))

	def checkUpdate(self):
		try:
			versionGithub = requests.get('https://raw.githubusercontent.com/Sam-Marx/AmaterasuV2/master/version.txt').text
			version = open('version.txt', 'r').read()

			if float(versionGithub) != float(version):
				return f"Amaterasu can be updated. New version: {versionGithub}"
			else: return ''
		except Exception as e:
			return "Could not check the Github's version."
			#return e