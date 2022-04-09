# -*- coding: utf-8 -*-

"""
Slang Coding Challenge 2022
April 9, 2022

__author__ = "Andy Ortiz"
__email__ = "a.ortizg@uniandes.edu.co"

This program fetches data from a REST API at a given enpoint and consumes a list of
activites for an arbitrary amount of users in no particular order. It then parses the JSON
file to create a dictionary of user ids and their groups their respective sessions from the list of
their activities if the time between activities exceeds 5 minutes.
"""

