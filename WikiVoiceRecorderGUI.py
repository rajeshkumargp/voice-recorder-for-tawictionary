import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import record
import subprocess
import os

class WikiVoiceRecorder(Gtk.Window):

    def __init__(self):
        global WIKI_WORDS
        WIKI_WORDS = []

        WIKI_WORDS = self.getwordslist()

        Gtk.Window.__init__(self, title="Wiki Voice Recorder")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.getawordbutton = Gtk.Button.new_with_label("Get a word")
        self.getawordbutton.connect("clicked", self.on_getaword_clicked)
        vbox.pack_start(self.getawordbutton, True, True, 0)

        self.showWordlabel = Gtk.Label(
            "Words will be displayed here ...")
        #showWordlabel.set_justify(Gtk.Justification.RIGHT)
        vbox.pack_start(self.showWordlabel, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        #self.add(hbox)

        self.recordbutton = Gtk.Button.new_with_label("Record")
        self.recordbutton.connect("clicked", self.on_record_clicked,self.showWordlabel.get_text())
        hbox.pack_start(self.recordbutton, True, True, 0)

        playbutton = Gtk.Button.new_with_label("Play")
        playbutton.connect("clicked", self.on_play_clicked,self.showWordlabel.get_text())
        hbox.pack_start(playbutton, True, True, 0)

        uploadbutton = Gtk.Button.new_with_label("Upload")
        uploadbutton.connect("clicked", self.on_upload_clicked)
        hbox.pack_start(uploadbutton, True, True, 0)

        vbox.pack_start(hbox,True,True,0)

        logoutbutton = Gtk.Button.new_with_mnemonic("Close")
        logoutbutton.connect("clicked", self.on_close_clicked)
        vbox.pack_start(logoutbutton, True, True, 0)

    def on_getaword_clicked(self, button):
        print("Get a word Button is clicked")
        if len(WIKI_WORDS) > 0 :
            print(WIKI_WORDS[0])
            self.showWordlabel.set_text(WIKI_WORDS[0].replace('\n', ''))
            del WIKI_WORDS[:1]

        else:
            print("Refresh Word List")
            self.showWordlabel.set_text("List is empty")


    def on_record_clicked(self, button,wikiword):
        print("Record Button is clicked")
        print(wikiword)

        print(self.showWordlabel.get_text())
        wikiword = self.showWordlabel.get_text()
        record.record_audio(wikiword)
        subprocess.call(["oggenc", '-Q', wikiword + '.wav'])


    def on_play_clicked(self, button,wikiword):

        print("Play Button is clicked")
        print(wikiword)
        print(self.showWordlabel.get_text())
        wikiword = self.showWordlabel.get_text()

        os.system("ogg123 " + wikiword + ".ogg")

    def on_upload_clicked(self, button):
        print("Upload Button is clicked")

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()

    def getwordslist(self):
        fin = open('file', "r")
        WIKI_WORDS = fin.readlines()
        fin.close()
        return WIKI_WORDS

win = WikiVoiceRecorder()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
