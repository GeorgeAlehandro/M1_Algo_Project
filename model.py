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
        if '$' in self.sequence:
            self.string_coded = self.sequence
        else:
            self.motif = self.sequence

    def load(self, file):
        file = codecs.open(file, 'r', encoding='utf-8')
        sequence = file.read()
        print(sequence)
        if not all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in sequence.upper()):
            self.coding_partition(sequence)
        else:
            self.__init__(sequence)


# a = Model('ATACAG')
# print(type(a))
# print(a.motif)
# print(a.string_code())
# print(a.string_coded)
# # print(a.sequence)
# # print(a.all_compressing())
# # print(a.binary_tree_value)
# # b = Model('6□	□N$')
# # print(b.binary_tree_value)
# # c = Model()
# # print(c)
# # c.load('FF')
# # print(c.motif)
# # print(c.sequence)
# # e = Model('ATACAGAT'+'\n')
# # print(e.motif)
# # print(e.sequence)
# d = Model('''269
# NF4äçäl8□□N$''')
# d.all_encoded
# d.all_decompressing()
# print(d.binary_tree_value)
# print(d.sequence)
# # d.decompression_assign()
# if hasattr(d, 'sequence'):
#     print(d.motif)
# print(d.all_encoded)
# print(d.string_coded)
