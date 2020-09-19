from tkinter import *
from greedy import maxcover_by_min_items
import sys
from io import StringIO


def makemenu(parent):
    menubar = Frame(parent)
    buttonbar = Frame(parent)
    mainwin1 = Frame(parent)
    mainwin2 = Frame(parent)
    mainwin3 = Frame(parent)
    menubar.pack(side=TOP, fill=X)
    buttonbar.pack(side=BOTTOM, fill = X)
    mainwin3.pack(side=BOTTOM)
    mainwin1.pack(side=LEFT)
    mainwin2.pack(side=LEFT)
    helpbutton = Menubutton(menubar, text='Help', underline=0)
    helpbutton.pack(side=RIGHT)
    help = Menu(helpbutton, tearoff=False)
    help.add_command(label='about', command=maketextwin, underline=0)
    helpbutton.config(menu=help)
    personsbutton = Menubutton(menubar, text='Persons', underline=0)
    personsbutton.pack(side=LEFT)
    persons = Menu(personsbutton, tearoff=False)
    personsbutton.config(menu=persons)
    submenu = Menu(persons, tearoff=False)
    submenu.add_command(label='add hated persons', command=(lambda: makeform(database1)), underline=0)
    submenu.add_command(label='add haters', command=(lambda: makeform(database2)), underline=0)
    persons.add_cascade(label='manually', menu=submenu, underline=0)
    genlists1 = Button(buttonbar, text='show hated', command=(lambda: showlists(mainwin1, 'hated', database1)))
    genlists1.pack(side=LEFT)
    genlists2 = Button(buttonbar, text='show haters', command=(lambda: showlists(mainwin2, 'haters', database2)))
    genlists2.pack(side=LEFT)
    showresults = Button(buttonbar, text='show results', command=(lambda: showres(mainwin3, database1, database2, database3)))
    showresults.pack(side=RIGHT)
    calculate = Button(buttonbar, text='calculate', command=(lambda: maxcover_by_min_items(database1, database3)))
    calculate.pack(side=RIGHT)
    # return menubar


def maketextwin(inserted_text=open('help.txt', 'r').read()):
    parent = Toplevel()
    parent.title('help')
    sbar = Scrollbar(parent)
    text = Text(parent, relief=SUNKEN)
    sbar.config(command=text.yview)
    text.config(yscrollcommand=sbar.set)
    sbar.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, expand=YES, fill=BOTH)
    text.insert('1.0', inserted_text)


def getdata(variables, database):
    database.append(variables.get())
    return database


def makeform(database=[]):
    var = StringVar()
    parent = Toplevel()
    parent.title('Input names manually')
    win1 = Frame(parent)
    win2 = Frame(parent)
    lab = Label(win1, width=5, text='name')
    ent = Entry(win1)
    adb = Button(win2, text='add person to list', command=(lambda: getdata(var, database)))
    win1.pack(side=TOP, fill=BOTH)
    win2.pack(side=BOTTOM, fill=BOTH)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    adb.pack(side=LEFT)
    ent.config(textvariable=var)


def showlists(parent, name, data):
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
        pos+=1
    # list.config(selectmode=SINGLE, setgrid=1)
    list.bind('<Double-1>', handlelist)


def handlelist(event):
    data = database1
    widget = event.widget
    index = widget.curselection()
    label = widget.get(index)
    parent = Toplevel()
    parent.title(f'persons, hated by {label}')
    sbar = Scrollbar(parent)
    list = Listbox(parent)
    addperson = Button(parent, text='add person to list', command=(lambda: selectedlist(list, label)))
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


def selectedlist(list, label):
    index = list.curselection()
    data = []
    for i in index:
        data.append(database1[i])
    database3[label] = set(data)


def showres(parent, data1, data2, data3):
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


root = Tk()
root.title('HATER GUI')
database1 = []
database2 = []
database3 = {}
root.geometry("500x500")
makemenu(root)
root.mainloop()





