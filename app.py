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

import requests

# the url from where the API is to be consumed
url = "https://api.slangapp.com/challenges/v1/activities"

# the authentication header
headers = {'Authorization':  'Basic '
                             'NjU6ckRjd2VyL1BicXN1OGdEMUtGMFFja2JrWWJ3TFNjN2tRbUZ4bXJoQndsUT0='}

# obtain the user activites response from the API
user_activities = requests.get(url, headers=headers).json()

# the python array containing all activites
activity_arr = user_activities['activities']

print()