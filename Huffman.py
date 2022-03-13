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
import codecs
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import copy


class Node:
    '''
    Nodes class used to create the tree of the Huffman's compression
    '''

    def __init__(self, freq, symbol, left=None, right=None):
        '''
        Constructor of the Nodes class
        '''
        # For each node there is a calculated frequence
        self.freq = freq
        # For each node there is a symbol
        self.symbol = symbol
        # For each node if there it has another node on its left
        self.left = left
        # For each node if there it has another node on its right
        self.right = right
        # Calculations for each path to the node, being a sequence of 0s and 1s
        self.branch = ''

    def __str__(self):
        '''
        Modifiying the print statement for each node object
        '''
        # The print statement will return the frequence and symbol of each node
        info = str(self.freq) + self.symbol
        return info
    # To specify how the object will be presented textually when printing
    __repr__ = __str__


class Huffman:
    '''
    Huffman class for all the Huffman's operations including compression and
    decompression
    '''

    def __init__(self, entry=None):
        '''
        Constructor of the class
        '''
        # Sequence is the combination that will be compressed
        self.sequence = None
        if entry is not None:
            # Verification of entry and unifying the syntax eliminating spaces
            if all(letter in ['A', 'T', 'C', 'G', 'N', '\n', '$'] for letter in entry.upper()):
                self.sequence = entry.lstrip().rstrip().replace('\n', "").upper()
            else:
                self.coding_partition(entry)
        else:
            self.sequence = None
        # self.dico = None
        # self.nodes = None
        # self.tree = None
        # self.binary_tree_value = None
        # self.compressed = None
        # self.all_encoded = None
        # self.reconstructed_binary = None
        # self.decrypted_chain = None
        # self.dict_compressed = None

    def calcul_freq(self):
        '''
        Calculer la frequence de chaque lettre
        '''
        dico = {}
        for a in self.sequence:
            if a not in dico:
                dico[a] = 1
            else:
                dico[a] += 1
        self.dico = dico
        return 'Has the following frequences ' + str(dico)

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
        return 'Which will constitute theses nodes ' + str(nodes)

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
        return 'Overview of the tree ' + str(tree)  # LIST OF A NODE

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
        return 'The following resulting dictionnary ' + str(binary_tree_value)

    def binary_transformation(self):
        '''
        Transforms the sequence into a binary number based on the tree's values
        '''
        binary_tree_value = self.binary_tree_value
        compressed = ''
        for nuc in self.sequence:
            compressed += binary_tree_value[nuc]
        self.compressed = compressed
       # return 'The nucleotide sequence is then turned into :' + str(compressed)
        return self.sequence + '---->' + str(compressed)

    def binary_coding(self):
        '''
        Tree values turned into characters
        '''
        compressed = self.compressed  # String of 0s and ones
        # Binary sequence will be divided into pieces of 8
        partition = [compressed[i:i + 8] for i in range(0, len(compressed), 8)]
       # print(partition)
        all_encoded = ''
        for i in range(len(partition)):
            all_encoded += chr(int(partition[i], 2))
            # To take care of the last piece of the bit, which will not be
            # forcefully of length 8
        # Appending the length of the last bit that would be used for decompressing

        all_encoded += str(len(partition[-1]))

        # print(self.sequence + ' has the code ' + all_encoded)
        self.all_encoded = all_encoded
        return self.sequence + '---->' + str(compressed) + '---->'+str(all_encoded)

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
#        print(self.sequence + ' becomes ' + str(reconstructed_binary))
        self.reconstructed_binary = reconstructed_binary
        self.compressed = ''.join(reconstructed_binary)
        return 'The binary reconstruction of the sequence is '+str(reconstructed_binary)

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
        decrypted_chain = ''.join(key_list)
        # print(str(compressed)+' becomes below')
        # print(decrypted_chain)
        self.decrypted_chain = decrypted_chain
        self.sequence = decrypted_chain
        return str(compressed)+' becomes ' + str(decrypted_chain)

    def save_transformation(self, file):
        file = open(file, 'w')
        file.write(self.all_encoded)
        # print('The whole sequence written is ')
        # print(len(self.all_encoded))
        # print(len(self.dict_compressed))
        # print(self.all_encoded+self.dict_compressed)
        file.write(self.dict_compressed)
        # print('Whole len should be written: ' +
        #       str((len(self.all_encoded)+len(self.dict_compressed))))
        file.close()

    def coding_partition(self, entry):
        begin_dict = entry.index('□')
        str_rep_of_dic = entry[begin_dict:len(entry)]
        self.dict_compressed = str_rep_of_dic
        # print(self.dict_compressed)
        self.decompressing_dict()
        # print('coding_partition')
        # print(entry)
        self.all_encoded = entry[0:begin_dict]

    def load_transformation(self, file):
        file = codecs.open(file, 'r', encoding='utf-8')
        sequence = file.read()
        self.coding_partition(sequence)

    # def dict_values(self):
    #     compress = ''
    #     for value in self.binary_tree_value.values():
    #         print(value)

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
        □ + compressed values each in one character + □ + missing_letters
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
        self.dict_compressed = values_compressed
        self.full_sequence_compressed = self.all_encoded + self.dict_compressed
        return 'The dictionnary is encoded as' + '"'+str(values_compressed)+'"'

    def pedagogic_compressing(self):
        yield self.sequence
        yield self.calcul_freq()
        yield self.create_nodes()
        self.tree_parser()
      #  yield self.draw(self.tree[0], 0)
        yield self.recursive_parcours()
        yield self.sequence
        yield self.binary_transformation()
        yield self.binary_coding()
        yield self.compressing_dict()
        yield 'Full encoding of the sequence: ' + '"'+self.all_encoded + self.dict_compressed+'"'

    def pedagogic_decompressing(self):
        yield self.binary_decoding()
        yield self.binary_decompression()
        yield self.decompressing_dict()
        # yield 'Full encoding of the sequence: ' + self.all_encoded + self.dict_compressed

    def decompressing_dict(self):
        lst = []
        for pos, char in enumerate(self.dict_compressed):
            if char == '□':
                lst.append(pos)
        to_map = []
        begin_number = lst[0]+1
        end_number = lst[1]
        numbers = self.dict_compressed[begin_number:end_number]
        for number in numbers:
            back_to_old = bin(ord(number))[3:]  # Removes 0b1
         #   print((back_to_old))
            to_map.append(back_to_old)
        new = {'$': None, 'A': None, 'C': None, 'G': None,
               'N': None, 'T': None}
        letters = [word for word in self.dict_compressed if word.isalpha()
                   or word == '$']
        for letter in letters:
            del new[letter]
        keys_of_dict = list(new)
        # print(keys_of_dict)
        for i in range(len(new)):
            new[keys_of_dict[i]] = to_map[i]
        self.binary_tree_value = new
        return 'The reconstruction of the dictionary gives back ' + str(self.binary_tree_value)

    def draw(self, node, data):   # Draw a node as root
        saw = defaultdict(int)

        def create_graph(G, node, p_name="initvalue", pos={}, x=0, y=0, layer=1):
            if not node:
                return
            name = str(node.symbol)
           # print("node.name:", name, "x,y:(", x, ",", y, ")l_layer:", layer)
            saw[name] += 1
            if name in saw.keys():
                name += ' ' * saw[name]
            if p_name != "initvalue":
                G.add_edge(p_name, name)
            pos[name] = (x, y)

            l_x, l_y = x - 1 / (3 * layer), y - 1
            # print("l_x, l_y:",l_x, l_y)
            l_layer = layer + 1
            # print("l_layer:",l_layer)
            create_graph(G, node.left, name, x=l_x,
                         y=l_y, pos=pos, layer=l_layer)

            r_x, r_y = x + 1 / (3 * layer), y - 1
            # print("r_x, r_y:", r_x, r_y)
            r_layer = layer + 1
            create_graph(G, node.right, name, x=r_x,
                         y=r_y, pos=pos, layer=r_layer)
            return (G, pos)

        graph = nx.DiGraph()
        graph.name
        graph, pos = create_graph(graph, node)
        # pos["     "] = (0, 0)
        # print("pos:", pos)
        # Scale can be adjusted appropriately according to the depth of the tree
        fig, ax = plt.subplots(figsize=(8, 10))
        color_map = []
        # for j,node in enumerate(graph.nodes):
        # for degree in graph.out_degree:
        #     if int(degree[0]) in data and degree[1] == 0:
        #         color_map.append('blue')
        #     else:
        #         color_map.append('green')
        # nx.draw(G, node_color=color_map, with_labels=True)
        nx.draw_networkx(graph, pos, ax=ax, node_size=1000,
                         node_color=color_map)
        plt.show()
        return 'With this tree'


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
