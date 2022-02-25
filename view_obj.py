# coding: utf-8
"""
Tkinter View of the project.

"""

from __future__ import absolute_import
from tkinter import Button
from tkinter import Label
from tkinter import Tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import StringVar
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar
from tkinter import Entry
from view import SuperView


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
        self.buttons = ["Generate Code", "Reconstruct"]
        self.extrabuttons = ["Content", "Clear"]
        self.autocomplete_values = []
        self.list_surname = []
        self.list_name = []
        self.list_telephone = []
        self.list_address = []
        self.list_city = []

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

    def get_value(self):
        '''
        Returns the values introduced by the user.
        '''
        entry_fetch = (self.widgets_entry["BWT"].get())
        if all(item == '' for item in entry_fetch):
            messagebox.showerror('Entry unavailable',
                                 self.error_messages[3])
            return False
        return entry_fetch

    def update_values(self):
        '''
        To update autocomplete values after user entry.
        '''
        self.widgets_entry["Surname"].config(
            completevalues=self.list_surname)
        self.widgets_entry["Name"].config(
            completevalues=self.list_name)
        self.widgets_entry["Telephone"].config(
            completevalues=self.list_telephone)
        self.widgets_entry["Address"].config(
            completevalues=self.list_address)
        self.widgets_entry["City"].config(
            completevalues=self.list_city)

    def create_fields(self):
        '''
        Creates the different elements of the graphical interface.
        '''
        i, j, k = 0, 0, 0

        for idi in self.entries:
            lab = Label(self, text=idi.capitalize())
            self.widgets_labs[idi] = lab
            lab.grid(row=i, column=0)

            var = StringVar()
            entry = Entry(self, text=var)
            self.widgets_entry[idi] = entry
            entry.grid(row=i, column=1)

            i += 1

        for idi in self.buttons:
            buttown = Button(self, text=idi, command=(
                lambda button=idi: self.button_press_handle(button)))
            self.widgets_button[idi] = buttown
            buttown.grid(row=i+1, column=j)
            # self.widgets_button[idi].config(command = idi)

            j += 1
        for idi in self.extrabuttons:
            buttown = Button(self, text=idi, command=(
                lambda button=idi: self.button_press_handle(button)))
            self.widgets_button[idi] = buttown
            buttown.grid(row=k, column=2, rowspan=2)
            # self.widgets_button[idi].config(command = idi)

            k += 2

    def delete_display(self, title, result):
        '''
        Message display after delete.
        '''
        if result is not None:
            messagebox.showinfo(title, result)
        else:
            messagebox.showerror(title, self.error_messages[1])

    def insertion_display(self, title, result):
        '''
        Message display after insertion
        '''
        if result is not None:
            messagebox.showinfo(title, result)
            self.fetch_autocomplete_values()
        else:
            messagebox.showerror(
                title, self.error_messages[0])
        for value in self.widgets_entry.values():
            value.delete(0, 'end')

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

    def button_press_handle(self, buttonid):
        '''
        Assign a command for each pressed button.
        '''
        if buttonid == "Generate Code":
            self.controller.string_code()
        elif buttonid == "Reconstruct":
            self.controller.delete()
        # elif buttonid == "Insert":
        #     self.controller.insert()
        # elif buttonid == "Content":
        #     self.controller.display()
        elif buttonid == "Clear":
            for value in self.widgets_entry.values():
                value.delete(0, 'end')

    def main(self):
        '''
        Main execution of the Tkinter view.
        '''
        self.title("Phone Notebook")
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)
      #  self.fetch_autocomplete_values()
        self.create_fields()
        self.mainloop()
