from tkinter import *
from tkinter import filedialog
import json

root = Tk()
root.title('Laboratory 1')
root.geometry('1200x660')

global selected
selected = False


# new file function
def new_file():
    # clear previous text
    my_text.delete('1.0', END)

    # update status bars
    root.title('New File')
    status_bar.config(text='New File       ')


# cut text
def cut_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # delete selected text from textbox
        my_text.delete("sel.first", "sel.last")
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# copy text
def copy_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste text
def paste_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif selected:
        position = my_text.index(INSERT)
        my_text.insert(position, selected)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)
        # use start += 1 to find overlapping matches


# open file function
def open_file():
    # clear previous text
    my_text.delete('1.0', END)

    # get file name
    text_file = filedialog.askopenfilename(
        initialdir='lab1/Audit Files/',
        title='Open File', filetypes=(('All Files', '*.*'),))

    # update status bars
    name = text_file
    status_bar.config(text=f'{name}       ')
    name = name.replace('lab1/', '')
    root.title(f'{name} - Dvorac Ana')

    # open file
    text_file = open(text_file, 'r')
    contents = text_file.read()

    contents = contents.replace('            :', ':')
    contents = contents.replace('           :', ':')
    contents = contents.replace('          :', ':')
    contents = contents.replace('         :', ':')
    contents = contents.replace('        :', ':')
    contents = contents.replace('       :', ':')
    contents = contents.replace('      :', ':')
    contents = contents.replace('     :', ':')
    contents = contents.replace('    :', ':')
    contents = contents.replace('   :', ':')
    contents = contents.replace('  :', ':')
    contents = contents.replace(' :', ':')

    start = list(find_all(contents, '<custom_item>'))
    ending = list(find_all(contents, '</custom_item>'))

    custom_item = {}

    custom_item['CMD_EXEC'] = {'type': [], 'description': [], 'cmd': [], 'expect': []}
    custom_item['MACOSX_DEFAULTS_READ'] = {'type': [], 'description': [], 'regex': [], 'plist_item': [], 'plist_name ': [], 'plist_option': []}
    custom_item['FILE_CONTENT_CHECK'] = {'type': [], 'description': []}
    custom_item['FILE_CONTENT'] = {'type': [], 'description': []}
    custom_item['FILE_CONTENT_CHECK_NOT'] = {'type': [], 'description': []}
    custom_item['BANNER_CHECK'] = {'type': [], 'description': []}
    
    general_custom_item = {}
    general_custom_item_keys = []

    for key in custom_item:
        keys_list = list(custom_item[key])
        for key_x in keys_list:
            if key_x not in general_custom_item_keys:
                general_custom_item_keys.append(key_x)
    for key in general_custom_item_keys:
        general_custom_item[key] = []

    for i in range(len(start)):
        content_type_block = contents[start[i] + 13: ending[i]]
        for element in list(general_custom_item.keys()):
            element_length = len(element) + 1
            if content_type_block.find(element) != -1:
                general_custom_item[element].append(content_type_block[content_type_block.find(element + ':') + element_length: content_type_block[content_type_block.find(element + ':') + element_length:].find('\n') + content_type_block.find(element + ':') + element_length].strip())
            else:
                general_custom_item[element].append('')

    to_json = []
    for i in range(len(general_custom_item['type'])):
        to_print = {}
        for element in list(general_custom_item.keys()):
            if general_custom_item[element][i] != '':
                to_print[element] = general_custom_item[element][i]
        to_json.append(to_print)

    my_text.insert(END, json.dumps(to_json, indent=4))

    # close file
    text_file.close()


# save as file function
def save_as_file():
    text_file = filedialog.asksaveasfilename(
        defaultextension='.*',
        initialdir='lab1/Audit Files/',
        title='Save File', filetypes=(('All Files', '*.*'),))
    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}       ')
        name = name.replace('lab1/Audit Files/', '')
        root.title(f'{name} - Dvorac Ana')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # close file
        text_file.close()


def export():
    text_file = filedialog.askopenfilename(
        defaultextension='.*',
        initialdir='lab1/Audit Files/',
        title='Save File', filetypes=(('All Files', '*.*'),))

    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}      ')
        name = name.replace('lab1/Audit Files/', '')
        root.title(f'{name} - Dvorac Ana')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # close file
        text_file.close()


# main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# text box scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# horizontal scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16),
               selectbackground="yellow", selectforeground="black",
               undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()

# configure scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_command(label='Export', command=export)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# bottom status bar
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

root.mainloop()