# coding: utf-8
"""
Tkinter View of the project.

"""

from __future__ import absolute_import
import tkinter as tk
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar
from tkinter import Entry
from view import SuperView
from tkinter.filedialog import askopenfile
from tkinter import ttk


class View(Tk, SuperView):
    '''
    Class for the Tkinter view (inherits from SuperView)
    '''

    def __init__(self, controller):
        '''
        Constructor for the Tkinter view.
        '''
        super().__init__()
        SuperView.__init__(self, controller)
        self.widgets_labs = {}
        self.widgets_entry = {}
        self.widgets_button = {}
        self.widgets_tab = {}
        self.buttons = ["Generate Code", "Reconstruct", "Save", "Load"]
        #self.extrabuttons = ["Content", "Clear"]

    def fetch_autocomplete_values(self):
        '''
        Returns a list containing the elements to be used in the autocompletion
        entry. Elements are inside the memory.
        '''
        (self.list_surname, self.list_name,
         self.list_telephone, self.list_address,
         self.list_city) = self.controller.memory_generator()
        self.autocomplete_values = [self.list_surname, self.list_name,
                                    self.list_telephone,
                                    self.list_address, self.list_city]

    def get_value_BWT(self):
        '''
        Returns the values introduced by the user.
        '''
        entry_fetch = (self.widgets_entry["BWT"].get())
        if all(item == '' for item in entry_fetch):
            messagebox.showerror('Entry unavailable',
                                 self.error_messages[3])
            return False
        return entry_fetch

    def get_value_BWT_pedagogic(self):
        '''
        Returns the values introduced by the user.
        '''
        entry_fetch = (self.widgets_entry["BWT Pedagogic"].get())
        if all(item == '' for item in entry_fetch):
            messagebox.showerror('Entry unavailable',
                                 self.error_messages[3])
            return False
        return entry_fetch

    def get_value_Huffman(self):
        entry_fetch = (self.widgets_entry["HUFFMAN"].get())
        if all(item == '' for item in entry_fetch):
            messagebox.showerror('Entry unavailable',
                                 self.error_messages[3])
            return False
        return entry_fetch

    def create_fields(self):
        '''
        Creates the different elements of the graphical interface.
        '''
        i, j, k = 0, 0, 0

        for idi in self.entries:
            j = 0
            # lab = Label(self, text=idi.capitalize())
            # self.widgets_labs[idi] = lab
            # lab.grid(row=i, column=0)
            tab = Frame(self.my_notebook, width=700, height=700, bg='white')
            self.widgets_tab[idi] = tab
            tab.grid()
            self.my_notebook.add(tab, text=idi)
            var = StringVar()
            entry = Entry(self.widgets_tab[idi], text=var)
            self.widgets_entry[idi] = entry
            entry.grid(row=0, columnspan=4)
            for button_name in self.buttons:
                buttown = Button(self.widgets_tab[idi], text=button_name, command=(
                    lambda button=button_name+idi: self.button_press_handle(button)))
                print(button_name+idi)
                self.widgets_button[button_name+idi] = buttown
                buttown.grid(row=i+1, column=j)
                j += 1
        for idi in self.pedagogic_entries:
            j = 0
            # lab = Label(self, text=idi.capitalize())
            # self.widgets_labs[idi] = lab
            # lab.grid(row=i, column=0)
            tab = Frame(self.my_notebook, width=700, height=700, bg='white')
            self.widgets_tab[idi] = tab
            tab.grid()
            self.my_notebook.add(tab, text=idi)
            var = StringVar()
            entry = Entry(self.widgets_tab[idi], text=var)
            self.widgets_entry[idi] = entry
            entry.grid(row=0, columnspan=4)
            for button_name in self.buttons:
                buttown = Button(self.widgets_tab[idi], text=button_name, command=(
                    lambda button=button_name+idi: self.button_press_handle(button)))
                print(button_name+idi)
                self.widgets_button[button_name+idi] = buttown
                buttown.grid(row=i+1, column=j)
                j += 1
            buttown = Button(self.widgets_tab[idi], text='Next', command=(
                lambda button='Next'+idi: self.button_press_handle(button)), state='disabled')
            self.widgets_button['Next'+idi] = buttown
            buttown.grid(row=i+1, column=j)
            j += 1
        print(self.widgets_tab)
        print(self.widgets_entry)
        print(self.widgets_button)
        self.my_notebook.grid()
        # for frame in self.widgets_tab.keys():
        #     j = 0
        #     print(frame)
        #     for idi in self.buttons:
        #         print(idi)
        #         buttown = Button(self.widgets_tab[frame], text=idi, command=(
        #             lambda button=idi: self.button_press_handle(button)))
        #         self.widgets_button[idi] = buttown
        #         buttown.grid(row=i+1, column=j)

        #         j += 1
    def disable_next(self):
        for idi in self.pedagogic_entries:
            self.widgets_button['Next'+idi].configure(state='disabled')

    def focusText(self, event):
        self.pedagogic_result.config(state='normal')
        self.pedagogic_result.focus()
        self.pedagogic_result.config(state='disabled')

    def result_display(self, result):
        '''
        Message display after insertion
        '''
        this_tab = self.widgets_tab['BWT Pedagogic']
        self.below_entry = Frame(this_tab)
        self.below_entry.grid(row=2, columnspan=4)
        # lezemla tezbit
        # TODO
        try:
            self.final_result.configure(state='normal')
            self.final_result.delete('1.0', 'end')
            self.final_result.insert('1.0', result)
            self.final_result.configure(state='disabled')
        except:
            self.final_result = CustomText(
                self.below_entry, height=2, width=50, borderwidth=0)
            self.final_result.insert('1.0', result)
            self.final_result.configure(
                state='disabled', bg=this_tab.cget('bg'), relief="flat")
            self.final_result.grid(row=2, columnspan=4, sticky='ns')
            self.final_result.bind('<Button-1>', self.focusText)

    def pedagogic_display(self, result, widgets_tab):
        #'BWT Pedagogic'
        this_tab = self.widgets_tab[widgets_tab]
        self.below_entry = Frame(this_tab)
        self.below_entry.grid(row=2, columnspan=5)
        try:
            self.pedagogic_result.configure(state='normal')
            self.pedagogic_result.delete('1.0', 'end')
            for element in result:
                self.pedagogic_result.insert('end', element+'\n')
            self.pedagogic_result.configure(state='disabled')
        except:
            self.pedagogic_result = CustomText(
                self.below_entry, height=40, width=50, borderwidth=0, font=('Times new roman', 15))
            for element in result:
                self.pedagogic_result.insert('end', element+'\n')
            #     self.pedagogic_result.tag_add('last', float(len(element)-1), 'end')
            # self.pedagogic_result.tag_configure('last', background='yellow',
            #                                     font='helvetica 14 bold', relief='raised')
            self.pedagogic_result.configure(
                state='disabled', bg=this_tab.cget('bg'), relief="flat")
            self.pedagogic_result.grid(row=3, columnspan=2)
            self.pedagogic_result.bind('<Button-1>', self.focusText)
        # buttown = Button(self.below_entry, text='Next',
        #                  command=self.pedagogic_display(result[0]))
        # buttown.grid(row=4)
        # TODO: Next button not balbling
