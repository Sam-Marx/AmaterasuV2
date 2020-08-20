#!/usr/bin/env python3
#coding: utf-8
# Amaterasu project

import socket
import sys
from huepy import *
from typing import Optional

class handle:
	def __init__(self, lhost: str, lport: int, command: Optional[str] = None):
		self.host = lhost
		self.port = lport
		self.command = command
		self.sock = None

	def run(self):
		self.create_socket()
		self.bind_socket()
		self.accept_socket()

	def create_socket(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as sock_error:
			print(bad(f'Socket creation error: {sock_error}'))

	def bind_socket(self):
		try:
			print(info(f'Binding socket to port {self.port}...'))
			self.sock.bind((self.host, self.port))
			self.sock.listen(5)
		except socket.error as sock_error:
			print(bad(f'Socket binding error: {sock_error}.\nRetrying...'))
			self.bind_socket()

	def accept_socket(self):
		try:
			connection, address = self.sock.accept()
			print(good(f'Connection has been established.\n'))

			self.send_commands(connection)
			connection.close()
		except socket.error as sock_error:
			print(bad(f'Socket accepting error: {sock_error}'))

	def send_commands(self, connection):
		while True:
			command = input(bold(white('amaterasu>> ')))

			if self.command:
				command = self.command.format(command)

			if command.lower() == 'quit':
				connection.close()
				self.sock.close()
				sys.exit()

			if len(command) > 0:
				connection.send(command.encode())
				result = connection.recv(4096).decode('utf-8')

				print(f'{result}\n', end='')
