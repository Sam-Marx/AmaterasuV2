#!/usr/bin/env python3.7
#coding: utf-8

import sqlite3

class SQLiteConnection:
	def __init__(self):
		self.made_on = "07.04.20" 

	def create_file(self, filename):
		open(filename, 'w+')

	def create_connection(self, db_file):
		connection = None

		try:
			connection = sqlite3.connect(db_file)
		except Exception as e:
			print(e)

		return connection

	def close_connection(self, connection):
		cursor = connection.cursor()
		cursor.close()

	def select_all_from_task(self, connection, table):
		try:	
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT * FROM {table}")

				return cursor
		except Exception as e:
			print(e)

	def select_from_task(self, connection, table, column):
		try:	
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT {column} FROM {table}")

				return cursor
		except Exception as e:
			print(e)

	def select_fetchall(self, connection, sql):
		try:
			with connection:
				cursor = connection.cursor()
				cursor.execute(sql)

				return cursor.fetchall()[0][0]

		except IndexError:
			return None

		except Exception as e:
			print(e)

	def insert(self, connection, sql):
		try:
			cursor = connection.cursor()
			cursor.execute(sql)
			connection.commit()
			connection.close()
		except Exception as e:
			print(e)