# self.pedagogic_result.highlight_pattern(
#             '.*\$$', 'Found', regexp=True)

    def on_closing(self):
        '''
        Function that sets the behavior when closing the graphical interface.
        '''
        message_closing = "Do you want to quit? Modifications will be saved."
        if messagebox.askokcancel("Quit", message_closing):
            self.controller.save_notebook()
            self.destroy()

    def result_presentation(self, items_list):
        '''
        Results presentation after fetching.
        '''
        if items_list is not None:
            treepresentation = Toplevel(self)
            treepresentation.title("Address Book")
            columns = ("Surname", "Name", "Telephone", "Address", "City")
            tree = Treeview(treepresentation, columns=columns, show='headings')
            tree.heading("Surname", text="Surname")
            tree.heading("Name", text="Name")
            tree.heading("Telephone", text="Telephone")
            tree.heading("Address", text="Address")
            tree.heading("City", text="City")

            for person in items_list:
                tree.insert("", "end", values=(
                    person['surname'], person['name'], person['telephone'],
                    person['address'], person['city']))

            tree.grid(row=0, column=0, sticky='nsew')
            vsb = Scrollbar(treepresentation,
                            orient="vertical", command=tree.yview)
            vsb.grid(row=0, column=1, sticky='nsw')

            tree.configure(yscrollcommand=vsb.set)

            def item_delete(event):
                for selected_item in tree.selection():
                    item = tree.item(selected_item)
                    record = item['values']
                    message_verif = 'Are you sure you want to\
                        delete the selected element?'
                    answer = messagebox.askyesno(title='Information',
                                                 message=message_verif,
                                                 parent=treepresentation)
                    if answer:
                        self.controller.delete(record)
            tree.bind('<<TreeviewSelect>>', item_delete)
            quit_button = Button(treepresentation,  text="Quit",
                                 command=lambda: treepresentation.destroy())
            quit_button.grid(row=1, column=0, sticky='s')
        else:
            messagebox.showerror('Results', 'Results were not found')

    def highlight_BWT(self):
        print('MAFROUD HIGHLIGHT')
        self.pedagogic_result.tag_configure(
            "Found", foreground="yellow", background='grey', underline=True)
        self.pedagogic_result.highlight_pattern(
            self.pattern, 'Found', regexp=True)

