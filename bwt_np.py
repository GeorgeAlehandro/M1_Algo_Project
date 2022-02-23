#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:01:03 2022

@author: s21217588
"""
import numpy as np


class BTW:
    def __init__(self, motif):
        self.motif = motif

    def string_code(self):
        if '$' in self.motif:
            print('Motif containing /$/ cannot be analyzed')
            return False
        list_of_BTW = []
        for i in range(len(self.motif), 0, -1):
            if i == len(self.motif):
                print(self.motif[:i]+'$'+self.motif[i:])
                print(self.motif[i:]+'$'+self.motif[:i])
                # Initializing a np.array
                a = np.array(list(self.motif[:i]+'$'+self.motif[i:]))
                # Adding
                row_to_add = self.motif[i:]+'$'+self.motif[:i]
                a = np.vstack([a, list(row_to_add)])
            else:
                row_to_add = self.motif[i:]+'$'+self.motif[:i]
                print(self.motif[i:]+'$'+self.motif[:i])
                # print(len(row_to_add))
                a = np.vstack([a, list(row_to_add)])
        print(np.shape(a))
        print(a)
        a = a[a[:, 0].argsort()]  # Sort by rows
        string_code = np.ndarray.tolist(a[:, -1])  # Take the last column
        string_code = ''.join(string_code)
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
        for i in range(len(self.motif)-1):
            reconstruction = [m+n for m, n in zip(original, reconstruction)]
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
            i += 1


a = BTW('ACTTGATC')
TEST = BTW('C$GTATATC')
print(a.string_code())
(TEST.reconstruction())
