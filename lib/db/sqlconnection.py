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

	def select_all_from_task(self, connection, table, fetch = False):
		try:	
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT * FROM {table}")

				if fetch:
					return cursor.fetchall()
				return cursor
		except Exception as e:
			print(e)

	def select_from_task(self, connection, table, column):
		try:	
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT {column} FROM {table}")
				rows = cursor.fetchall()

				return rows
		except Exception as e:
			print(e)

	def select_fetchall(self, connection, sql):
		try:
			with connection:
				cursor = connection.cursor()
				cursor.execute(sql)

				return cursor.fetchall()
		except IndexError:
			return None

		except Exception as e:
			print(e)

	def select_task_by_priority(self, connection, value, table, name, priority):
		try:	
			with connection:
				cursor = connection.cursor()
				cursor.execute(f"SELECT {value} FROM {table} WHERE {name}='{priority}'")

				rows = cursor.fetchall()

				return rows
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