# '.*\$$', 'Found', regexp=True)

    def button_press_handle(self, buttonid):
        '''
        Assign a command for each pressed button.
        '''
        if buttonid == "Generate CodeBWT":
            print(buttonid)
            self.controller.string_code_BWT()
        if buttonid == "Generate CodeBWT Pedagogic":
            print(buttonid)
            self.controller.string_code_BWT_pedagogic()
            self.pattern = '.$'
            self.widgets_button['NextBWT Pedagogic'].configure(state='normal')
        if buttonid == "Generate CodeHUFFMAN":
            print(buttonid)
            self.controller.string_code_Huffman()
        elif buttonid == "ReconstructBWT":
            print(buttonid)
            self.controller.reconstruct_BWT()
        elif buttonid == "ReconstructBWT Pedagogic":
            print(buttonid)
            self.controller.reconstruct_BWT_pedagogic()
            self.pattern = '.*\$$'
            self.widgets_button['NextBWT Pedagogic'].configure(state='normal')
        elif buttonid == "ReconstructHUFFMAN":
            print(buttonid)
            self.controller.reconstruct_Huffman()
        elif buttonid == "SaveBWT":
            print(buttonid)
            self.controller.save()
        elif buttonid == "SaveHUFFMAN":
            print(buttonid)
            self.controller.save()
        elif buttonid == "LoadBWT":
            print(buttonid)
            self.controller.load()
        elif buttonid == "LoadHUFFMAN":
            print(buttonid)
            self.controller.load()
        elif buttonid == "NextBWT Pedagogic":
            print(buttonid)
            self.controller.next_button('BWT Pedagogic')
        elif buttonid == "Clear":
            for value in self.widgets_entry.values():
                value.delete(0, 'end')

    def open_file(self):
        file = askopenfile(mode='r')
        return file

    def main(self):
        '''
        Main execution of the Tkinter view.
        '''
        self.title("Algo")
        self.geometry("700x700")
        self.my_notebook = ttk.Notebook(self)
        # my_notebook.pack()
        # my_frame1 = Frame(my_notebook, width=500, height=500, bg='blue')
        # my_frame2 = Frame(my_notebook, width=500, height=500, bg='red')
        # my_frame1.pack(fill="both", expand=1)
        # my_frame2.pack(fill="both", expand=1)

        # my_notebook.add(my_frame1, text="Blue Tab")
        # my_notebook.add(my_frame2, text="Red Tab")
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)
      #  self.fetch_autocomplete_values()
        self.create_fields()
        self.mainloop()


class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit",
                                count=count, regexp=regexp)
            if index == "":
                break
            if count.get() == 0:
                break  # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
