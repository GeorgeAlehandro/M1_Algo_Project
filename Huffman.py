#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:51:07 2022

@author: s21217588
"""
import json
import io
import pickle
import zlib
import ast


class Node:
    def __init__(self, freq, symbol, left=None, right=None):

        self.freq = freq

        self.symbol = symbol

        self.left = left

        self.right = right

        self.branch = ''

    def __str__(self):
        info = str(self.freq) + self.symbol
        return info

    __repr__ = __str__


class Huffman:
    def __init__(self, motif=None):
        if motif is not None:
            self.motif = motif
        else:
            self.motif = None
        self.dico = None
        self.nodes = None
        self.tree = None
        self.binary_tree_value = None
        self.compressed = None
        self.all_encoded = None
        self.reconstructed_binary = None
        self.decrypted_chain = None
        self.dict_compressed = None

    def calcul_freq(self):
        '''
        Calculer la frequence de chaque lettre
        '''
        dico = {}
        for a in self.motif:
            if a not in dico:
                dico[a] = 1
            else:
                dico[a] += 1
        self.dico = dico
        return dico

    def create_nodes(self):
        '''
        list of nucleotides and their frequences inside a node item.
        '''
        nodes = []
        self.calcul_freq()
        dico = self.dico
        for symb, freq in dico.items():
            new_node = Node(freq, symb)
            nodes.append(new_node)
        self.nodes = nodes
        return nodes

    def tree_parser(self):
        '''
        Sorts and sums the nodes
        '''
        self.create_nodes()
        tree = self.nodes  # list
        while len(tree) > 1:
            # list will be sorted
            tree = sorted(tree, key=lambda x: x.freq)
            # take first two elements of the list
            left = tree[0]
            right = tree[1]
            # give scores to trajectories
            left.branch = 1
            right.branch = 0
            # create a new node that is the sum of both of the lists
            newNode = Node(left.freq + right.freq,
                           left.symbol + right.symbol, left, right)
            # delete those 2 lists as they have been replaced
            tree.remove(left)
            tree.remove(right)
            # insert newNode inside (sum of the smallest two nodes)
            tree.append(newNode)
        self.tree = tree
        return tree  # LIST OF A NODE

    def recursive_parcours(self, node=None, val='', binary_tree_value={}):
        '''
        Recursive function to retrieve all the values of the different symbols
        inside the tree
        '''
        # first_element = self.tree_parser()[0]
        if node is None:
            node = self.tree[0]
        newVal = val + str(node.branch)  # addingg 0 or 1 within the directions
        if node.left:
            self.recursive_parcours(node.left, newVal)
        if node.right:
            self.recursive_parcours(node.right, newVal)
        if not node.left and not node.right:
            # print(f"{node.symbol} -> {newVal}")
            binary_tree_value[node.symbol] = newVal
        self.binary_tree_value = binary_tree_value
        return(binary_tree_value)

    def binary_transformation(self):
        '''
        Transforms the motif into a binary number based on the tree's values
        '''
        binary_tree_value = self.binary_tree_value
        compressed = ''
        for nuc in self.motif:
            compressed += binary_tree_value[nuc]
        self.compressed = compressed
        return compressed

    def binary_coding(self):
        '''
        Tree values turned into characters
        '''
        compressed = self.compressed  # String of 0s and ones
        # Binary sequence will be divided into pieces of 8
        partition = [compressed[i:i + 8] for i in range(0, len(compressed), 8)]
        print(partition)
        all_encoded = ''
        for i in range(len(partition)):
            all_encoded += chr(int(partition[i], 2))
            # To take care of the last piece of the bit, which will not be
            # forcefully of length 8
        # Appending the length of the last bit that would be used for decompressing

        all_encoded += str(len(partition[-1]))

        print(self.motif + ' has the code ' + all_encoded)
        self.all_encoded = all_encoded
        return (all_encoded)

    def binary_decoding(self):
        '''
        Turns encoded characters into binary 8bits
        '''
        all_encoded = self.all_encoded  # Coded file
        # Extracts the last character of the coded file to know the size of the
        # last bit
        how_many_0 = all_encoded[-1]
       # print('here', how_many_0)
        reconstructed_binary = []
        for i in range(len(all_encoded)-1):
            if i == len(all_encoded)-2:
                # Filling will be done depending on the length of the saved sequence
                # [2:] removes the 2b indicator
                reconstructed_binary.append(bin(ord(all_encoded[i]))[
                    2:].zfill(int(how_many_0)))
            else:
                reconstructed_binary.append(
                    bin(ord(all_encoded[i]))[2:].zfill(8))
#        print(self.motif + ' becomes ' + str(reconstructed_binary))
        self.reconstructed_binary = reconstructed_binary
        return reconstructed_binary

    def binary_decompression(self):
        '''
        Iterating through the compressed file, until finding a match
        '''
        compressed = self.reconstructed_binary
        binary_tree_value = self.binary_tree_value
        key_list = []
        residual = ''
        for i in ''.join(compressed):
            i = residual+i
            if i in binary_tree_value.values():
                match = list(binary_tree_value.keys())[
                    list(binary_tree_value.values()).index(i)]
                key_list.append(match)
                # Reset the iteration factors
                i = ''
                residual = ''
            else:
                # Takes the unmatched part, adds it to the next iteration
                residual = i
        print(str(compressed)+' becomes ' + ''.join(key_list))
        decrypted_chain = ''.join(key_list)
        self.decrypted_chain = decrypted_chain
        return decrypted_chain

    def save_transformation(self, file):
        file = open(file, 'wb')
      #  file.write(self.all_encoded)
        print('The whole sequence written is ')
        print(len(self.all_encoded))
        print(len(self.dict_compressed))
        print(self.all_encoded+self.dict_compressed)
       # test_zip = zlib.compress(self.all_encoded+self.dict_compressed)
        # file.write(self.all_encoded+self.dict_compressed)
        pickle.dump(self.all_encoded+self.dict_compressed, file)
        print('Whole len should be written: ' +
              str((len(self.all_encoded)+len(self.dict_compressed))))
        file.close()

    def load_transformation(self, file):
        file = open(file, 'rb')
       # sequence = file.read()
        sequence = pickle.load(file)
        begin_dict = sequence.index('□')
        #begin_dict = sequence.index('{')
        print('Whole len of the loaded sequence: ' + str(len(sequence)))
        print(sequence)
        str_rep_of_dic = sequence[begin_dict:len(sequence)]
        self.dict_compressed = str_rep_of_dic
        print("Check here", self.dict_compressed)
        self.decompressing_dict()
        print(type(self.binary_tree_value))
        self.all_encoded = sequence[0:begin_dict]
        print('dictionnaire', self.binary_tree_value)
        print('here', self.all_encoded)

    def dict_values(self):
        compress = ''
        for value in self.binary_tree_value.values():
            print(value)

    def all_compressing(self):
        self.calcul_freq()
        self.create_nodes()
        self.tree_parser()
        self.recursive_parcours()
        self.binary_transformation()
        self.binary_coding()

    def all_decompressing(self):
        self.binary_decoding()
        self.binary_decompression()

    def compressing_dict(self):
        '''
        Used to compress the dictionnary (self.binary_tree_value)
        { + compressed values each in one character + } + missing_letters
        '''
        self.binary_tree_value = dict(sorted(self.binary_tree_value.items()))
        values_compressed = ''
        for value in self.binary_tree_value.values():
            protection = '1' + value
            # print(value)
            # int_from_binary = str(int(protection,2))
            values_compressed += chr(int(protection, 2))
      #  values_compressed = '□'+values_compressed + '□'
        values_compressed = '□'+values_compressed + '□'
        check = ['A', 'T', 'C', 'G', 'N', '$']
        for nuc in check:
            if nuc not in self.binary_tree_value.keys():
                values_compressed += nuc
        print(values_compressed)
        print(len(values_compressed))
        self.dict_compressed = values_compressed
        print(len(self.dict_compressed))
        return values_compressed

    def decompressing_dict(self):
        lst = []
        print('Length of seld.dict_compressed', len(self.dict_compressed))
        for pos, char in enumerate(self.dict_compressed):
            if char == '□':
                lst.append(pos)
                print('FOUND')
                print(pos)
        print('This is list', lst)
        to_map = []
        # begin_number = self.dict_compressed.index('{')+1
        # end_number = self.dict_compressed.index('}')
       # print(begin_number, end_number)
        # only takes the numbers
        numbers = self.dict_compressed[lst[0]+1:lst[1]]
        print(numbers)
        # print(numbers)
        # print(len(numbers))
        print('here')
        print(to_map)
        for number in numbers:
            back_to_old = bin(ord(number))[3:]  # Removes 0b1
         #   print((back_to_old))
            to_map.append(back_to_old)
            print(back_to_old)
        print(to_map)
        new = {'$': None, 'A': None, 'C': None, 'G': None,
               'N': None, 'T': None}
        letters = [word for word in self.dict_compressed if word.isalpha()
                   or word == '$']
        for letter in letters:
            del new[letter]
        print(new)
        keys_of_dict = list(new)
        # print(keys_of_dict)
        print(len(to_map))
        print(len(new))
        for i in range(len(new)):
            new[keys_of_dict[i]] = to_map[i]
        print(self.binary_tree_value)
        self.binary_tree_value = new
        print(new)


def dict2File(data, filename):
    bytes = io.BytesIO()
    pickle.dump(data, bytes)
    # we compress this bytes
    zbytes = zlib.compress(bytes.getbuffer())
    # create a file and store the compressed bytes to file
    with open(filename, 'wb') as fd:
        fd.write(zbytes)


def file2Dict(filename):
    with open(filename, 'rb') as fd:
        zbytes = fd.read()
    # decompress this zbytes again
    bytes = zlib.decompress(zbytes)
    return pickle.loads(bytes)


test_all_new = Huffman('ATGGCGGC$GGTCACGTATTAAACAA')
# ATGGCGGC$GGTCACGTATTAAACAA test with this
test_all_new.all_compressing()
test_all_new.compressing_dict()
print('here test_all.all_encoded '+str(len(test_all_new.all_encoded)))
# print(type(test_all_new.all_encoded))
# print(test_all_new.all_encoded)
# print(type(test_all_new.dict_compressed))
# print(test_all_new.dict_compressed)
# print(test_all_new.compressed)
# print('here test_all.compressed_cict '+str(len(test_all_new.dict_compressed)))
# print('herllo')'
print(test_all_new.binary_tree_value)
# test_all_new.decompressing_dict()
test_all_new.save_transformation('test_mix.txt')
# print(test_all_new.compressed)
# print(test_all_new.binary_tree_value)
last_test = Huffman()
last_test.load_transformation('test_mix.txt')
last_test.all_decompressing()
print('Same dictionnary codage? ' +
      str(str(last_test.dict_compressed == test_all_new.dict_compressed)))
print('Same dictionarries?' +
      str(last_test.binary_tree_value == test_all_new.binary_tree_value))
# print(last_test.all_encoded)
# test_all_new.save_transformation('test_dico_big_combo.txt')
# test_load = Huffman()
# test_load.load_transformation('test_dico_big_combo.txt')
# test_load.all_decompressing()
