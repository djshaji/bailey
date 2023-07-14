import sys, os
import glob
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
from gi.repository.GdkPixbuf import Pixbuf

class UI(Gtk.ApplicationWindow):
    box = None
    iconSize = 64
    icons = ["edit-cut", "edit-paste", "edit-copy"]

    def openHome (self, data = None):
        self.openFolder (os.path.expanduser ("~"))

    def openFolder (self, path):
        files = glob.glob (path + "/*")
        # print (files)
        self.liststore.clear ()
        for f in files:
            if os.path.isdir (f):
                pixbuf = Pixbuf.new_from_file ("icons/folder.svg")
                self.liststore.append ([pixbuf, os.path.basename (f), f])

    def button (self, filename):
        image = Gtk.Image.new_from_file (filename)
        button = Gtk.Button (child=image)
        button.set_has_frame (False)
        button.set_size_request (self.iconSize, self.iconSize)
        return button
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here
        self.set_size_request (800, 600)
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        # ~ self.header.set_show_title_buttons (False)

        self.box = Gtk.Box ()
        self.box.set_orientation (1)
        self.set_child (self.box)
        
        back = self.button ("icons/go-previous.svg")
        self.header.pack_start (back)
        home = self.button ("icons/go-home.svg")
        self.header.pack_start (home)
        home.connect ("clicked", self.openHome)

        self.bar = Gtk.Entry ()
        self.bar.set_hexpand (True)
        self.header.set_title_widget (self.bar)
        
        go = self.button ("icons/go-next.svg")
        self.header.pack_end (go)

        self.iconview = Gtk.IconView ()
        self.sw = Gtk.ScrolledWindow ()
        self.sw.set_child (self.iconview)
        self.liststore = Gtk.ListStore(Pixbuf, str, str)
        self.iconview.set_model(self.liststore)
        self.iconview.set_pixbuf_column(0)
        self.iconview.set_text_column(1)
        self.box.append (self.sw)
        self.sw.set_hexpand (True)
        self.sw.set_vexpand (True)
