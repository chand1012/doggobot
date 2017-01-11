from tkinter import *
from tkinter import messagebox
import sys, os
import json

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

def json_window(): # fix this
    json_window = Toplevel(root)
    json_window.title('JSON Generate')
    id_text = Label(json_window, text="Imgur API Client ID")
    id_text.grid(row=0)
    id_str = StringVar()
    id_box = Entry(json_window, bd=3, textvariable=id_str)
    id_box.grid(row=0, column=1)

    imgur_secret_text = Label(json_window, text="Imgur Client secret")
    imgur_secret_text.grid(row=0)
    imgur_secret = StringVar()
    imgur_secret_box = Entry(json_window, bd=3, textvariable=imgur_secret)
    imgur_secret_box.grid(row=0, column=1)

    consumer_key_text = Label(json_window, text="Twitter consumer key")
    consumer_key_text.grid(row=0)
    consumer_key = StringVar()
    consumer_key_box = Entry(json_window, bd=3, textvariable=consumer_key)
    consumer_key_box.grid(row=0, column=1)

    consumer_secret_text = Label(json_window, text="Twitter consumer secret key")
    consumer_secret_text.grid(row=0)
    consumer_secret = StringVar()
    consumer_secret_box = Entry(json_window, bd=3, textvariable=consumer_secret)
    consumer_secret_box.grid(row=0, column=1)

    access_token_text = Label(json_window, text="Twitter access token")
    access_token_text.grid(row=0)
    access_token = StringVar()
    access_token_box = Entry(json_window, bd=3, textvariable=access_token)
    access_token_box.grid(row=0, column=1)

    access_secret_text = Label(json_window, text="Twitter access token")
    access_secret_text.grid(row=0)
    access_secret = StringVar()
    access_secret_box = Entry(json_window, bd=3, textvariable=access_secret)
    access_secret_box.grid(row=0, column=1)

    makebutton = Button(json_window, text="Start", command= lambda: json_gen('keys.json', id_str.get(), imgur_secret.get(), consumer_key.get(), consumer_secret.get(), access_token.get(), access_secret.get()))
    makebutton.grid(row=6, column=1)

def json_gen(filename, imgurid, imgursecret, consumerkey, consumersecret, access, accesssecret):
    data = {}
    data["client_id_imgur"] = imgurid
    data["client_secret_imgur"] = imgursecret
    data["tw_consumer_key"] = consumerkey
    data["tw_consumer_secret"] = consumersecret
    data["access_token"] = access
    data["access_secret"] = accesssecret

    json_data = json.dumps(data)
    json_file = open(filename, 'w+')
    json_file.write(json_data)
    json_file.close()

    messagebox.showinfo('JSON Generation', 'JSON file successfully written!')

def help_window():
    top = Toplevel(root)
    top.iconbitmap(icon)
    top.title("Help")
    helptext = '''
    Keyfile - File in which the keys are stored.
    If file is not found, you can generate one by pressing the generate Button
    Text - Text for the Tweet
    Search - Search for the Imgur query
    Limit - Number of allowed Precached photos
    Time - Number of minutes between posts
    '''
    helptextitem = Label(top, text=helptext).pack()
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

json_button = Button(root, text="JSON", command=json_window)
json_button.grid(row=7)

root.title("Doggobot")
try:
    root.iconbitmap(icon)
except:
    pass
root.mainloop()
