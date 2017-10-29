#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of Kangaroo.

    Kangaroo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Kangaroo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Kangaroo.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
import os
import locale
import gettext
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GdkPixbuf
try:
    import constants as cn
    import helper as hl
except ImportError:
    import kangaroo.constants as cn
    import kangaroo.helper as hl

class Results(Gtk.Box):
    
    update = False

    try:
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
        translate = gettext.translation (cn.App.application_shortname, locale_path, [current_locale] )
        _ = translate.gettext
    except FileNotFoundError:
        _ = str

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)   
        self.parent = parent
        self.resize(0)
        self.set_homogeneous(True)
        self.scroll = Gtk.ScrolledWindow()
        self.generate_items()
        self.add(self.scroll)
        
    def resize(self, height):
        return self.set_size_request(False, height)

    def generate_items(self, data=[], update=False):
        items = data
        if update == False:
            self.items_model = Gtk.ListStore(int, str, str)
        self.items_model.clear()
        for item in items:
            self.items_model.append([item[0], item[1], item[2]])
        self.item_sort = Gtk.TreeModelSort(model=self.items_model)
        self.treeview = Gtk.TreeView.new_with_model(self.item_sort)
        self.treeview.connect("row-activated", self.row_activated)
        for i, column_title in enumerate([self._('Id'), self._('Item'), self._('Type')]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
            self.treeview.set_headers_visible(False)
        self.scroll.add(self.treeview)


    def row_activated(self, widget, row, col):
        model = widget.get_model()
        self.parent.parent.Search.do(model[row][:])
