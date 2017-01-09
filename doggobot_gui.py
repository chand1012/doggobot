from tkinter import *
import sys, os

global python
global icon
appdata = os.getenv('APPDATA')
if 'win32' in sys.platform: #change this to a settings file to add the python executeable
    icon = r'{}/doggobot/icon.ico'.format(appdata)
    python = 'python'
else:
    icon = r'./data/icon.ico'
    python = 'python3'

root = Tk()

def help_window():
    top = Toplevel(root)
    #add more stuff to this
    kill = Button(top,text='Close',command=top.destroy).pack()

def execute_bot(array):
    if array[5] is True:
        clear_command = '-c'
    else:
        clear_command = ''
    command_string = "{} doggobot.py -f {} -text {} -s {} -l {} -t {} {}".format(python, array[0], array[1], array[2], array[3], array[4], clear_command)
    print("Using command string:\n{}".format(command_string))
    os.system(command_string)

def get_command_arguments():
    global arguments
    arguments = []
    if keyfile.get() is "":
        arguments += ["keys.json"]
    else:
        arguments += [keyfile.get()]

    if text.get() is "":
        arguments += ["#doggobot"]
    else:
        arguments += [text.get()]

    if search.get() is "":
        arguments += ["dogs"]
    else:
        arguments += [search.get()]

    if limit.get() is "":
        arguments += ["1"]
    else:
        arguments += [limit.get()]

    if time.get() is "":
        arguments += ["30"]
    else:
        arguments += [time.get()]

    arguments += [clear.get()]
    print(arguments)
    execute_bot(arguments)

def help_command():
    if sys.platform is 'linux':
        os.system("xdg-open http://github.com/chand1012/doggobot")
    elif sys.platform is 'win32':
        os.system('start "" http://github.com/chand1012/doggobot')

keyfile_text = Label(root, text="Keyfile")
keyfile_text.grid(row=0)
keyfile = StringVar()
keyfile_box = Entry(root, bd=3, textvariable=keyfile)
keyfile_box.grid(row=0, column=1)

text_text = Label(root, text="Post text")
text_text.grid(row=1)
text = StringVar()
text_box = Entry(root, bd=3, textvariable=text)
text_box.grid(row=1, column=1)

search_text = Label(root, text="Search query text")
search_text.grid(row=2)
search = StringVar()
search_box = Entry(root, bd=3, textvariable=search)
search_box.grid(row=2, column=1)

limit_text = Label(root, text="Precached photo limit")
limit_text.grid(row=3)
limit = StringVar()
limit_box = Entry(root, bd=3, textvariable=limit)
limit_box.grid(row=3, column=1)

time_text = Label(root, text="Time between posts")
time_text.grid(row=4)
time = StringVar()
time_box = Entry(root, bd=3, textvariable=time)
time_box.grid(row=4, column=1)

clear = BooleanVar()
clear_box = Checkbutton(root, text="Clear cache?", variable=clear, onvalue=True, offvalue=False, height=5, width=20)
clear_box.grid(row=5)

button = Button(root, text="Start", command=get_command_arguments)
button.grid(row=6, column=1)

help_button = Button(root, text="Help", command=help_window)
help_button.grid(row=6)

root.title("Doggobot")
try:
    root.iconbitmap(icon)
except:
    pass
root.mainloop()
