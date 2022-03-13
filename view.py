# coding: utf-8
"""
SuperView

"""


class SuperView():
    '''
    Super class of both views.
    '''

    def __init__(self, controller):
        '''
        constructor of the super class.
        '''
        self.controller = controller
        self.entries = ["Entry"]
        #self.pedagogic_entries = ["BWT Pedagogic", "HUFFMAN Pedagogic"]
        self.error_messages = ["You need to specify name and surname.",
                               "Error in compressed sequence.",
                               "Sequence can only contain A,T,C,G,N,$",
                               'Entries cannot be all empty.',
                               'Error in BWT sequence inserted. It should consist of only A,T,C,G,N with exactly one $.',
                               "Sequence can only contain A,T,C,G,N",
                               ]

    # def create_interface(self):
    #     pass

    # def get_value(self):
    #     pass

    # def delete_display(self, title, result):
    #     pass

    # def insertion_display(self, title, result):
    #     pass

    # def result_presentation(self, items_list):
    #     '''
    #     Results presentation after fetching.
    #     '''
    #     pass

    # def main(self):
    #     pass
