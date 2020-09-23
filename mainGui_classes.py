from tkinter import *
from greedy import maxcover_by_min_items
import sys
from io import StringIO


class Handlers:
    def start(self):
        self.database1=[]
        self.database2=[]
        self.database3={}

    def maketextwin(self, inserted_text=open('help.txt', 'r').read()):
        parent = Toplevel()
        parent.title('help')
        sbar = Scrollbar(parent)
        text = Text(parent, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.insert('1.0', inserted_text)

    def getdata(self, variables, database):
        database.append(variables.get())
        return database

    def makeform(self, database=[]):
        var = StringVar()
        parent = Toplevel()
        parent.title('Input names manually')
        win1 = Frame(parent)
        win2 = Frame(parent)
        lab = Label(win1, width=5, text='name')
        ent = Entry(win1)
        adb = Button(win2, text='add person to list', command=(lambda: self.getdata(var, database)))
        win1.pack(side=TOP, fill=BOTH)
        win2.pack(side=BOTTOM, fill=BOTH)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        adb.pack(side=LEFT)
        ent.config(textvariable=var)

    def showlists(self, parent, name, data):
        for widget in parent.winfo_children():
            widget.destroy()
        mainwindow = Frame(parent)
        Label(parent, text=name).pack(side=TOP)
        mainwindow.pack(side=LEFT)
        sbar = Scrollbar(mainwindow)
        list = Listbox(mainwindow)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for i in data:
            list.insert(pos, i)
            pos += 1
        # list.config(selectmode=SINGLE, setgrid=1)
        list.bind('<Double-1>', self.handlelist)

    def handlelist(self, event):
        data = self.database1
        widget = event.widget
        index = widget.curselection()
        label = widget.get(index)
        parent = Toplevel()
        parent.title(f'persons, hated by {label}')
        sbar = Scrollbar(parent)
        list = Listbox(parent)
        addperson = Button(parent, text='add person to list', command=(lambda: self.selectedlist(list, label)))
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        addperson.pack(side=BOTTOM)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for i in data:
            list.insert(pos, i)
            pos += 1
        list.config(selectmode=EXTENDED, setgrid=1)

    def selectedlist(self, list, label):
        index = list.curselection()
        data = []
        for i in index:
            data.append(self.database1[i])
        self.database3[label] = set(data)

    def showres(self, parent, data1, data2, data3):
        for widget in parent.winfo_children():
            widget.destroy()
        buff = StringIO()
        temp = sys.stdout
        sys.stdout = buff
        print('here - the list of hated persons, inputted by you before:')
        for i in data1:
            print(i)
        print('here - the list of haters:')
        for i in data2:
            print(i)
        print('here - the list of haters WITH hated persons:')
        for key in data3:
            print(key)
            for value in data3[key]:
                print('    ', value)
        print('and here - the minimum list of haters, who covers hated persons:')
        result = maxcover_by_min_items(data1, data3)
        for i in result:
            print(i)
        text = Text(parent)
        sbar = Scrollbar(parent)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        text.delete('1.0', END)
        text.insert('1.0', buff.getvalue())
        sys.stdout = temp


class MainWin(Handlers):
    def __init__(self, parent):
        mainwin1 = Frame(parent)
        mainwin2 = Frame(parent)
        mainwin3 = Frame(parent)
        mainwin4 = Frame(parent)
        mainwin5 = Frame(parent)
        mainwin1.pack(side=TOP, fill=X)
        mainwin5.pack(side=BOTTOM, fill=X)
        mainwin4.pack(side=BOTTOM, fill=X)
        mainwin2.pack(side=LEFT)
        mainwin3.pack(side=LEFT)
        self.start()
        self.buttons = [('show hated', lambda: self.showlists(mainwin2, 'hated', self.database1), {'side': LEFT}),
                        ('show haters', lambda: self.showlists(mainwin3, 'haters', self.database2), {'side': LEFT}),
                        ('show results', lambda: self.showres(mainwin4, self.database1, self.database2, self.database3), {'side': RIGHT}),
                        ('calculate', lambda: maxcover_by_min_items(self.database1, self.database3), {'side': RIGHT})]
        self.makemenubar(mainwin1)
        self.makebuttons(mainwin5)

    def makemenubar(self, parent):
        helpbutton = Menubutton(parent, text='Help', underline=0)
        helpbutton.pack(side=RIGHT)
        help = Menu(helpbutton, tearoff=False)
        help.add_command(label='about', command=self.maketextwin, underline=0)
        helpbutton.config(menu=help)
        personsbutton = Menubutton(parent, text='Persons', underline=0)
        personsbutton.pack(side=LEFT)
        persons = Menu(personsbutton, tearoff=False)
        personsbutton.config(menu=persons)
        submenu = Menu(persons, tearoff=False)
        submenu.add_command(label='add hated persons', command=(lambda: self.makeform(self.database1)), underline=0)
        submenu.add_command(label='add haters', command=(lambda: self.makeform(self.database2)), underline=0)
        persons.add_cascade(label='manually', menu=submenu, underline=0)

    def makebuttons(self, parent):
        for (name, action, where) in self.buttons:
            button = Button(parent, text=name, command=action)
            button.pack(where)


root = Tk()
root.title('HATER GUI')
root.geometry("500x500")
mainwin = MainWin(root)
root.mainloop()
