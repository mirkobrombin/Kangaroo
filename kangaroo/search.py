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

import os
import gi
import time
import locale
import gettext
import threading
import subprocess
import numpy as np
import configparser
from time import gmtime, strftime
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
gi.require_version('Wnck', '3.0') 
from gi.repository import Gtk, Gdk, Gio, Granite, GObject, GLib, GdkPixbuf, Wnck
try:
    import constants as cn
    import helper as hl
    import alert as al
except ImportError:
    import kangaroo.constants as cn
    import kangaroo.helper as hl
    import kangaroo.alert as al

GLib.threads_init()

class T_Hello(threading.Thread):

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        
    def run(self):
        pass

class Search:
    HGtk = hl.HGtk()
    HUser = hl.HUser()
    HPath = hl.HPath()
    HString = hl.HString()

    '''
    Define the names of the lists we use for indexing search results
    '''
    index_data = [] # contains the list of windows and applications (id, str, str)
    index_windows_act = [] # contains xid for windows (id, str)
    index_apps_act = [] # contains all commands for applications (id, str)

    search_entry = None
    i = 0

    # Params
    item_height = 26 # This is the height size for each treeview row
    trim_limit = 50 # Limit characters per line

    # Load Translate
    try:
        current_locale, encoding = locale.getdefaultlocale()
        locale_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
        translate = gettext.translation (cn.App.application_shortname, locale_path, [current_locale] )
        _ = translate.gettext
    except FileNotFoundError:
        _ = str

    def __init__(self, parent):
        self.parent = parent # I use this to reach the window and widgets
        self.search_entry = self.parent.search_entry

    '''
    Here we create the application index (all apps from /usr/share/applications)
    '''
    def make_index_apps(self):
        for appinfo in Gio.AppInfo.get_all():
            # https://developer.gnome.org/pygobject/stable/class-gioappinfo.html
            if appinfo.supports_files() or appinfo.supports_uris():
                appname = appinfo.get_name()
                appcmd = appinfo.get_commandline()
                self.index_data.append([self.HString.trim(appname, self.trim_limit), self.i, "[app]"])
                self.index_apps_act.append([self.index_data[-1][1], appcmd])  
                self.i = self.i+1

    '''
    Here we create the windows index (all open windows)
    '''
    def make_index_windows(self):
        windows = Wnck.Screen.get_default().get_windows()
        for w in windows:
            self.index_data.append([self.HString.trim(w.get_name(), self.trim_limit), self.i, "[win]"])
            self.index_windows_act.append([self.index_data[-1][0], w.get_xid()])  
            self.i = self.i+1
    '''
    Create index_data and index_final
    '''
    def index(self):
        self.i = 0
        # To avoid duplicate results, empty indexes
        self.index_apps_act = []
        self.index_windows_act = []
        self.index_data = []

        # Generate indexes
        self.make_index_apps()
        self.make_index_windows()
    '''
    Shows a window from its xid
    '''
    def show_window(self, xid):
        print(Wnck.Window.get(xid).activate(time.time()))

    '''
    Search start from here.
    Here I filter the indexes and get the "filter" list
    '''
    def find(self, search_text):
        # Get widgets
        self.results = self.parent.stack.results

        # Check for empty
        if search_text == "":
            self.results.resize(0)
        else:
            # Get data
            self.index_data = []
            self.index()
            found = []
            for f, i, t in self.index_data:
                if search_text in f:
                    found.append([f, i, t])
            if len(found) == 0:
                found.append([self._('I did not find anything'), 0, "[none]"])
            # Resize results box (calculate the number of results not > 250)
            estimated_results_size = len(found) * self.item_height
            if estimated_results_size > 250:
                self.results.resize(250)
            else:
                self.results.resize(estimated_results_size)

            # Return results
            self.results.generate_items(found, True)

    '''
    Check result type and call action
    '''
    def do(self, result):
        if result[2] == "[none]":
            pass
        elif result[2] == "[app]": # Application detected
            for i, a in self.index_apps_act:
                print(i)
                if result[1] == i:
                    os.system(a)
        elif result[2] == "[win]": # Window detected
            for i, x in self.index_windows_act:
                if result[1] == i:
                    self.show_window(x)

