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

from heapq import heappush
from collections import namedtuple
import requests
import datetime

# the url from where the API is to be consumed
url = "https://api.slangapp.com/challenges/v1/activities"

# the authentication header
headers = {'Authorization':  'Basic '
                             'NjU6ckRjd2VyL1BicXN1OGdEMUtGMFFja2JrWWJ3TFNjN2tRbUZ4bXJoQndsUT0='}

# obtain the user activites response from the API
user_activities = requests.get(url, headers=headers).json()

# the python array containing all activites
activity_arr = user_activities['activities']

# dictionary to store the activities, dictionary to store all activites for a given user
activities_dict, user_activities_dict, user_sessions = dict(), dict(), dict()

# insert all activities
def insert_activites():
    """
    Part 1: Inserting activites

    This inserts all the activities into a dictionary so that we fetch the information from a
    desired activity in constant time.

    Also, for each user, the start time and the activity id for each respective activity he/she
    realized is pushed onto a min-heap ordered by "first_seen_at" so that element 0 is always
    the first activity chronologically speaking.

    Analysis: The time complexity to insert n activites into the min-heaps is O(nlogn).
    """
    for i in range(len(activity_arr)):

        # create namedtuple to represent an activity as a tuple with named fields
        # the first value of the second parameter species the invariant by which to insert
        # in this case, the invariant will be the time the user was first seen for that activity
        Activity = namedtuple("activity", "id user_id first_seen_at answered_at")

        # obtain the attributes of an activity
        activity_id = activity_arr[i]['id']
        user_id = activity_arr[i]['user_id']
        start_time = datetime.datetime.fromisoformat(
            activity_arr[i]['first_seen_at'])
        end_time = datetime.datetime.fromisoformat(
            activity_arr[i]['answered_at'])

        # create a namedtuple with attributes for a given activity_id
        activity = Activity(activity_id, user_id, start_time, end_time)

        # store the activity in the dictionary
        activities_dict[f"{activity_id}"] = activity

        if user_activities_dict.get(f"{user_id}") is None:
            h = []
            user_activities_dict[f"{user_id}"] = h
            heappush(user_activities_dict[f"{user_id}"],
                     (activity.first_seen_at, activity.id))

insert_activites()
print()