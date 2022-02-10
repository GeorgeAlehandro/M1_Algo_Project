#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:01:03 2022

@author: s21217588
"""


class BTW:
    def __init__(self, motif):
        self.motif = motif
    
    def string_code(self):
        if '$' in self.motif:
            print('Motif containing /$/ cannot be analyzed')
            return False
        list_of_BTW = []
        for i in range(len(self.motif),0,-1):
            if i == len(self.motif):
                print(self.motif[:i]+'$'+self.motif[i:])
                print(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[:i]+'$'+self.motif[i:])
            else:
                print(self.motif[i:]+'$'+self.motif[:i])
                list_of_BTW.append(self.motif[i:]+'$'+self.motif[:i])
        
        #print(list_of_BTW)
        list_of_BTW.sort()
       # print(list_of_BTW)
        string_code = ''
        length_motif = len(self.motif)
        for el in list_of_BTW:
            string_code += el[length_motif]
        return string_code
    
    def reconstruction(self):
        if '$' not in self:
            print('Encrypted sequence should contain a /$/')
            return False
        original = []
        for _ in self:
            original.append(_)
        ## Step b y step list made will be used 7a nzid 3aleya original kel marra after sorting
        reconstruction = []
        for letter in self:
            reconstruction.append(letter)
        reconstruction.sort()
        print(reconstruction)
        for i in range(len(self.motif)-1):
            reconstruction = [m+n for m,n in zip(original,reconstruction)]
            print(reconstruction)
            reconstruction.sort()
            print(reconstruction)
            print(len(self.motif))
        for _ in reconstruction:
            if _.endswith('$'):
                sequence_reconstructed = _[:-1]
                print(sequence_reconstructed)
                
    def __iter__(self):
        i = 0
        while i < len(self.motif):
          yield self.motif[i]
          i+=1
a = BTW('ACTTGATC')
TEST = BTW('C$TGAATCAGA')
for b in TEST:
    print(b)
print(a.string_code())
(TEST.reconstruction())