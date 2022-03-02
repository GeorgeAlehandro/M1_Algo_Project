#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:01:03 2022

@author: s21217588
"""
import copy


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
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[:i]+'$'+self.motif[i:])
            else:
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
        list_of_BTW_sorted = copy.deepcopy(list_of_BTW)
        list_of_BTW_sorted.sort()
       # print(list_of_BTW)
        string_code = ''
        length_motif = len(self.motif)
        for element in list_of_BTW_sorted:
            string_code += element[length_motif]
        self.string_coded = string_code
        print(list_of_BTW_sorted)
        print(string_code)
        return string_code, list_of_BTW, list_of_BTW_sorted

    def string_code_pedagogic(self):
        if '$' in self:
            print('Motif containing /$/ cannot be analyzed')
            return False
        list_of_BTW = []
        for i in range(len(self.motif), 0, -1):
            if i == len(self.motif):
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
                yield list_of_BTW
                list_of_BTW.append(self.motif[:i]+'$'+self.motif[i:])
                yield list_of_BTW
            else:
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
                yield list_of_BTW
        list_of_BTW.sort()
        yield list_of_BTW
       # print(list_of_BTW)
        string_code = ''
        length_motif = len(self.motif)
        for element in list_of_BTW:
            string_code += element[length_motif]
     #   yield list_of_BTW
        self.string_coded = string_code
        print(list_of_BTW)
        print(string_code)
        return string_code, list_of_BTW

    def reconstruction(self):
        if '$' not in self:
            print('Encrypted sequence should contain a /$/')
            return False
        #self.wahem_step = []
        original = list(self)  # TRANSOMRED SEQUENCE

        print('this is original', original)
        # Step b y step list made will be used 7a nzid 3aleya original kel marra after sorting
        reconstruction = []
        # self.wahem_step.append(reconstruction)
        for letter in self:
            reconstruction.append(letter)
        # self.wahem_step.append(reconstruction)
        reconstruction.sort()
        print(reconstruction)
        for i in range(len(self.string_coded)-1):
            reconstruction = [m+n for m, n in zip(original, reconstruction)]
            print(reconstruction)
         #   self.wahem_step.append(reconstruction)
            reconstruction.sort()
          #  self.wahem_step.append(reconstruction)
            print(reconstruction)
        for _ in reconstruction:
            if _.endswith('$'):
                sequence_reconstructed = _[:-1]
                print(sequence_reconstructed)
        #self.motif = sequence_reconstructed
        # print(self.wahem_step)
        return sequence_reconstructed

    def reconstruction_pedagogic(self):
        reconstruction = list(self.string_coded)
        yield reconstruction
        original = self.string_coded
        reconstruction.sort()
        for i in range(len(self.string_coded)-1):
            reconstruction = [m+n for m, n in zip(original, reconstruction)]
            yield(reconstruction)
            reconstruction.sort()
            yield(reconstruction)
        for _ in reconstruction:
            if _.endswith('$'):
                sequence_reconstructed = _[:-1]
             #   yield(sequence_reconstructed)
            return 'ENd'

    def save_transformation(self, file):
        file = open(file, 'w')
        file.write(self.string_code())
        file.close()

    def load_transformation(self, file):
        #file = open(file, 'r')
        sequence = str(file.readline())
        print(sequence)
        file = BWT(sequence)
        print(file.string_coded)
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


a = BWT('ACTTGATC')
print(a.motif)
print(a.string_code())
b = BWT('C$GTATATC')
b.reconstruction()
test = a.string_code_pedagogic()
print(a.reconstruction_pedagogic())
print(next(test))
print(next(test))
print(next(test))
print(next(test))
print(next(test))
print(next(test))
print(next(test))
print(next(test))
print(next(test))

# print(next(test))
# # print(type(a))
# # print(a.string_coded)
# a.save_transformation('test')
# a.load_transformation('test')
# # TEST.reconstruction()
# print(TEST.string_coded)
# print(TEST.motif)
