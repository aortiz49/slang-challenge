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

from heapq import heappush, heappop
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

        # create a namedtuple with attributes for a given activity_id. This makes it easier to
        # know which data is which.
        activity = Activity(activity_id, user_id, start_time, end_time)

        # store the activity in the dictionary
        activities_dict[f"{activity_id}"] = activity

        # when a user's id is not a key in the dictionary, create a new array and push the
        # activity onto the min-heap for this user
        if user_activities_dict.get(f"{user_id}") is None:
            h = []
            user_activities_dict[f"{user_id}"] = h
            heappush(user_activities_dict[f"{user_id}"],
                     (activity.first_seen_at, activity.id))

        # if a user's id is already a key in the dictionary, push the tuple with the activity
        # into the min-heap
        else:
            heappush(user_activities_dict[f"{user_id}"],
                     (activity.first_seen_at, activity.id))

def build_user_sessions():
    """
    Part 2: Processing

    This iterates over each key in the dictionary that stores the list of activities and
    calculates the time between successive activites. If this gap time exceeds 5 minutes (300
    seconds) then the subsequent activity gets logged as a unique session. The process is
    repeated for each user until he/she has no more activities.


    Regardless of there being m users and an arbitrary amount of activites associated to each user,
    there are still n activities; they are simply distributed between the users.

    The time complexity to pop n activites from their heaps is O(nlogn).

    """
    for key in user_activities_dict.keys():

        # obtain the min-heap for the current user
        k = user_activities_dict[f"{key}"]

        # array that contains all session dictionaries for the current user
        session_arr = []

        # array that contains the activities of the current session for the current user
        activities = []

        # initial number of activities
        num_activities = len(k)

        # pop the first activity for the current user
        prev_activity = heappop(k)

        # the start time of the session
        start = activities_dict[f"{prev_activity[1]}"][2]

        # for all keys in the dictionary of users
        print(f"====> {key}")
        while len(k) > 0:
            curr_activity = heappop(k)
            print(f"--{curr_activity[1]}")

insert_activites()
build_user_sessions()
print()