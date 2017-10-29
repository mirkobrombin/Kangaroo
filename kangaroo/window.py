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
from datetime import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
try:
    import constants as cn
    import helper as hl
    import stack as sk
    import search as sh
except ImportError:
    import kangaroo.constants as cn
    import kangaroo.helper as hl
    import kangaroo.stack as sk
    import kangaroo.search as sh

class Window(Gtk.Dialog):
    HGtk = hl.HGtk()

    def __init__(self):
        Gtk.Dialog.__init__(self, 
                            title=cn.App.application_name, 
                            width_request=550,
                            resizable=False,
                            icon_name=cn.App.application_id)
        # Load Translate
        try:
            current_locale, encoding = locale.getdefaultlocale()
            locale_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
            translate = gettext.translation (cn.App.application_shortname, locale_path, [current_locale] )
            _ = translate.gettext
        except FileNotFoundError:
            _ = str

        # Dialog params
        self.HGtk.add_class(self, Gtk.STYLE_CLASS_FLAT)
        self.set_deletable(False)
        self.set_border_width(0)
        
        # Content params
        self.get_action_area().destroy()
        self.main_content = self.get_content_area()
        self.main_content.set_spacing(0)
        self.main_content.set_border_width(0)

        # Search Box
        self.search_box = Gtk.Frame()
        self.HGtk.add_class(self.search_box, "SearchBox")
        self.main_content.add(self.search_box)
        
        # Search Entry
        self.search_entry = Gtk.SearchEntry()
        self.HGtk.add_class(self.search_entry, "SearchEntry")
        self.search_entry.set_placeholder_text(_('Search..'))
        self.search_entry.connect("key-release-event", self.on_entry_key_release)
        self.search_box.add(self.search_entry)
        
        # Stack
        self.stack = sk.Stack(self)
        self.main_content.add(self.stack)
        
        # Search
        self.Search = sh.Search(self)

        # Style
        self.screen = Gdk.Screen.get_default()
        self.css_provider = Gtk.CssProvider()
        try:
            self.css_provider.load_from_path('../data/style.css')
        except GLib.Error:
            self.css_provider.load_from_path('/usr/local/bin/kangaroo/style.css')
        except GLib.Error:
            self.css_provider.load_from_path('/usr/bin/kangaroo/style.css')
        except GLib.Error:
            print('Couldn\'t load style.css')
            exit(1)
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css_provider,
          Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_entry_key_release(self, entry, ev, data=None):
        search_text = entry.get_text()
        self.Search.find(search_text)

