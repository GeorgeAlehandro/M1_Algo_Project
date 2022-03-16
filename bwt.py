#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: George Alehandro Saad
"""
import bz2


class BWT:
    '''
    BWT Class for all the necessary BWT transformations
    '''

    def __init__(self, DNA_motif=None, BWT_sequence=None):
        '''
        Constructor of the BWT part of the model, it can contain 2 different
        stades either DNA_motif or BWT_sequence or both
        '''
        # Declaring DNA_motif attribute
        self.DNA_motif = None
        # Declaring BWT_sequence attribute
        self.BWT_sequence = None
        # Declaring how the arguments can be interpreted
        if DNA_motif is not None:
            # Assigning the first argument
            if all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in DNA_motif.upper()):
                DNA_motif = DNA_motif.lstrip().rstrip().replace('\n', "").upper()
                if '$' in DNA_motif:
                    self.BWT_sequence = DNA_motif.upper()
                else:
                    self.DNA_motif = DNA_motif.upper()
        if BWT_sequence is not None:
            # Assigning the first argument
            if all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in BWT_sequence.upper()):
                BWT_sequence = BWT_sequence.lstrip().rstrip().replace('\n', "").upper()
                if '$' not in DNA_motif:
                    self.BWT_sequence = BWT_sequence.upper()

    def BWT_transformation(self):
        '''
        BWT transformation method
        '''
        # Input verification
        if '$' in self:
            print('Motif containing /$/ cannot be BWT-transformed')
            return False
        # Creation of empty list
        list_of_BTW = []
        # Itterating over the list, starting from the largest i
        # This itterations begins with the biggest number until the smallest
        for i in range(len(self.DNA_motif), 0, -1):
            # This one is specific for the first i
            if i == len(self.DNA_motif):
                # This is the sequence itself with a '$' in the end
                list_of_BTW.append(self.DNA_motif[i:]+'$'+self.DNA_motif[:i])
                yield list_of_BTW  # For the next button
                # Second sequence to be appended
                list_of_BTW.append(self.DNA_motif[:i]+'$'+self.DNA_motif[i:])
                yield list_of_BTW
            else:
                list_of_BTW.append(self.DNA_motif[i:]+'$'+self.DNA_motif[:i])
                yield list_of_BTW
        # Sort by lexicographic order
        list_of_BTW.sort()
        yield list_of_BTW
        string_code = ''
        length_motif = len(self.DNA_motif)
        for element in list_of_BTW:
            string_code += element[length_motif]
        self.BWT_sequence = string_code

        yield string_code

    def BWT_reconstruction(self):
        '''
        BWT reconstruction method, finds the reconstructed sequence from the
        BWT coded sequence.
        '''
        # Creation of a List of all the letters of the BWT_sequence attribute
        reconstruction = list(self.BWT_sequence)
        # First yield gives back the initial BWT_sequence, but as a list
        yield reconstruction
        reconstruction.sort()
        for i in range(len(self.BWT_sequence)-1):
            reconstruction = [m+n for m,
                              n in zip(self.BWT_sequence, reconstruction)]
            yield(reconstruction)
            reconstruction.sort()
           # print('here')
            yield(reconstruction)
        for _ in reconstruction:
            if _.endswith('$'):
                sequence_reconstructed = _[:-1]
                self.DNA_motif = sequence_reconstructed
                yield(sequence_reconstructed)

    def save_reconstruction(self, file):
        file = open(file, 'w')
        if self.DNA_motif is None:
            self.reconstruction()
        file.write(self.DNA_motif)
        file.close()

    def __iter__(self):
        '''
        __iter__ would dictate how both attributes of a BWT object can be
        ittered upon
        '''
        i = 0
        if self.DNA_motif is not None:
            while i < len(self.DNA_motif):
                yield self.DNA_motif[i]
                i += 1
        if self.BWT_sequence is not None:
            while i < len(self.BWT_sequence):
                yield self.BWT_sequence[i]
                i += 1

    def save_bzip(self, file):
        '''
        Saves the transformed BWT sequence into a zipped file
        Using bzip2
        '''
        data = self.BWT_sequence
        data = data.encode('utf-8')
        file = open(file, 'wb')
        data_compressed = bz2.compress(data)
        file.write(data_compressed)
        file.close()

    def load_bzip(self, file):
        '''
        loads the zipped file of the transformed BWT sequence
        '''
        file = open(file, 'rb')
        data = file.read()
        decompressed_sequence = bz2.decompress(data).decode('utf-8')
        # The decompressed_sequence is a BWT sequence on it's own, when
        # Creating an object, this loaded bzip2 file will constitute the BWT
        # Part of the model
        self.BWT_sequence = decompressed_sequence
        return decompressed_sequence
