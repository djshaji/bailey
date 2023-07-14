import magic
from textwrap import shorten
import sys, os
import glob
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
from gi.repository.GdkPixbuf import Pixbuf

class UI(Gtk.ApplicationWindow):
    box = None
    app = None
    iconSize = 600
    icons = ["edit-cut", "edit-paste", "edit-copy"]

    def goUp (self, data = None):
        self.openFolder (os.path.dirname (self.currentFolder))

    def onclick (self, iconview, path):
        iter = self.liststore.get_iter (path)
        filename = self.liststore.get_value (iter, 3)
        if os.path.isdir (filename):
            self.openFolder (filename)

    def getIcon (self, mimeType):
        fileType = mimeType.split ("/") [0]
        filename = glob.glob (f"icons/Chicago95/mimes/scalable/{fileType}*")
        if len (filename) == 0:
            return "icons/file.svg"

        return filename [0]

    def openHome (self, data = None):
        self.openFolder (os.path.expanduser ("~"))

    def openFolder (self, path):
        self.progress.show ()
        self.spinner.start ()
        self.currentFolder = path
        files = glob.glob (path + "/*")
        sorted(files, key=os.lstat)

        # print (files)
        self.liststore.clear ()
        self.bar.set_text (path)
        total = len (files)
        count = 0 
        for f in files:
            self.progress.set_fraction (float (count) / float (total))
            # print (float (count) / float (total))
            count += 1
            if os.path.isdir (f):
                pixbuf = Pixbuf.new_from_file_at_size ("icons/folder.svg", self.iconSize, self.iconSize)
            elif os.path.islink (f):
                print (f)
            else:
                m = magic.detect_from_filename (f)[0]
                icon = self.getIcon (m)
                if m.startswith ("image"):
                    icon = f
                pixbuf = Pixbuf.new_from_file_at_size (icon, self.iconSize, self.iconSize)

            self.liststore.append ([pixbuf, shorten (os.path.basename (f), 20), os.path.basename (f),f])

        self.spinner.stop ()
        self.progress.hide ()

    def button (self, filename):
        image = Gtk.Image.new_from_file (filename)
        button = Gtk.Button (child=image)
        button.set_has_frame (False)
        button.set_size_request (64, 64)
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
        back.connect ("clicked", self.goUp)
        home = self.button ("icons/go-home.svg")
        self.header.pack_start (home)
        home.connect ("clicked", self.openHome)

        self.bar = Gtk.Entry ()
        self.bar.set_hexpand (True)
        self.header.set_title_widget (self.bar)
        
        go = self.button ("icons/go-next.svg")
        self.header.pack_end (go)

        self.spinner = Gtk.Spinner ()
        self.header.pack_start (self.spinner)

        self.iconview = Gtk.IconView ()
        self.sw = Gtk.ScrolledWindow ()
        self.sw.set_child (self.iconview)
        self.liststore = Gtk.ListStore(Pixbuf, str, str, str)
        self.iconview.set_model(self.liststore)
        self.iconview.set_pixbuf_column(0)
        self.iconview.set_text_column(1)
        self.iconview.set_tooltip_column(2)
        self.iconview.set_item_width (120)
        self.iconview.set_activate_on_single_click (True)
        self.iconview.connect ("item-activated", self.onclick)

        self.box.append (self.sw)

        self.progress = Gtk.ProgressBar ()
        self.box.append (self.progress)
        self.sw.set_hexpand (True)
        self.sw.set_vexpand (True)

        self.maximize ()
        self.openHome ()
