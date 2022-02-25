#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The model file for the MVC structure of the phonebook program.
"""
from controller import Controller
import os

if __name__ == "__main__":
    controller = Controller()
    controller.start_view()
