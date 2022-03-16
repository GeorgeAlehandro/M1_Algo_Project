#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:37:10 2022

@author: ubuntu
"""
from huffman import Huffman
from bwt import BWT
import codecs
import copy


class Model(BWT, Huffman):
    def __init__(self, motif=None):
        BWT.__init__(self, motif)
        Huffman.__init__(self, motif)

    def decompression_assign(self):
        '''
        After decompressing the sequence, this method helps the model
        identify if the resulting sequnce is a BWT-transformed sequence or a
        DNA motif
        '''
        if '$' in self.sequence:
            self.BWT_sequence = self.sequence
        else:
            self.DNA_motif = self.sequence

    def load_txt(self, file):
        '''
        Manages the loading process of both txt files
        For normal DNA motifs, and compressed sequences
        '''
        file = codecs.open(file, 'r', encoding='utf-8-sig')
        sequence = file.read()
        print(len(sequence))
        print(sequence)
        if not all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in sequence.upper()):
            # Processes the sequence, makes sure it's viable
            self.coding_partition(sequence)
            # Decompresses the sequence when it's viable, returning the
            # Different attributes for the object Model.
            self.all_decompressing()
        return sequence
