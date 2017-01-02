from tkinter import *
import sys, os

root = Tk()


def execute_bot(array):
    if array[5] is True:
        clear_command = '-c'
    else:
        clear_command = ''
    command_string = "python doggobot.py -f {} -text {} -s {} -l {} -t {} {}".format(array[0], array[1], array[2], array[3], array[4], clear_command)
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

root.mainloop()
