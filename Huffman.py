#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:51:07 2022

@author: s21217588
"""
class Node:
    def __init__(self, freq, symbol, left=None, right=None):

        self.freq = freq

        self.symbol = symbol

        self.left = left

        self.right = right

        self.huff = ''
    def __str__(self):
        info = str(self.freq) + self.symbol
        return info

    __repr__ = __str__
class Huffman:
    def __init__(self, motif):
        self.motif = motif

    def calcul_freq(self):
        dico = {}
        for a in self.motif:
            if a not in dico:
                dico[a] = 1
            else:
                dico[a] += 1
        return dico
    def create_nodes(self):
        nodes = []
        dico = self.calcul_freq()
        for symb, freq in dico.items():
            new_node = Node(freq,symb)
            nodes.append(new_node)
        return nodes

    def tree_parser(self):
        tree = self.create_nodes()
        while len(tree) > 1:
            tree = sorted(tree, key=lambda x: x.freq)
            left = tree[0]
            right = tree[1]
            left.huff = 1
            right.huff = 0
            newNode = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
            tree.remove(left)
            tree.remove(right)
            tree.append(newNode)
        return tree
    def recursive_parcours(self, node,val = '', binary_tree_value = {}):
        first_element = self.tree_parser()[0]
        newVal = val + str(node.huff)
        if node.left:
            self.recursive_parcours(node.left, newVal)
        if node.right:
            self.recursive_parcours(node.right, newVal)
        if not node.left and not node.right:
            #print(f"{node.symbol} -> {newVal}")
            binary_tree_value[node.symbol] = newVal
        return(binary_tree_value)
    def binary_transformation(self):
        binary_tree_value = self.recursive_parcours(self.tree_parser()[0])
        compressed = ''
        for nuc in self.motif:
            compressed += binary_tree_value[nuc]

        return compressed
    def binary_coding(self):
        compressed = self.binary_transformation()
        test = [compressed[i:i + 8] for i in range(0, len(compressed), 8)]
        all_encoded = []
        for i in test:
            all_encoded.append(chr(int(i, 2)))
        all_encoded=''.join(all_encoded)
        return (all_encoded)
    def binary_decoding(self):
        all_encoded = self.binary_coding()
        a = [bin(ord(x))[2:].zfill(8) for x in all_encoded]
        return a
    def binary_decompression(self):
        compressed = self.binary_transformation()
        binary_tree_value = self.recursive_parcours(self.tree_parser()[0])
        key_list = []
       # for key in binary_tree_value.keys():
         #   for value in binary_tree_value[key]:
          #      if value in compressed:
           #         key_list.append(key)
        a =''
        for i in compressed:
            i = a+i
            if i in binary_tree_value.values():
                match = list(binary_tree_value.keys())[list(binary_tree_value.values()).index(i)]
                key_list.append(match)
                #print(i)
                i =''
                a=''
            else:
                #print(i)
                a = i
        print(compressed+' becomes '+ ''.join(key_list))
        decrypted_chain = ''.join(key_list)
        return decrypted_chain


o = Huffman('NNTNACTTNGNNGTTNCCTATACCT')
print(o.recursive_parcours(o.tree_parser()[0]))
print(o.binary_transformation())
print(o.binary_coding())
print('ok')
print(o.binary_decoding())
print(o.binary_decompression())