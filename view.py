# coding: utf-8
"""
Tkinter View of the project.

"""

from __future__ import absolute_import
import tkinter as tk
from tkinter import *
from tkinter import Menu, Frame
from tkinter.messagebox import askyesno, askokcancel, showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import ttk
from tkinter.messagebox import showinfo
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from PIL import Image, ImageTk
import pyscreenshot
import webbrowser
import asyncio
# Python scripts containing the classes (import from a local file)
from customtext import CustomText
from tooltip import CreateToolTip

# import random
# import time
# Backend graphic used to show the tree plot
matplotlib.use('TkAgg')


class View(Tk):
    '''
    Class for the Tkinter view
    '''

    def __init__(self, controller):
        '''
        Constructor for the Tkinter view.
        '''
        super().__init__()
        self.controller = controller
        self.entries = ["Entry"]
        # A dictionnary to store the entries
        self.widgets_entry = {}
        # A dictionnary to store the buttons
        self.widgets_button = {}
        # A dictionnary to store the labels of the progress tracker
        self.progress_labels = {}
        # A dictionnary to store the images of the progress tracker
        self.progress_images = {}
        # List containing the 4 stages of the sequence in the Model
        self.sequence = ['DNA Motif', 'BWT Coded',
                         'Decompressed', 'Compressed']
        # List of possible operations of model manipulation
        self.data_buttons = ["Load"]
        # List of the necessary buttons for the BWT's operations
        self.buttons_BWT = ["Generate Code",
                            "Reconstruct", "Next", "Final Result"]
        # List of the necessary buttons for the Huffman's operations
        self.buttons_huffman = ["Compress",
                                "Decompress", "Next", "Final Result"]

    def get_value(self):
        '''
        Returns the values introduced by the user.
        '''
        # Fetching the entry of the app
        entry_fetch = self.widgets_entry["Entry"].get()
        # The first time get_value is called it's going to create an internal
        # Attribute original_value which the role is to set the entry value
        # If the user decides not to destroy his object.
        self.original_value = entry_fetch
        return entry_fetch

    def create_frames(self):
        '''
        The goal of this function is to create the frames of the graphical
        interface
        '''
        # Creation of frame0 which is the highest frame
        self.frame0 = Frame(self, bg="White", height=100, width=400)
        self.frame0.grid(row=0, column=0)
        # Creation of frame_entry_load_save which is the highest frame which
        # contains the entry, load and save buttons
        self.frame_entry_load_save = Frame(
            self, bg="White", height=20, width=400, bd=10)
        self.frame_entry_load_save.grid(row=0, column=1)
        # Creation of frame_progress which is the highest frame which
        # contains the real-time tracker of the sequence
        self.frame_progress = Frame(
            self, bg="White", height=20, width=400)
        self.frame_progress.grid(row=1, column=0, rowspan=2, sticky='N')
        self.informations = Frame(
            self, bg="White", height=20, width=400, bd=10)
        self.informations.grid(row=3, column=0)
        self.frame_git = Frame(
            self, bg="White", height=20, width=400, bd=10)
        self.frame_git.grid(row=6, column=0, rowspan=2)
        # Creation of frame_label_BWT which is the highest frame which
        # contains the label message of BWT
        self.frame_label_BWT = Frame(
            self, height=10, width=450)
        self.frame_label_BWT.grid(row=1, column=1, sticky='WE')
        # Creation of frame_buttons_BWT which is the highest frame which
        # contains the buttons of BWT
        self.frame_buttons_BWT = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_buttons_BWT.grid(row=2, column=1)
        # Creation of frame_results_BWT which is the highest frame which
        # contains the results of BWT
        self.frame_results_BWT = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_results_BWT.grid(row=3, column=1, sticky='W')
        # Creation of frame_label_huffman which is the highest frame which
        # contains the label message of BWT
        self.frame_label_huffman = Frame(
            self, height=10, width=400)
        self.frame_label_huffman.grid(row=4, column=1, sticky='WE')
        # Creation of frame_buttons_huffman which is the highest frame which
        # contains the buttons of Huffman
        self.frame_buttons_huffman = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_buttons_huffman.grid(row=5, column=1)
        # Creation of frame_results_huffman which is the highest frame which
        # contains the results of Huffman
        self.frame_results_huffman = Frame(self, bg="White", height=10, width=400, bd=10,
                                           cursor="target")
        self.frame_results_huffman.grid(row=6, column=1,  sticky='W')

    def create_menu(self):
        '''
        For the creation of the top menubar of the interface
        '''
        # Create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)
        # Create the file_menu
        file_menu = Menu(menubar, tearoff=0)
        # Add menu items to the File menu
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open...')
        file_menu.add_command(label='Close')
        file_menu.add_separator()
        # Add a submenu
        sub_menu = Menu(file_menu, tearoff=0)
        # Listing all the available themes to configure the tkinter window
        sub_menu.add_command(
            label='classic', command=lambda: self.s.theme_use('classic'))
        sub_menu.add_command(
            label='alt', command=lambda: self.s.theme_use('alt'))
        sub_menu.add_command(
            label='clam', command=lambda: self.s.theme_use('clam'))
        sub_menu.add_command(
            label='default', command=lambda: self.s.theme_use('default'))
