#!/usr/bin/env python3
#coding: utf-8

from cmd2.table_creator import Column, HorizontalAlignment, SimpleTable, VerticalAlignment
from typing import Any, List

class Opt:
	def __init__(self):
		self.data_list: List[List[Any]] = list()
		self.columns: List[Column] = list()

	def new(self, **kwargs):
		name = kwargs.get('name')
		current_setting = kwargs.get('current_setting')
		required = self.bool_transformer(kwargs.get('required'))
		description = kwargs.get('description')

		self.data_list.append([name, current_setting, required, description])

	def create_table(self):
		self.columns.append(Column("Name", width=24))
		self.columns.append(Column("Current Setting", width=26))
		self.columns.append(Column("Required", width=8))
		self.columns.append(Column("Description", width=45, 
			header_horiz_align=HorizontalAlignment.CENTER, 
			data_horiz_align=HorizontalAlignment.CENTER))

		return SimpleTable(self.columns).generate_table(self.data_list, row_spacing=0)

	def bool_transformer(self, value: bool) -> str:
		return str(value).replace('True', 'yes').replace('False', 'no')
