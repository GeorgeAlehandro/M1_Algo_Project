# coding: utf-8
"""
Tkinter View of the project.

"""

from __future__ import absolute_import
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter.ttk import Scrollbar
from view import SuperView
from tkinter.filedialog import askopenfile, askdirectory, asksaveasfilename, askopenfilename
from tkinter import ttk
from customtext import CustomText
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import copy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')


class View(Tk, SuperView):
    '''
    Class for the Tkinter view (inherits from SuperView)1
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
        self.progress_labels = {}
        self.progress_images = {}
        self.sequence = ['Motif', 'Coded', 'Decompressed', 'Compressed']
        self.data_buttons = ["Save", "Load", ]
        self.buttons = ["Generate Code", "Reconstruct", "Next", "Final Result"]
        # self.extrabuttons = ["Content", "Clear"]
        self.buttons_huffman = ["Compress",
                                "Decompress", "Next", "Final Result"]

    def get_value(self, request=None):
        '''
        Returns the values introduced by the user.
        '''
        entry_fetch = (self.widgets_entry["Entry"].get())
        if all(item == '' for item in entry_fetch):
            messagebox.showerror('Entry unavailable',
                                 self.error_messages[3])
            return False
        if request == 'reconstruction':
            if all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in entry_fetch.upper()) and entry_fetch.count("$") == 1:
                return entry_fetch
            else:
                messagebox.showerror('Entry unavailable',
                                     self.error_messages[4])
                return False
        if request == 'decompression':
            if '□' in entry_fetch:
                return entry_fetch
            else:
                messagebox.showerror('Entry unavailable',
                                     self.error_messages[1])
                return False
        if request == 'transformation':
            if all(letter in ['A', 'T', 'C', 'G', 'N', '\n'] for letter in entry_fetch.upper()):
                return entry_fetch
            else:
                messagebox.showerror('Entry unavailable',
                                     self.error_messages[5])
        if request is None:
            if not all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in entry_fetch.upper()):
                messagebox.showerror('Entry unavailable',
                                     self.error_messages[2])
                return False
            return entry_fetch

    # def get_value_decompression(self):
    #     entry_fetch = self.widgets_entry["Entry"].get()
    #     if '□' in entry_fetch:
    #         return entry_fetch
    #     else:
    #         messagebox.showerror('Entry unavailable',
    #                              self.error_messages[1])
    #         return False

    def create_frames(self):
        self.frame0 = Frame(self, bg="green", height=10, width=400, bd=10,
                            cursor="target")
        self.frame0.grid(row=0, column=5)
        self.frame_entry_load_save = Frame(
            self, bg="White", height=20, width=400, bd=10)
        self.frame_entry_load_save.grid(row=1, column=0)
        self.frame_progress = Frame(
            self, bg="White", height=20, width=400, bd=10)
        self.frame_progress.grid(row=1, column=1)
        self.frame_label_BWT = Frame(
            self, height=10, width=450)
        self.frame_label_BWT.grid(row=2, column=0, sticky='W')
        self.frame_buttons_BWT = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_buttons_BWT.grid(row=3, column=0)
        self.frame_results_BWT = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_results_BWT.grid(row=4, column=0, sticky='W')
        self.frame_label_huffman = Frame(
            self, height=10, width=400)
        self.frame_label_huffman.grid(row=5, column=0, sticky='WE')
        self.frame_buttons_huffman = Frame(
            self, bg="White", height=10, width=400, bd=10)
        self.frame_buttons_huffman.grid(row=6, column=0)
        self.frame_results_huffman = Frame(self, bg="White", height=10, width=400, bd=10,
                                           cursor="target")
        self.frame_results_huffman.grid(row=7, column=0, sticky='W')

    def create_labels(self):
        label_top = ttk.Label(
            self.frame_entry_load_save, text='Please type in your sequence, or load one.')
        label_top.grid(row=0, column=0)
        label_BWT = ttk.Label(
            self.frame_label_BWT, text='Burrows–Wheeler transform.')
        label_BWT.config(font=("Calibri", 40))
        label_BWT.grid(row=0, columnspan=50, sticky='E')
        label_Huffman = ttk.Label(
            self.frame_label_huffman, text='Huffman Compression.')
        label_Huffman.config(font=("Calibri", 40))
        label_Huffman.grid(row=0, columnspan=50, sticky='E')
        self.result_BWT = CustomText(
            self.frame_results_BWT, height=10, width=100, borderwidth=0, font=('Times new roman', 15))
        self.result_BWT.configure(
            state='disabled',  relief="flat")
        self.result_BWT.grid(
            row=0, columnspan=2, sticky='ew')
        scrollb = ttk.Scrollbar(
            self.frame_results_BWT, command=self.result_BWT.yview)
        scrollb.grid(row=0, column=2, sticky='ns')
        self.result_BWT['yscrollcommand'] = scrollb.set
        self.result_huffman = CustomText(
            self.frame_results_huffman, height=10, width=100, borderwidth=0, font=('Times new roman', 15))
        self.result_huffman.configure(
            state='disabled',  relief="flat")
        self.result_huffman.grid(
            row=0, columnspan=2, sticky='ew')
        scrollb = ttk.Scrollbar(
            self.result_huffman, command=self.result_huffman.yview)
        scrollb.grid(row=0, column=2, sticky='ns')
        self.result_huffman['yscrollcommand'] = scrollb.set

    def create_progress_table(self):
        # Creating a reference for both possibilities of the images (Done or not)
        image_not_done = Image.open('not_done.png').resize((30, 30))
        self.photo_not_done = ImageTk.PhotoImage(image_not_done)
        image_done = Image.open('done.png').resize((30, 30))
        self.photo_done = ImageTk.PhotoImage(image_done)
        i = 0
        for possibility in self.sequence:
            lab = Label(self.frame_progress, text=possibility.title())
            self.progress_labels[possibility] = lab
            lab.grid(row=0, column=i, padx=20)
            label = Label(self.frame_progress,
                          image=self.photo_not_done, height=30, width=30)
            label.image = self.photo_not_done
            label.grid(row=1, column=i)
            self.progress_images[possibility] = label
            i += 1

    def create_fields(self):
        '''
        Creates the different elements of the graphical interface.
        '''
        i, j, k = 0, 0, 0
        l = 0
        print('here self entries', self.entries)
        label = Label(self.frame0, text='Welcome')
        label.grid(row=0, column=2, sticky='N')
        for idi in self.entries:
            j = 0
            # lab = Label(self, text=idi.capitalize())
            # self.widgets_labs[idi] = lab
            # lab.grid(row=i, column=0)

            self.var = StringVar()
            entry = tk.Entry(self.frame_entry_load_save,
                             textvariable=self.var)
            self.widgets_entry[idi] = entry
            entry.grid(row=1, column=0, columnspan=2, sticky='we')
            for button_name in self.data_buttons:
                buttown = ttk.Button(self.frame_entry_load_save, text=button_name, command=(
                    lambda button=button_name: self.button_press_handle(button)))
                print(button_name+idi)
                self.widgets_button[button_name] = buttown
                buttown.grid(row=1, column=2+l, sticky='we')
                l += 1
            for button_name in self.buttons:
                button_id = button_name + 'BWT'
                buttown = ttk.Button(self.frame_buttons_BWT, text=button_name, command=(
                    lambda button=button_id: self.button_press_handle(button)))
                self.widgets_button[button_id] = buttown
                buttown.grid(row=i+2, column=j)
                if button_name in ['Final Result', 'Next']:
                    buttown.configure(state='disabled')
                j += 1
            j = 0
            for button_name in self.buttons_huffman:
                button_id = button_name + 'Huffman'
                buttown = ttk.Button(self.frame_buttons_huffman, text=button_name, command=(
                    lambda button=button_id: self.button_press_handle(button)))
                self.widgets_button[button_id] = buttown
                buttown.grid(row=10, column=j)
                if button_name in ['Final Result', 'Next']:
                    buttown.configure(state='disabled')
                j += 1
        button_id = 'Show Tree'
        buttown = ttk.Button(self.frame_results_huffman, text='Show Tree', command=(
            lambda button=button_id: self.button_press_handle(button)))
        self.widgets_button[button_id] = buttown
        self.widgets_button['Show Tree'].configure(state='disabled')
        buttown.grid(row=0, column=5)
        print(self.widgets_tab)
        print(self.widgets_entry)
        print(self.widgets_button)

    def save_choices(self):
        print('save_choices here')
        frame_entry_load_save = Toplevel(self.my_notebook)
       # frame_entry_load_save.pack(expand=True, fill=BOTH)
        button1 = Button(frame_entry_load_save, text='Compressed Form',
                         command=lambda: self.controller.save('save_transformation'))
        button2 = Button(frame_entry_load_save, text='Decompressed Form',
                         command=lambda: self.controller.save('save_reconstruction'))
        # command=self.controller.save('save_reconstruction')
        button1.pack(side=RIGHT)
        button2.pack(side=LEFT)

    def compression_choices(self):
        print('compression_choices here')
        frame_entry_load_save = Toplevel(self)
       # frame_entry_load_save.pack(expand=True, fill=BOTH)
        button1 = Button(frame_entry_load_save, text='Compress non-BWT sequence',
                         command=lambda: self.controller.compresion_Huffman('non_BWT'))
        button2 = Button(frame_entry_load_save, text='Compress BWT sequence',
                         command=lambda: self.controller.compresion_Huffman('BWT'))
        # command=self.controller.save('save_reconstruction')
        button1.pack(side=RIGHT)
        button2.pack(side=LEFT)

    def enable_show_tree(self):
        self.widgets_button['Show Tree'].configure(state='normal')

    def disable_show_tree(self):
        self.widgets_button['Show Tree'].configure(state='disabled')

    def disable_next_BWT(self):
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

    def on_closing(self):
        '''
        Function that sets the behavior when closing the graphical interface.
        '''
        message_closing = "Do you want to quit? Modifications will be saved."
        if messagebox.askokcancel("Quit", message_closing):
            self.controller.save_notebook()
            self.destroy()

    def highlight_BWT(self):
        print('MAFROUD HIGHLIGHT')
        self.result_BWT.tag_configure(
            "Found", foreground="yellow", background='grey', underline=True)
        self.result_BWT.highlight_pattern(
            self.pattern, 'Found', regexp=True)

    def update_entry(self, data):
        self.widgets_entry["Entry"].delete(0, "end")
        self.widgets_entry["Entry"].insert(0, data)
# '.*\$$', 'Found', regexp=True)

    def activate_on_load_BWT(self):
        self.widgets_button['NextBWT'].configure(state='normal')
        self.widgets_button['Final ResultBWT'].configure(state='normal')

    def activate_on_load_huffman(self):
        self.widgets_button['NextHuffman'].configure(state='normal')
        self.widgets_button['Final ResultHuffman'].configure(state='normal')

    def desactivate_buttons_BWT(self):
        self.widgets_button['NextBWT'].configure(state='disabled')
        self.widgets_button['Final ResultBWT'].configure(state='disabled')

    def desactivate_buttons_huffman(self):
        self.widgets_button['NextHuffman'].configure(state='disabled')
        self.widgets_button['Final ResultHuffman'].configure(state='disabled')

    def clear_pressed_BWT(self):
        self.widgets_button['Generate CodeBWT'].state(['!pressed'])
        self.widgets_button['ReconstructBWT'].state(['!pressed'])

    def clear_pressed_huffman(self):
        self.widgets_button['CompressHuffman'].state(['!pressed'])
        self.widgets_button['DecompressHuffman'].state(['!pressed'])

    def clear_BWT(self):
        self.result_BWT.configure(state='normal')
        self.result_BWT.delete('1.0', 'end')
        self.result_BWT.configure(state='disabled')

    def clear_huffman(self):
        self.result_huffman.configure(state='normal')
        self.result_huffman.delete('1.0', 'end')
        self.result_huffman.configure(state='disabled')

    def progress_check(self, image_check=None):
        if image_check is None:
            image_check = self.resulting_sequence
        self.progress_images[image_check].configure(
            image=self.photo_done)

    def reset_progress_check(self):
        for image in self.sequence:
            self.progress_images[image].configure(
                image=self.photo_not_done)
        print('MUST CHANGE')

    def file_save(self):
        f = asksaveasfilename(initialdir="./", title="Select file",
                              filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        return f

    def button_press_handle(self, buttonid):
        '''
        Assign a command for each pressed button.
        '''
        if buttonid == "Generate CodeBWT":
            print(buttonid)
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.result_BWT.delete('1.0', 'end')
            self.controller.string_code_BWT()
            self.widgets_button['Generate CodeBWT'].state(['pressed'])
            self.activate_on_load_BWT()
            self.pattern = '.$'
            # Used for the progress check
            self.resulting_sequence = 'Coded'
        if buttonid == "CompressHuffman":
            print(buttonid)
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.clear_huffman()
            self.widgets_button['CompressHuffman'].state(['pressed'])
            self.controller.compresion_Huffman()
          #  self.compression_choices()
            self.activate_on_load_huffman()
            self.resulting_sequence = 'Compressed'
        elif buttonid == "ReconstructBWT":
            print(buttonid)
            self.clear_pressed_BWT()
            self.clear_pressed_huffman()
            self.result_BWT.delete('1.0', 'end')
            self.controller.reconstruct_BWT()
            self.widgets_button['ReconstructBWT'].state(['pressed'])
            self.activate_on_load_BWT()
            self.pattern = '.*\$$'
            self.resulting_sequence = 'Motif'
        elif buttonid == "Final ResultBWT":
            self.controller.final_result_BWT()
            self.desactivate_buttons_BWT()
        elif buttonid == "DecompressHuffman":
            print(buttonid)
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
        elif buttonid == "SaveBWT":
            print(buttonid)
            self.save_choices()
        elif buttonid == "Load":
            print(buttonid)
            self.controller.load()
        elif buttonid == "NextBWT":
            print(buttonid)
            self.controller.next_button_bwt()
        elif buttonid == "NextHuffman":
            print(buttonid)
            self.controller.next_button_huffman()
        elif buttonid == "Show Tree":
            print(buttonid)
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
           # print("node.name:", name, "x,y:(", x, ",", y, ")l_layer:", layer)
            saw[name] += 1
            if name in saw.keys():
                name += ' ' * saw[name]
            if p_name != "initvalue":
                G.add_edge(p_name, name)
            pos[name] = (x, y)

            l_x, l_y = x - 1 / (3 * layer), y - 1
            # print("l_x, l_y:",l_x, l_y)
            l_layer = layer + 1
            # print("l_layer:",l_layer)
            create_graph(G, node.left, name, x=l_x,
                         y=l_y, pos=pos, layer=l_layer)

            r_x, r_y = x + 1 / (3 * layer), y - 1
            # print("r_x, r_y:", r_x, r_y)
            r_layer = layer + 1
            create_graph(G, node.right, name, x=r_x,
                         y=r_y, pos=pos, layer=r_layer)
            return (G, pos)

        graph = nx.DiGraph()
        graph.name
        graph, pos = create_graph(graph, node)
        # pos["     "] = (0, 0)
        # print("pos:", pos)
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
        # canvas = FigureCanvasTkAgg(self.fig, master=self.frame0)
        # canvas.get_tk_widget().grid()
        # canvas.draw()
        # TODO Zabbeta lal canvas teje ma7alla
        plt.show()

    def test_draw(self):
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v = np.array([16, 16.31925, 17.6394, 16.003, 17.2861,
                      17.3131, 19.1259, 18.9694, 22.0003, 22.81226])
        p = np.array([16.23697,     17.31653,     17.22094,     17.68631,     17.73641,    18.6368,
                      19.32125,     19.31756,    21.20247,   22.41444,  22.11718,   22.12453])

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.scatter(v, x, color='red')
        a.plot(p, range(2 + max(x)), color='blue')
        a.invert_yaxis()

        a.set_title("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_results_huffman)
        canvas.get_tk_widget().grid()
        canvas.draw()

    def open_file(self):
        # file = askopenfile(mode='r')
        file = askopenfilename()
        return file

    def main(self):
        '''
        Main execution of the Tkinter view.
        '''
        self.title("Algo")
        s = ttk.Style()
        s.theme_use('clam')
        self.configure(bg='white')
        self.my_notebook = ttk.Notebook(self)
        self.create_frames()
        self.create_progress_table()
        self.create_labels()
        self.create_fields()

        def trace_when_Entry_widget_is_updated(var, index, mode):
            self.reset_progress_check()
            self.controller.reset()
            self.clear_pressed_BWT()
            self.clear_BWT()
            self.desactivate_buttons_BWT()
            self.clear_pressed_huffman()
            self.clear_huffman()
            self.disable_show_tree()
            self.desactivate_buttons_huffman()
        self.var.trace_variable("w", trace_when_Entry_widget_is_updated)
        # self.attributes("-fullscreen", True)
        self.attributes('-zoomed', True)
        self.mainloop()