# TODO Add shi lal color
        # Add the File menu to the menubar
        file_menu.add_cascade(label="Themes", menu=sub_menu)
        screen_menu = Menu(file_menu, tearoff=0)
        screen_menu.add_command(
            label='Fullscreen', command=lambda: self.attributes("-fullscreen", True))
        screen_menu.add_command(
            label='Windowed', command=lambda: self.attributes("-fullscreen", False))
        # Add the Screen menu to the file menubar
        file_menu.add_cascade(label="Display", menu=screen_menu)
        # Create the tools menu
        tools_menu = Menu(file_menu, tearoff=0)
        # Add the screenshot command
        tools_menu.add_command(
            label='Screenshot', command=lambda: asyncio.run(self.screenshot()))
        # Add Exit menu item
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        menubar.add_cascade(label="Tools", menu=tools_menu, underline=0)
        # Create the Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')
        # Add the Help menu to the menubar
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

    async def screenshot(self):
        '''
        Method to take a screenshot using pyscreenshot
        '''
        # If the screen is not fullscreen, make it full screen
        if not self.attributes("-fullscreen"):
            self.attributes("-fullscreen", True)
            # Waits one second
            await asyncio.sleep(1)
        file_path = asksaveasfilename(defaultextension='.png')
        # If the file_path has been validated, show the image and save it
        if file_path:
            # Waits one second
            await asyncio.sleep(1)
            image = pyscreenshot.grab()
            image.show()
            image.save(file_path)
        # Ends with Windowed mode (not fullscreen)
        self.attributes("-fullscreen", False)

    def create_labels(self):
        '''
        Used to create the different lables of the interface
        '''
        # Label of entry instructions
        label_top = ttk.Label(
            self.frame_entry_load_save, text='Please type in your sequence, or load one.')
        label_top.grid(row=0, column=0)
        # Instructions
        informations = Label(
            self.informations, text='By observing the tracker above,\nyou can get real-time information\nabout the sequence.\nThe program automatically detects\nthe possible operations.\nRefer to README for more info.', font=('Arial 24'))
        # Will make the background of the entry seem "transparent"
        informations['bg'] = self['bg']
        # Reference for the label.image being a not_done "X"
        informations.grid(row=1, rowspan=3, pady=10, column=0, columnspan=2)

        # BWT title
        label_BWT = ttk.Label(
            self.frame_label_BWT, text='Burrows–Wheeler transform')
        label_BWT.config(font=("Calibri", 40))
        label_BWT.grid(row=0, columnspan=50, pady=10,
                       padx=300, sticky="wens")
        # Huffman title
        label_Huffman = ttk.Label(
            self.frame_label_huffman, text='Huffman Compression')
        label_Huffman.config(font=("Calibri", 40))
        label_Huffman.grid(row=0, column=1, pady=10,
                           padx=400, sticky="wens")
        # Box to to show the results of BWT, here it's a CustomText which is a
        # modification of the ordinary text. For the sake of highlighting
        # certain patterns
        self.result_BWT = CustomText(
            self.frame_results_BWT, height=10, width=100, borderwidth=0, font=('Times new roman', 15))
        self.result_BWT.configure(
            state='disabled',  relief="flat")
        self.result_BWT.grid(
            row=0, columnspan=2, sticky='ew')
        # Adding a scrollbar into the box of results
        scrollb = ttk.Scrollbar(
            self.frame_results_BWT, command=self.result_BWT.yview)
        scrollb.grid(row=0, column=2, sticky='ns')
        self.result_BWT['yscrollcommand'] = scrollb.set
        # Box to to show the results of Huffman, here it's a CustomText which is a
        # modification of the ordinary text. For the sake of highlighting
        # certain patterns
        self.result_huffman = CustomText(
            self.frame_results_huffman, height=10, width=100, borderwidth=0, font=('Times new roman', 15))
        self.result_huffman.configure(
            state='disabled',  relief="flat")
        self.result_huffman.grid(
            row=0, columnspan=2, sticky='ew')
        # Adding a scrollbar into the box of results
        scrollb = ttk.Scrollbar(
            self.frame_results_huffman, command=self.result_huffman.yview)
        scrollb.grid(row=0, column=2, sticky='ns')
        self.result_huffman['yscrollcommand'] = scrollb.set

    def create_progress_table(self):
        '''
        Method that creates the progress table and sets two pictures associated
        with two meanings
        '''
        # Creating a reference for both possibilities of the images
        # Reference for the not done image
        image_not_done = Image.open('not_done.png').resize((30, 30))
        self.photo_not_done = ImageTk.PhotoImage(image_not_done)
        # Reference for the done image
        image_done = Image.open('done.png').resize((30, 30))
        self.photo_done = ImageTk.PhotoImage(image_done)
        i = 0
        # Title of the tracker
        lab = Label(self.frame_progress,
                    text='Real-time sequence tracking', font=('Arial 24 underline'))
        lab['bg'] = self['bg']
        lab.grid(row=0, columnspan=4, padx=20)
        # Design of the presentation of the different states
        # By itterating through self.sequence
        for possibility in self.sequence:
            lab = Label(self.frame_progress, text=possibility)
            # Storage of the label in a dictionnary
            self.progress_labels[possibility] = lab
            # Will make the background of the entry seem "transparent"
            lab['bg'] = self['bg']
            lab.grid(row=1, column=i, padx=20)
            # Label that will containt the image
            label = Label(self.frame_progress,
                          image=self.photo_not_done, height=30, width=30)
            # Will make the background of the entry seem "transparent"
            label['bg'] = self['bg']
            # Reference for the label.image being a not_done "X"
            label.image = self.photo_not_done
            label.grid(row=2, column=i)
            # Storage of the corresponding Label containg the image inside a
            # dictionnary
            self.progress_images[possibility] = label
            # On each step, the program is moving one column to the right with
            # fixed row
            i += 1
        # Let's connect
        inquiries = Label(
            self.frame_git, text='For any inquiries:', font=('Arial 24 underline'))
        # Will make the background of the entry seem "transparent"
        inquiries['bg'] = self['bg']
        # Reference for the label.image being a not_done "X"
        inquiries.grid(row=1, rowspan=3, pady=10, column=0, columnspan=2)
       # Creating GitHub logo
        image_git = Image.open('github_logo.png').resize((150, 100))
        self.photo_git = ImageTk.PhotoImage(image_git)
        self.label_git = Label(self.frame_git,
                               image=self.photo_git, height=150, width=150, cursor="hand2")
        # Will make the background of the entry seem "transparent"
        self.label_git['bg'] = self['bg']
        # Reference for the label.image being a not_done "X"
        self.label_git.grid(row=4, rowspan=3, pady=10, column=0)
        self.label_git.bind(
            "<Button-1>", lambda e: self.callback("https://github.com/GeorgeAlehandro"))
        # Creating Email logo
        image_mail = Image.open('mail.png').resize((100, 100))
        self.photo_mail = ImageTk.PhotoImage(image_mail)
        self.label_mail = Label(self.frame_git,
                                image=self.photo_mail, height=150, width=150, cursor="hand2")
        # Will make the background of the entry seem "transparent"
        self.label_mail['bg'] = self['bg']
        # Reference for the label.image being a not_done "X"
        self.label_mail.grid(row=4, rowspan=3, pady=10, column=1)
        self.label_mail.bind(
            "<Button-1>", lambda e: self.callback("https://outlook.com"))

    def create_fields(self):
        '''
        Creates the different elements of the graphical interface.
        '''
        i, j = 0, 0
        l = 0
        # AT-Bit image insertion
        image_logo = Image.open('logo.png').resize((100, 100))
        self.photo_logo = ImageTk.PhotoImage(image_logo)
        label = Label(self.frame0,
                      image=self.photo_logo, height=100, width=100)
        # Setting the background color as 'White'
        label['bg'] = self['bg']
        label.grid(row=0, column=2, sticky='N')
        # For each Entry inside self.entries there will be an Entry created
        # In this case we only have one entry
        for idi in self.entries:
            j = 0
            self.entry_bar = StringVar()
            entry = tk.Entry(self.frame_entry_load_save,
                             textvariable=self.entry_bar, width=50, font=('Arial 24'))
            self.widgets_entry[idi] = entry
            entry.grid(row=1, column=0, columnspan=2, sticky='we')
            for button_name in self.data_buttons:
                buttown = ttk.Button(self.frame_entry_load_save, text=button_name, command=(
                    lambda button=button_name: self.button_press_handle(button)))
                self.widgets_button[button_name] = buttown
                buttown.grid(row=1, column=2+l, sticky='we')
                l += 1
            # For each button inside buttons_BWT
            for button_name in self.buttons_BWT:
                button_id = button_name + 'BWT'
                buttown = ttk.Button(self.frame_buttons_BWT, text=button_name, command=(
                    lambda button=button_id: self.button_press_handle(button)))
                # Stocking the name of the button inside the widgets dict
                self.widgets_button[button_id] = buttown
                buttown.grid(row=i+2, column=j)
                j += 1
            # Reset of the j gridding placement
            j = 0
            # For each button inside Huffman
            for button_name in self.buttons_huffman:
                button_id = button_name + 'Huffman'
                buttown = ttk.Button(self.frame_buttons_huffman, text=button_name, command=(
                    lambda button=button_id: self.button_press_handle(button)))
                # Stocking the name of the button inside the widgets dict
                self.widgets_button[button_id] = buttown
                buttown.grid(row=10, column=j)
                j += 1
        # Creation of the Show Tree Button
        button_id = 'Show Tree'
        buttown = ttk.Button(self.frame_results_huffman, text='Show Tree', command=(
            lambda button=button_id: self.button_press_handle(button)))
        self.widgets_button[button_id] = buttown
        self.widgets_button['Show Tree'].configure(state='disabled')
        buttown.grid(row=0, column=5, padx=50)
        self.disable_all_operations_buttons()

    def failed_save_warning(self):
        '''
        Used to prompt the user for a failed save attempt
        '''
        showerror(
            "Save Failed", """Failed save attempt because:\nThe object doesn't have the attribute you are trying to save.""")

    def create_tooltips(self):
        '''
        ToolTips for each button (displaying tips when hovering with the mouse)
        '''
        CreateToolTip(
            self.widgets_button["Load"], text='Click to load a sequence from local file.')
        CreateToolTip(self.widgets_button["Generate CodeBWT"],
                      text='Button to do the transformation of the original sequence in to the BWT sequence.')
        CreateToolTip(self.widgets_button["ReconstructBWT"],
                      text='Button to do the reconstruction of the original sequence based on the BWT sequence.')
        CreateToolTip(
            self.widgets_button["NextBWT"], text='Displays the next step of the ongoing BWT operation.')
        CreateToolTip(self.widgets_button["Final ResultBWT"],
                      text='Displays the final result of the ongoing BWT operation.')
        CreateToolTip(self.widgets_button["CompressHuffman"],
                      text='Button to do the compression of the sequence.')
        CreateToolTip(self.widgets_button["DecompressHuffman"],
                      text='Button to do the decompression of the sequence.')
        CreateToolTip(self.widgets_button["NextHuffman"],
                      text='Displays the next step of the ongoing Huffman operation.')
        CreateToolTip(self.widgets_button["Final ResultHuffman"],
                      text='Displays the final result of the ongoing Huffman operation.')
        CreateToolTip(self.widgets_button["Show Tree"],
                      text='Shows the Huffman tree that\n''is behind the encryption of the\n''different nucleotides in\n''the sequence.')

    def save_function(self, value):
        '''
        This is the method of saving that will take the input value of each
        button and transfer it to the controller which will behave accordingly
        '''
        self.controller.save(value)

    def save_choices(self):
        '''
        Function that creates the OptionMenu of the different choices of saving
        '''
        # List of the possible choices
        options = ['Save DNA Motif', 'Save BWT Coded',
                   'Save Compressed Sequence']
        self.default_save = StringVar()
        # This OptionMenu has its options and default value as default_save
        # The default value is only for displaying
        self.save_menu_choices = ttk.OptionMenu(self.frame_entry_load_save,
                                                self.default_save, self.default_save, *options, command=self.save_function)
        # Save Choices is the default value before choosing another option
        self.default_save.set('Save Choices')
        self.save_menu_choices.grid(row=1, column=3)

    def compression_choices(self):
        '''
        Prompt the user to choose which sequence he wants to compress in case
        of the presence of both choices (transformed or not)
        '''
        answer = askyesno(title='Choice of sequence',
                          message='''Do you want to compress the BWT sequence? \
                              Answer no to use the non-BWT sequence.''')
        # If the user's answer is Yes
        if answer:
            self.controller.compresion_Huffman('BWT')
        # If answer is No
        else:
            self.controller.compresion_Huffman('non_BWT')

    def enable_show_tree(self):
        '''
        Used to enable show_tree from controller
        '''
        self.widgets_button['Show Tree'].configure(state='normal')

    def disable_show_tree(self):
        '''
        Used to disable show_tree from controller
        '''
        self.widgets_button['Show Tree'].configure(state='disabled')

    def disable_next_BWT(self):
        '''
        Method uset disable the Next button on the BWT operations
        '''
        for idi in self.pedagogic_entries:
            self.widgets_button['NextBWT'].configure(state='disabled')

    def focusText(self, event):
        self.pedagogic_result.config(state='normal')
        self.pedagogic_result.focus()
        self.pedagogic_result.config(state='disabled')

    def result_display(self, result, tab):
        '''
        Message display after insertion
        '''
        if tab == 'result_BWT':
            self.result_BWT.configure(state='normal')
            self.result_BWT.delete('1.0', 'end')
            if isinstance(result, list):
                for element in result:
                    self.result_BWT.insert('end', element+'\n')
            else:
                self.result_BWT.insert('1.0', result)
            self.result_BWT.configure(state='disabled')
        elif tab == 'result_huffman':
            self.result_huffman.configure(state='normal')
        # self.result_huffman.delete('1.0', 'end')
            self.result_huffman.insert('end', result)
            self.result_huffman.insert('end', '\n')
            self.result_huffman.configure(state='disabled')

    def highlight_BWT(self):
        '''
        Method used to highlight based on the regex patter dictated by
        self.pattern
        '''
        # Creatomg a link between the regex and the sign to show inside the box
        # (Special methods for the CustomText class)
        self.result_BWT.tag_configure(
            "Found", foreground="yellow", background='grey', underline=True)
        self.result_BWT.highlight_pattern(
            self.pattern, 'Found', regexp=True)

    def update_entry(self, data):
        '''
        Used for updating the text inside Entry, in particular used for loading
        '''
        self.widgets_entry["Entry"].delete(0, "end")
        self.widgets_entry["Entry"].insert(0, data)

    def activate_on_load_BWT(self):
        '''
        Activates Next and Final Result buttons for BWT
        '''
        self.widgets_button['NextBWT'].configure(state='normal')
        self.widgets_button['Final ResultBWT'].configure(state='normal')

    def activate_on_load_huffman(self):
        '''
        Activates Next and Final Result buttons for Huffman
        '''
        self.widgets_button['NextHuffman'].configure(state='normal')
        self.widgets_button['Final ResultHuffman'].configure(state='normal')

    def desactivate_buttons_BWT(self):
        '''
        Desactivates Next and Final Result buttons for BWT
        '''
        self.widgets_button['NextBWT'].configure(state='disabled')
        self.widgets_button['Final ResultBWT'].configure(state='disabled')

    def desactivate_buttons_huffman(self):
        '''
        Desactivates Next and Final Result buttons for Huffman
        '''
        self.widgets_button['NextHuffman'].configure(state='disabled')
        self.widgets_button['Final ResultHuffman'].configure(state='disabled')

    def clear_pressed_BWT(self):
        '''
        Turns the BWT operation buttons into not pressed
        '''
        self.widgets_button['Generate CodeBWT'].state(['!pressed'])
        self.widgets_button['ReconstructBWT'].state(['!pressed'])

    def clear_pressed_huffman(self):
        '''
        Turns the Huffman operation buttons into not pressed
        '''
        self.widgets_button['CompressHuffman'].state(['!pressed'])
        self.widgets_button['DecompressHuffman'].state(['!pressed'])

    def clear_BWT(self):
        '''
        Used to clear the BWT result box
        '''
        self.result_BWT.configure(state='normal')
        self.result_BWT.delete('1.0', 'end')
        # Back to disabled state that can't be manually modified
        self.result_BWT.configure(state='disabled')

    def clear_huffman(self):
        '''
        Used to clear the Huffman result box
        '''
        self.result_huffman.configure(state='normal')
        self.result_huffman.delete('1.0', 'end')
        # Back to disabled state that can't be manually modified
        self.result_huffman.configure(state='disabled')

    def progress_check(self, image_check=None):
        '''
        Method used to keep track of the sequence, when image_check is passed
        the corresponding image will be "ticked" as done
        '''
        if image_check is None:
            # Takes the attribut self.resulting_sequence
            image_check = self.resulting_sequence
        # Change of the corresponding image into ticked
        self.progress_images[image_check].configure(
            image=self.photo_done)

    def reset_progress_check(self):
        '''
        Called to reset the track of the sequence
        '''
        # "Unticks" all the images
        for image in self.sequence:
            self.progress_images[image].configure(
                image=self.photo_not_done)
            CreateToolTip(self.progress_images[image],
                          text='')

    def file_save(self, action):
        '''
        This method is used to dictate the behavior of the program depending on
        the different possibilities of saving
        '''
        # To save a reconstructed (non_BWT) sequence or the compressed sequence
        # inside a .txt file
        if action == 'Save DNA Motif' or action == 'Save Compressed Sequence':
            f = asksaveasfilename(initialdir="./", title="Save destination",
                                  filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        # To save the BWT transformed sequence inside a .bzip2 file
        elif action == 'Save BWT Coded':
            f = asksaveasfilename(initialdir="./", title="Save destination",
                                  filetypes=(("Zip files", "*.bz2"), ("all files", "*.*")))
        # Returns the file directory
        return f

    def button_press_handle(self, buttonid):
        '''
        Assign a command for each pressed button.
        '''
        # buttonid is returned for each button pressed by the user
        # it's specific for each button and each runs a specific sequence of
        # Functions
        if buttonid == "Generate CodeBWT":
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.result_BWT.delete('1.0', 'end')
            self.controller.string_code_BWT()
            self.widgets_button['Generate CodeBWT'].state(['pressed'])
            self.activate_on_load_BWT()
            self.pattern = '.$'
            # Used for the progress check
            self.resulting_sequence = 'BWT Coded'
        if buttonid == "CompressHuffman":
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.clear_huffman()
            self.widgets_button['CompressHuffman'].state(['pressed'])
            self.controller.compresion_Huffman()
          #  self.compression_choices()
            self.activate_on_load_huffman()
            self.resulting_sequence = 'Compressed'
        elif buttonid == "ReconstructBWT":
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.result_BWT.delete('1.0', 'end')
            self.controller.reconstruct_BWT()
            self.widgets_button['ReconstructBWT'].state(['pressed'])
            self.activate_on_load_BWT()
            self.pattern = '.*\$$'
            self.resulting_sequence = 'DNA Motif'
        elif buttonid == "Final ResultBWT":
            self.controller.final_result_BWT()
            self.desactivate_buttons_BWT()
        elif buttonid == "DecompressHuffman":
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.clear_huffman()
            self.widgets_button['DecompressHuffman'].state(['pressed'])
            self.controller.decompresion_Huffman()
            self.activate_on_load_huffman()
            self.resulting_sequence = 'Decompressed'
        elif buttonid == "Final ResultHuffman":
            self.controller.final_result_huffman()
            self.desactivate_buttons_huffman()
        elif buttonid == "Load":
            self.controller.load()
        elif buttonid == "NextBWT":
            self.controller.next_button_bwt()
        elif buttonid == "NextHuffman":
            self.controller.next_button_huffman()
        elif buttonid == "Show Tree":
            self.controller.tree_presentation()
        elif buttonid == "Clear":
            for value in self.widgets_entry.values():
                value.delete(0, 'end')
# TODO:
    # Presentation of the tree in a tkinter canvas

    def draw(self, node, data):   # Draw a node as root
        saw = defaultdict(int)

        def create_graph(G, node, p_name="initvalue", pos={}, x=0, y=0, layer=1):
            if not node:
                return
            name = str(node.symbol)
            saw[name] += 1
            if name in saw.keys():
                name += ' ' * saw[name]
            if p_name != "initvalue":
                G.add_edge(p_name, name)
            pos[name] = (x, y)

            l_x, l_y = x - 1 / (3 * layer), y - 1
            l_layer = layer + 1
            create_graph(G, node.left, name, x=l_x,
                         y=l_y, pos=pos, layer=l_layer)

            r_x, r_y = x + 1 / (3 * layer), y - 1
            r_layer = layer + 1
            create_graph(G, node.right, name, x=r_x,
                         y=r_y, pos=pos, layer=r_layer)
            return (G, pos)

        graph = nx.DiGraph()
        graph.name
        graph, pos = create_graph(graph, node)
        # pos["     "] = (0, 0)
        # Scale can be adjusted appropriately according to the depth of the tree
        self.fig = plt.Figure(figsize=(1, 1), dpi=100)
        color_map = []
        # for j,node in enumerate(graph.nodes):
        # for degree in graph.out_degree:
        #     if int(degree[0]) in data and degree[1] == 0:
        #         color_map.append('blue')
        #     else:
        #         color_map.append('green')
        # nx.draw(G, node_color=color_map, with_labels=True)
        nx.draw_networkx(graph, pos,  node_size=1000,
                         node_color=color_map)
        plt.show()

    def open_file(self):
        '''
        Used to prompt user for filename and directory, returns file into the
        controller
        '''
        file = askopenfilename()
        if file.endswith('.txt'):
            showinfo(
                title='File loaded', message='.txt file loaded')
        if file.endswith('.bz2'):
            showinfo(
                title='File loaded', message='.bz2 file loaded')
        return file

    def disable_all_operations_buttons(self):
        '''
        Disables all the buttons, used when changing the sequence
        '''
        self.widgets_button['Generate CodeBWT'].configure(state='disabled')
        self.widgets_button['ReconstructBWT'].configure(state='disabled')
        self.widgets_button['CompressHuffman'].configure(state='disabled')
        self.widgets_button['DecompressHuffman'].configure(state='disabled')
        self.widgets_button['NextBWT'].configure(state='disabled')
        self.widgets_button['Final ResultBWT'].configure(state='disabled')
        self.widgets_button['NextHuffman'].configure(state='disabled')
        self.widgets_button['Final ResultHuffman'].configure(state='disabled')

    def callback(self, url):
        webbrowser.open_new(url)

    def verify_entry_activate_buttons(self):
        '''
        Verification of all entry inside the box, activates the right  buttons
        accordingly
        '''
        # First all the buttons are desactivated
        self.disable_all_operations_buttons()
        # Then fetches the entry
        entry_fetch = self.widgets_entry["Entry"].get()
        # If the entry is empty or only spaces, reset all the pics to not_done
        if (len(entry_fetch.replace(" ", "")) == 0):
            self.reset_progress_check()
        # If only A, T, C, G,N inside the entry, it wil activate two possible
        # operations, either Compressing by Huffman or Generating the BWT seq
        if all(letter in ['A', 'T', 'C', 'G', 'N'] for letter in entry_fetch.upper()) and len(entry_fetch) > 0:
            self.widgets_button['CompressHuffman'].configure(state='normal')
            self.widgets_button['Generate CodeBWT'].configure(state='normal')
            self.progress_check('DNA Motif')
            self.progress_check('Decompressed')
            CreateToolTip(self.progress_images['DNA Motif'],
                          text=entry_fetch)
            CreateToolTip(self.progress_images['Decompressed'],
                          text=entry_fetch)

        # If '□' is found inside the Entry, it means the sequence is a compressed
        # sequence, then the Huffman decompression will be possible
        if '□' in entry_fetch:
            self.widgets_button['DecompressHuffman'].configure(state='normal')
            self.progress_check('Compressed')
            CreateToolTip(self.progress_images['Compressed'],
                          text=entry_fetch)
        # If A, T, C, G, N and only one $ is found inside the sequence, then
        # the BWT reconstruction method is possible
        if all(letter in ['A', 'T', 'C', 'G', 'N', '$'] for letter in entry_fetch.upper()) and entry_fetch.count("$") == 1 and len(entry_fetch) > 0:
            self.widgets_button['ReconstructBWT'].configure(state='normal')
            self.widgets_button['CompressHuffman'].configure(state='normal')
            self.progress_check('BWT Coded')
            self.progress_check('Decompressed')
            CreateToolTip(self.progress_images['BWT Coded'],
                          text=entry_fetch)
            CreateToolTip(self.progress_images['Decompressed'],
                          text=entry_fetch)

    def main(self):
        '''
        Main execution of the Tkinter view.
        '''
        # Title of the main window
        self.title("AT-BIT M1 Project")
        # Using a particular theme for display
        self.s = ttk.Style()
        self.s.theme_use('clam')
        # White background
        self.configure(bg='white')
        # Creating all the different frames by calling the corresponding methods
        self.create_menu()
        self.create_frames()
        self.create_progress_table()
        self.create_labels()
        self.create_fields()
        self.save_choices()
        self.create_tooltips()
        # This function traces the Entry widget if it detects a change then
        # some methods will be called, in particular to reset

        def trace_when_Entry_widget_is_updated(var, index, mode):
            # If the user changes the Entry while in the middle of an operation,
            # He will be prompted by the interface to Confirm his modifications
            if (self.controller.operation_BWT is not None or self.controller.operation_Huffman is not None):
                answer = askokcancel(
                    title='Confirmation',
                    message='Changing the Entry or Loading will reset all the progress.')
                if not answer:
                    # The user modification will not be accepted, the old entry
                    # Is kept back
                    self.update_entry(self.original_value)
                    # The trace ends here, no reset was done
                    return
            self.controller.reset_operations()
            self.reset_progress_check()
            self.controller.reset()
            self.clear_pressed_BWT()
            self.clear_BWT()
            self.desactivate_buttons_BWT()
            self.clear_pressed_huffman()
            self.clear_huffman()
            self.disable_show_tree()
            self.desactivate_buttons_huffman()
            self.verify_entry_activate_buttons()
            self.controller.attributes_check()
            self.default_save.set('Save Choices')
        # Links the trace function and the entry widget
        self.entry_bar.trace_variable("w", trace_when_Entry_widget_is_updated)
        self.attributes('-zoomed', True)
      #  self.wm_attributes('-transparentcolor', self['bg'])
        self.mainloop()
