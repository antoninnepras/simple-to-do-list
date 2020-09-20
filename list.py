import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def strike(text):
    i = 0
    new_text = ''
    while i < len(text):
        new_text = new_text + (text[i] + u'\u0336')
        i = i + 1
    return(new_text)

class mainWindow (Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple to-do list")
        self.set_icon_from_file("images/icon.png")
        self.set_resizable(False)

        self.headLabel = Gtk.Label(label="To-do")

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter thing: ")
        self.entry.connect("activate",self.addThing)

        self.addThingButton = Gtk.Button()
        self.addThingButton.set_label("+")
        self.addThingButton.connect("clicked", self.addThing)

        self.deleteButton = Gtk.Button()
        self.deleteButton.set_label("DEL")
        self.deleteButton.connect("clicked",self.deleteThing)

        self.historyButton = Gtk.Button()
        self.historyButton.set_label("HISTORY")
        self.historyButton.connect("clicked",self.showHistory)

        self.mainListBox = Gtk.ListBox()
        self.mainListBox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.mainListBox.show_all()

        self.mainGrid = Gtk.Grid()
        self.mainGrid.attach(self.headLabel, 0,0,2,1)
        self.mainGrid.attach(self.historyButton, 2,0,1,1)
        self.mainGrid.attach(Gtk.HSeparator(), 0,1,2,1)
        self.mainGrid.attach(self.entry, 0,2,1,1)
        self.mainGrid.attach(self.addThingButton, 1,2,1,1)
        self.mainGrid.attach(self.deleteButton,2,2,1,1)
        self.mainGrid.attach(self.mainListBox, 0,3,3,1)
        #self.mainGrid.vexpandable()
        self.add(self.mainGrid)
        self.thingList = []

    def addThing(self, widget):
        thing = Thing()
        thing.number = len(self.thingList)
        thing.text = self.entry.get_text()
        self.entry.set_text("")
        thing.make_row()
        self.mainListBox.add(thing.row)
        self.thingList.append(thing)
        self.mainListBox.show_all()

    def deleteThing(self,widget):
        print("deleting")
        for i in self.mainListBox.get_selected_rows():
            self.mainListBox.remove(i)

    def showHistory(self,widget):
        historyWindow = HistoryWindow()
        historyWindow.list = self.thingList
        historyWindow.makeHistory()
        historyWindow.show_all()

class Thing():
    def __init__(self):
        self.number = 0
        self.text = ""
        self.row = Gtk.ListBoxRow()
        self.label = Gtk.Label()
        self.doneButton = Gtk.Button(label="DONE")
        self.doneButton.connect("clicked",self.done)
        self.doneButton.set_margin_right(True)
        self.undoneButton = Gtk.Button(label="NOT DONE")
        self.undoneButton.connect("clicked",self.undone)
        self.undoneButton.set_sensitive(False)

    def make_row(self):
        self.label.set_label(self.text)
        self.label.set_hexpand(True)
        self.grid = Gtk.Grid()
        self.grid.attach(self.label,0,0,1,1)
        self.grid.attach(self.doneButton,1,0,1,1)
        self.grid.attach(self.undoneButton,2,0,1,1)
        self.grid.set_hexpand(True)
        self.row.add(self.grid)

    def done(self,widget):
        text = self.label.get_text()
        text = strike(text)
        self.label.set_label(text)
        self.doneButton.set_sensitive(False)
        self.undoneButton.set_sensitive(True)

    def undone(self,widget):
        self.label.set_label(self.text)
        self.undoneButton.set_sensitive(False)
        self.doneButton.set_sensitive(True)

class HistoryWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="History")
        self.connect("destroy",self.exit)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.list = []

        self.mainLabel = Gtk.Label(label = "History")
        self.mainLabel.set_width_chars(30)
        self.mainListBox = Gtk.ListBox()

        self.mainGrid = Gtk.Grid()
        self.mainGrid.attach(self.mainLabel,0,0,1,1)
        self.mainGrid.attach(self.mainListBox,0,1,1,1)
        self.add(self.mainGrid)

    def makeHistory(self):
        for i in self.list:
            label = Gtk.Label(label = i.text)
            row = Gtk.ListBoxRow()
            row.add(label)
            self.mainListBox.add(row)
            self.mainListBox.show_all()

    def exit(self,widget):
        self.close()

mainWindow = mainWindow()
mainWindow.connect("destroy",Gtk.main_quit)
mainWindow.show_all()
Gtk.main()
