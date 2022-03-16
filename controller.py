"""
    controller.py makes the controller part
"""
from __future__ import absolute_import
from model import Model
from tooltip import ToolTip, CreateToolTip
import view
import copy
__author__ = 'George Alehandro Saad'


class Controller():
    '''
    Defining the controller class and its methods.
    '''

    def __init__(self):
        '''
        Controller class constructor.
        '''
        self.view = view.View(self)
        self.model = Model()
        self.operation_BWT = None
        self.operation_Huffman = None

    def start_view(self):
        '''
        Calls for the view interface.
        '''
        self.view.main()

    def string_code_BWT(self):
        '''
        Processes the search request of a person inside the notebook.
        '''
        # Check if Model has an attribute other than None as DNA_motif
        # If so, then the value to be analyzed will be this DNA_motif
        if self.model.DNA_motif is not None:
            # In this case no need to initiate a new Model object
            values_unpack = self.model.DNA_motif
        # If there was no Model() initiate a new one
        if self.model.DNA_motif is None:
            values_unpack = self.view.get_value()
            self.model = Model(values_unpack)
        if values_unpack:
            self.view.progress_check('DNA Motif')
            self.view.progress_check('Decompressed')
            self.operation_BWT = self.model.BWT_transformation()
#            self.view.pedagogic_display(last)

    def compresion_Huffman(self, choice=None):
        '''
        Processes the Huffman's compression operation
        '''
        self.view.disable_show_tree()
        if choice is None:
            if self.model.DNA_motif is not None and self.model.BWT_sequence is not None:
                self.view.compression_choices()
            elif self.model.sequence is not None:
                self.operation_Huffman = self.model.pedagogic_compressing()
            else:
                values_unpack = self.view.get_value()
                if values_unpack:
                    test = Model(values_unpack)
                    self.model = test
                    self.operation_Huffman = self.model.pedagogic_compressing()
        if choice == 'non_BWT' and self.model.DNA_motif is not None:
            self.model.sequence = self.model.DNA_motif
        if choice == 'BWT' and self.model.DNA_motif is not None:
            self.model.sequence = self.model.BWT_sequence
        print('here self.sequence', self.model.sequence)
        self.operation_Huffman = self.model.pedagogic_compressing()
