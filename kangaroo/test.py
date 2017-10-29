from gi.repository import Gtk
from gi.repository import Gio
import sys


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="GMenu Example", application=app)


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        # start the application
        Gtk.Application.do_startup(self)

        # create a menu
        menu = Gio.Menu()
        # append to the menu three options
        menu.append("New", "app.new")
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")
        # set the menu as menu of the application
        self.set_app_menu(menu)

        # create an action for the option "new" of the menu
        new_action = Gio.SimpleAction.new("new", None)
        # connect it to the callback function new_cb
        new_action.connect("activate", self.new_cb)
        # add the action to the application
        self.add_action(new_action)

        # option "about"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        # option "quit"
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    # callback function for "new"
    def new_cb(self, action, parameter):
        print("This does nothing. It is only a demonstration.")

    # callback function for "about"
    def about_cb(self, action, parameter):
        print("No AboutDialog for you. This is only a demonstration.")

    # callback function for "quit"
    def quit_cb(self, action, parameter):
        print("You have quit.")
        self.quit()

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
