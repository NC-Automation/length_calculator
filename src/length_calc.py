#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2022 reuben <1987.python3.programmer>
# 
# length-calc is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# length-calc is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from decimal import Decimal
from fractions import Fraction
import os, sys, subprocess, re, decimal


UI_FILE = "src/length_calc.ui"


class GUI:
	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		self.edit_widget = None # variable placeholder for editing cells
		self.total_length = Decimal()
		
		self.calc_store = self.builder.get_object('calc_store')
		self.treeview = self.builder.get_object("calc_treeview")
		self.tree_selection = self.builder.get_object("calc_tree_selection")

		window = self.builder.get_object('window')
		window.show_all()

	def on_window_destroy(self, window):
		Gtk.main_quit()

	### start callbacks

	def qty_edited (self, cellrenderertext, path, text):
		number = re.sub("[^0-9]", "", text)
		self.calc_store[path][0] = int(number)
		self.calculate_row_sum(path)

	def feet_edited (self, cellrenderertext, path, text):
		number = re.sub("[^0-9]", "", text)
		self.calc_store[path][1] = int(number)
		self.calculate_row_sum(path)

	def inches_edited (self, cellrenderertext, path, text):
		inches = text
		try:   # check if valid Decimal otherwise convert to decimal
			Decimal(text) 
		except decimal.InvalidOperation:
			try: # on error go back to same cell
				inches = str(self.architectural_to_decimal(text))
			except decimal.InvalidOperation:
				self.builder.get_object('main_box').set_visible(False)
				GLib.timeout_add(500, self.show_box, path)
				return True
		self.calc_store[path][2] = text
		self.calc_store[path][3] = inches
		self.calculate_row_sum(path)

	def show_box (self, path):
		self.builder.get_object('main_box').set_visible(True)
		column = self.treeview.get_column(2)
		GLib.timeout_add(10, self.treeview.set_cursor, path, column, True)

	def qty_editing_started (self, cellrenderer, celleditable, path):
		self.edit_widget = celleditable
		celleditable.connect("activate", self.move_cursor_to_column, 1) # enter key
		self.builder.get_object("fraction_box").set_sensitive(False)

	def feet_editing_started (self, cellrenderer, celleditable, path):
		self.edit_widget = celleditable
		celleditable.connect("activate", self.move_cursor_to_column, 2) # enter key
		self.builder.get_object("fraction_box").set_sensitive(False)

	def inches_editing_started (self, cellrenderer, celleditable, path):
		self.edit_widget = celleditable
		celleditable.connect("activate", self.move_cursor_to_next_row) # enter key
		self.builder.get_object("fraction_box").set_sensitive(True)

	def move_cursor_to_column (self, entry, col):
		model, path = self.tree_selection.get_selected_rows()
		next_column = self.treeview.get_column(col)
		GLib.timeout_add(10, self.treeview.set_cursor, path, next_column, True)

	def move_cursor_to_next_row (self, entry = None):
		model, path = self.tree_selection.get_selected_rows()
		titer = model.iter_next(model.get_iter(path))
		if titer is None:
			titer = model.append([0, 0, '0', '0', '0', '0'])
		path = model.get_path(titer)
		column = self.treeview.get_column(0)
		GLib.timeout_add(10, self.treeview.set_cursor, path, column, True)

	def number_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		# consolidated function(s) by getting the number from the button's label
		number = button.get_label()
		subprocess.call(['xte', "key %s" % number])

	def dot_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		subprocess.call(['xte', "key period"])

	def slash_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "key slash"])

	def hyphen_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "key minus"])

	def space_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		subprocess.call(['xte', "key space"])

	def backspace_clicked_cb (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "key BackSpace"])

	def enter_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "key Return"])

	def seven_eigth_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -7/8"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def three_quarter_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -3/4"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def five_eigth_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -5/8"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def one_half_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -1/2"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def three_eigth_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -3/8"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def one_quarter_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -1/4"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def one_eigth_clicked (self, button):
		if self.edit_widget == None:
			return
		number = button.get_label()
		subprocess.call(['xte', "str -1/8"])
		GLib.timeout_add(10, self.edit_widget.editing_done)
		GLib.timeout_add(15, self.move_cursor_to_next_row)

	def treeview_tab_key (self, treeview, event):
		keyname = Gdk.keyval_name(event.keyval)
		path, col = treeview.get_cursor()
		# only editable columns!!
		columns = []
		for i in [0,1,2]:
			columns.append(treeview.get_column(i))
		colnum = columns.index(col)
		if keyname == "Tab":
			# critical code to keep the 'activate' signal from firing, resulting in skipping a column
			self.edit_widget.editing_done()  
			if colnum + 1 < len(columns):
				next_column = columns[colnum + 1]
			else:
				tmodel = treeview.get_model()
				titer = tmodel.iter_next(tmodel.get_iter(path))
				if titer is None:
					titer = tmodel.append([0, 0, '0', '0', '0', '0'])
				path = self.calc_store.get_path(titer)
				next_column = columns[0]
			GLib.timeout_add(10, treeview.set_cursor, path, next_column, True)

	def price_per_foot_changed (self, spinbutton):
		self.calculate_total_price ()

	def price_spinbutton_focus_in_event (self, spinbutton, event):
		GLib.idle_add(spinbutton.select_region, 0, -1)

	### end callbacks

	def architectural_to_decimal (self, text):
		''' Convert architectural measurements to inches.'''
		# See http://stackoverflow.com/questions/8675714
		text = re.sub(" ", "-", text).lstrip("-")
		text = text.replace('"', '').replace(' ', '')
		feet, sep, inches = text.rpartition("'")
		floatfeet, sep, fracfeet = feet.rpartition('-')
		feetnum, sep, feetdenom = fracfeet.partition('/')
		feet = Decimal(floatfeet or 0) + Decimal(feetnum or 0) / Decimal(feetdenom or 1)
		floatinches, sep, fracinches = inches.rpartition('-')
		inchesnum, sep, inchesdenom = fracinches.partition('/')
		inches = Decimal(floatinches or 0) + Decimal(inchesnum or 0) / Decimal(inchesdenom or 1)
		return feet * Decimal(12) + inches

	def calculate_row_sum (self, path):
		qty = self.calc_store[path][0]
		feet = self.calc_store[path][1]
		inches = self.calc_store[path][3]
		row_sum = Decimal(qty) * (( Decimal(feet) * 12 ) + Decimal(inches) )
		feet = int(row_sum / 12)
		inches = row_sum % 12
		decimal_inch = inches - int(inches)
		fractions = Fraction(decimal_inch)
		if fractions == 0:
			self.calc_store[path][4] = '''%s' %s"''' % (feet, int(inches))
			self.calc_store[path][5] = str(row_sum)
		else:
			self.calc_store[path][4] = '''%s' %s-%s"''' % (feet, int(inches), fractions)
			self.calc_store[path][5] = str(row_sum)
		self.calculate_total_length()

	def calculate_total_length (self):
		self.total_length = Decimal()
		total_qty = int()
		for row in self.calc_store:
			self.total_length += Decimal(row[5])
			total_qty += row[0]
		feet = int(self.total_length / 12)
		inches = self.total_length % 12
		fractions = Fraction(inches - int(inches))
		if fractions == 0:
			label = '''%s' %s"''' % (feet, int(inches))
			self.builder.get_object("total_length_label").set_label(label)
		else:
			label = '''%s' %s-%s"''' % (feet, int(inches), fractions)
			self.builder.get_object("total_length_label").set_label(label)
		self.builder.get_object("total_qty_label").set_label(str(total_qty))
		self.calculate_total_price ()

	def calculate_total_price (self):
		price_per_foot = self.builder.get_object("price_spinbutton").get_text()
		if price_per_foot == '0.00' or self.total_length == Decimal('0.00'):
			self.builder.get_object("total_price_label").set_label("0.00")
			return
		total_price = ( Decimal(price_per_foot) * self.total_length ) / Decimal(12)
		total_price = "${:,.2f}".format(total_price)
		self.builder.get_object("total_price_label").set_label(total_price)
			

def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

