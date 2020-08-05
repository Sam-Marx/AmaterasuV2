#!/usr/bin/env python3.8
#coding: utf-8
# Amaterasu project

import requests
from bs4 import BeautifulSoup

class domainbigdata:
	def __init__(self, email, timeout):
		self.email = email
		self.url = f'https://domainbigdata.com/email/{self.email}'
		self.timeout = timeout
		self.clean_domains = []

	def get_domains(self):
		request_url = requests.get(self.url, allow_redirects=True, timeout=self.timeout)
		soup = BeautifulSoup(request_url.text, 'lxml')

		all_domains = soup.find_all("a", id='aDomain')
		for domain in all_domains:
			self.clean_domains.append(domain['href'].replace('/', ''))

		return self.clean_domains