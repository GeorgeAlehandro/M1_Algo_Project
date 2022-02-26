#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:01:03 2022

@author: s21217588
"""


class BWT:
    def __init__(self, motif=None, string_coded=None):
        self.string_coded = None
        self.motif = None
        if motif is not None:
            if '$' in motif:
                self.string_coded = motif
            else:
                self.motif = motif
        if string_coded is not None:
            if '$' not in motif:
                self.string_coded = string_coded

    def string_code(self):
        # if self.motif is None:
        #     print('Motif should')
        #     return False
        if '$' in self:
            print('Motif containing /$/ cannot be analyzed')
            return False
        list_of_BTW = []
        for i in range(len(self.motif), 0, -1):
            if i == len(self.motif):
                print(self.motif[:i]+'$'+self.motif[i:])
                print(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[:i]+'$'+self.motif[i:])
            else:
                print(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])

        # print(list_of_BTW)
        list_of_BTW.sort()
       # print(list_of_BTW)
        string_code = ''
        length_motif = len(self.motif)
        for el in list_of_BTW:
            string_code += el[length_motif]
        self.string_coded = string_code
        print(string_code)
        return string_code

    def reconstruction(self):
        if '$' not in self:
            print('Encrypted sequence should contain a /$/')
            return False
        original = []
        for _ in self:
            original.append(_)
        # Step b y step list made will be used 7a nzid 3aleya original kel marra after sorting
        reconstruction = []
        for letter in self:
            reconstruction.append(letter)
        reconstruction.sort()
        print(reconstruction)
        for i in range(len(self.string_coded)-1):
            reconstruction = [m+n for m, n in zip(original, reconstruction)]
            print(reconstruction)
            reconstruction.sort()
            print(reconstruction)
        for _ in reconstruction:
            if _.endswith('$'):
                sequence_reconstructed = _[:-1]
                print(sequence_reconstructed)
        self.motif = sequence_reconstructed
        return(sequence_reconstructed)

    def save_transformation(self, file):
        file = open(file, 'w')
        file.write(self.string_code())
        file.close()

    def load_transformation(self, file):
        file = open(file, 'r')
        sequence = str(file.readline())
        print(sequence)
        file = BWT(sequence)
        print(file)
        # file.reconstruction()

    def __iter__(self):
        i = 0
        if self.motif is not None:
            while i < len(self.motif):
                yield self.motif[i]
                i += 1
        if self.string_coded is not None:
            while i < len(self.string_coded):
                yield self.string_coded[i]
                i += 1


a = BWT('nntnacttngnngttncctatacct')
TEST = BWT('ttntanccanntttng$ncacnttgc')
print(a.string_code())
print(type(a))
print(a.string_coded)
a.save_transformation('test')
a.load_transformation('test')
# TEST.reconstruction()
# print(TEST.string_coded)
# print(TEST.motif)