# Todo: MESHEKLE BASS 3AM NEF2OS DECOMPRESS AFTER L COMPRESS

    def reconstruct_BWT(self):
        '''
        Processes the reconstruction of a  DNA sequence from a BWT coded sequence
        '''
        # No change in the entry
        if self.model.BWT_sequence is not None:
            values_unpack = self.model.BWT_sequence
        # If there has been change in the entry
        # Make a new model by using the entry
        elif self.view.get_value() != self.model.DNA_motif:
            values_unpack = self.view.get_value()
        if values_unpack:
            test = Model(values_unpack)
            self.model = test
            self.operation_BWT = self.model.BWT_reconstruction()
        else:
            print('HEHE')

    def decompresion_Huffman(self):
        '''
        Processes the Huffman decompression.
        '''
        if self.model.full_sequence_compressed is not None:
            values_unpack = self.model.full_sequence_compressed
        else:
            values_unpack = self.view.get_value()
            self.view.progress_check('Compressed')
            test = Model(values_unpack)
            self.model = test
            print(self.model.all_encoded)
        self.operation_Huffman = self.model.pedagogic_decompressing()

    def reset(self):
        '''
        Used to re-initialize the Model with an empty one
        '''
        self.model = Model()

    def final_result_BWT(self):
        '''
        Fast forward into the final result of the BWT operation
        '''
        # Fetches the last item of the generator object
        *_, last = self.operation_BWT
        self.view.result_display(last, 'result_BWT')
        # Buttons will be 'Unpressed'
        self.view.clear_pressed_BWT()
        # This will check for the done or not done attributes of hte model
        #
        self.attributes_check()

    def next_button_bwt(self):
        try:
            A = next(self.operation_BWT)
            print(A)
            if isinstance(A, list):
                self.view.result_display(A, 'result_BWT')
        except:
            self.view.clear_pressed_BWT()
            print('la2a error')
            self.view.highlight_BWT()
            self.view.desactivate_buttons_BWT()
            self.attributes_check()

    def final_result_huffman(self):
        *_, last = self.operation_Huffman
        self.view.result_display(last, 'result_huffman')
        self.view.clear_pressed_huffman()
        if hasattr(self.model, 'tree'):
            self.view.enable_show_tree()
        if hasattr(self.model, 'sequence') and self.model.sequence is not None:
            # Decompressed sequnece is assigned to the model.
            self.model.decompression_assign()
            print(self.model.DNA_motif)
            print(self.model.BWT_sequence)
        self.attributes_check()

    def next_button_huffman(self):

        try:
            A = next(self.operation_Huffman)
            print(A)
            self.view.result_display(A, 'result_huffman')
            if hasattr(self.model, 'tree'):
                self.view.enable_show_tree()
            if hasattr(self.model, 'sequence') and self.model.sequence is not None:
                # Decompressed sequnece is assigned to the model.
                self.model.decompression_assign()
        except:
            self.view.clear_pressed_huffman()
            self.view.desactivate_buttons_huffman()
            self.attributes_check()

    def attributes_check(self):
        '''
        Checks for the attributes of the model objects and updates the progres
        check table accodringly
        '''
        # If the model is empty and the attributes are none
        if self.model.full_sequence_compressed is None and self.model.DNA_motif is None and self.model.BWT_sequence is None and self.model.sequence is None:
            sequence_to_track = self.view.get_value()
            return
        # If the model has a DNA_motif sequence, then it's possible to generate
        # The BWT sequence out of it, and also the progress_check can be updated
        if self.model.DNA_motif is not None:
            self.view.widgets_button['Generate CodeBWT'].configure(
                state='normal')
            self.view.progress_check('DNA Motif')
            CreateToolTip(self.view.progress_images['DNA Motif'],
                          text=self.model.DNA_motif)
        # If the model has a BWT sequence, then it's possible to generate the
        # BWT sequence out of it, and also the progress_check can be updated
        if self.model.BWT_sequence is not None:
            self.view.widgets_button['ReconstructBWT'].configure(
                state='normal')
            self.view.progress_check('BWT Coded')
            CreateToolTip(self.view.progress_images['BWT Coded'],
                          text=self.model.BWT_sequence)
        # If the model has a sequence, then it's possible to generate the
        # Compressed sequence out of it, and also the progress_check
        # Can be updated
        if hasattr(self.model, 'sequence') and self.model.sequence is not None:
            self.view.widgets_button['CompressHuffman'].configure(
                state='normal')
            self.view.progress_check('Decompressed')
            CreateToolTip(self.view.progress_images['Decompressed'],
                          text=self.model.sequence)
        # If the model has a full_sequence_compressed, then it's possible to
        # Generate the decompressed sequence out of it, and also
        # The progress_check can be updated
        if hasattr(self.model, 'full_sequence_compressed') and self.model.full_sequence_compressed is not None:
            self.view.widgets_button['DecompressHuffman'].configure(
                state='normal')
            self.view.progress_check('Compressed')
            self.view.progress_check('Decompressed')
            CreateToolTip(self.view.progress_images['Compressed'],
                          text=self.model.full_sequence_compressed)

    def tree_presentation(self):
        '''
        Extracts the tree attribute out of the model in order to plot it in view
        '''
        if hasattr(self.model, 'tree'):
            to_plot = self.model.tree[0]
            self.view.draw(to_plot, 0)

    def save(self, action):
        '''
        Controller call for saving the model.
        '''
        if action == 'Save BWT Coded':
            if self.model.BWT_sequence is not None:
                # Will save the BWT transformation in a bzip2 fle
                file = self.view.file_save(action)
                self.model.save_bzip(file)
            else:
                self.view.failed_save_warning()
        elif action == 'Save DNA Motif':
            if self.model.DNA_motif is not None:
                # Will save the original sequence in a txt fle
                file = self.view.file_save(action)
                self.model.save_reconstruction(file)
            else:
                self.view.failed_save_warning()
        elif action == 'Save Compressed Sequence':
            if self.model.full_sequence_compressed is not None:
                # Will save the compressed sequence in a txt fle
                file = self.view.file_save(action)
                self.model.save_compression(file)
            else:
                self.view.failed_save_warning()
# IF MODEL HAS ATTRIBUTE BLA BLA ACTIVATE

    def reset_operations(self):
        '''
        Used to restart the background operations by turning them into None
        '''
        self.operation_BWT = None
        self.operation_Huffman = None

    def load(self):
        '''
        Controller call for loading the model
        '''
        # Calls for the open_file method in view
        file = self.view.open_file()
        # Creates a Model for the loaded file
        loaded_file = Model()
        # Checks if the file endswith .txt or bz2
        if file.endswith('.txt'):
            # Calls for the load_txt method which reads .txt files
            file = loaded_file.load_txt(file)
            # if hasattr(loaded_file, 'sequence'):
            if loaded_file.sequence is not None:
                self.view.update_entry(loaded_file.sequence)
            else:
                file = file.replace('\n', "")
                print('HERE')
                print(file)
                self.view.update_entry(file)
        if file.endswith('.bz2'):
            # Calls for the load_bzip method which reads compressed files
            file = loaded_file.load_bzip(file)
            self.view.update_entry(file)
