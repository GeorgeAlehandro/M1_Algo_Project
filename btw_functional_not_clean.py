#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 12:28:10 2022

@author: s21217588
"""

# sort = sorted('aza#akk')
# print(('').join(sort))
##########SLIDE 1 
motif = 'AATCGAGTAC'
motif_dollar = motif + '$'

list_of_BTW = []
for i in range(len(motif),0,-1):
    if i == len(motif):
        print(motif[:i]+'$'+motif[i:])
        list_of_BTW.append(motif[i:]+'$'+motif[:i])
        list_of_BTW.append(motif[:i]+'$'+motif[i:])
    else:
        print(motif[i:]+'$'+motif[:i])
        list_of_BTW.append(motif[i:]+'$'+motif[:i])

print(list_of_BTW)
list_of_BTW.sort()
print(list_of_BTW)
string_code = ''
length_motif = len(motif)
for el in list_of_BTW:
    string_code += el[length_motif]
print(string_code)
####################################3 SLIDE 16
##string_code BTW turned into a list that will be added consecutively to others
string_code='C$TGAATCAGA'
original = []
for _ in string_code:
    original.append(_)
## Step b y step list made will be used 7a nzid 3aleya original kel marra after sorting
reconstruction = []
for letter in string_code:
    reconstruction.append(letter)
reconstruction.sort()
print(reconstruction)
for i in range(len(motif)):
    reconstruction = [m+n for m,n in zip(original,reconstruction)]
    print(reconstruction)
    reconstruction.sort()
    print(reconstruction)
for _ in reconstruction:
    if _.endswith('$'):
        sequence_reconstructed = _[:-1]
        print(sequence_reconstructed)