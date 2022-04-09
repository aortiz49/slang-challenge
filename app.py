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

#  the url from where the API is to be consumed
url = "https://api.slangapp.com/challenges/v1/activities"

# the authentication header
headers = {'Authorization': 'Basic '
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

        # start a new session by adding the first session activity to the list
        # prev_actvity[1] contains the activity id
        activities = new_session(activities, prev_activity[1])

        # the start time of the session
        start = activities_dict[f"{prev_activity[1]}"][2]

        # counter to keep track of the activities that have already been added to the session
        added_counter = 0

        # while not all activites have been added to the session
        print(f"====> {key}")
        while 1:

            # the "answered_at" attribute of the previous activity
            end_act_1 = activities_dict[f"{prev_activity[1]}"][3]

            # if there is only one activity for the user
            if len(k) == 0 and added_counter == 0:
                last = new_session_dictionary(end_act_1, start, [prev_activity[1]])
                session_arr.append(last)
                finalize_entry(key,session_arr)
                break

            # if there is at least one other activity in the heap...
            # handles edge case for when the previous "first_activity" was the second-to-last
            # activity.
            if len(k) > 0:

                # obtain the current activity at the top of the heap
                curr_activity = heappop(k)
                start_act_2 = activities_dict[f"{curr_activity[1]}"][2]

                # calculate how much time is between the previous and current sessions
                gap = start_act_2.timestamp() - end_act_1.timestamp()

                # if we popped off all activities and the gap between the last two session is less
                # than 300, add the current activity to the current session. This is to handle the
                # edge case in which the last activity is part of the current session
                if len(k) == 0 and gap < 300:
                    activities.append(curr_activity[1])

                # if the gap exceeds the allotted time limit between activites to remain in the
                # current session or if we have popped off all the activites, create the
                # dictioanry of the session
                if gap >= 300 or (len(k) == 0):
                    # the time the session ends is the time the previous activity ended
                    end = activities_dict[f'{prev_activity[1]}'][3]

                    # create the dictionary for the current session
                    session_dictionary = new_session_dictionary(end, start, activities)

                    # append the dictioanry to the current user's sessions array
                    session_arr.append(session_dictionary)
                    print(session_dictionary)

                    # if the current activity has already been added to the session list and we
                    # have already popped off the last activity, do not create a new session.
                    if curr_activity[1] in activities and len(k) == 0:
                        finalize_entry(key, session_arr)
                        break

                        # if the current activity is not in the session list and we have already
                        # popped off the last activity, this means this last activity is more than 5
                        # minutes after the previous activity and will have to be its own session
                    elif curr_activity[1] not in activities and len(k) == 0:
                        end = activities_dict[f"{curr_activity[1]}"][3]
                        last = new_session_dictionary(end, start_act_2, [curr_activity[1]])
                        session_arr.append(last)
                        print(last)
                        finalize_entry(key, session_arr)
                        break

                    # default case if the length of the min-heap is not 0 and if the gap between
                    # sessions is < 300 seconds
                    else:
                        # add the current activity to the activities list since it will be the first
                        # activity in the next session
                        activities = new_session(activities, curr_activity[1])
                        added_counter += 1

                        # the start time of the new session
                        start = activities_dict[f"{curr_activity[1]}"][2]

                # if the time between activities is less than 300 seconds, add it to the list of
                # activities for the current user session
                else:
                    activities.append(curr_activity[1])
                    added_counter += 1

                # the current activity will become the previous activity for the next session
                prev_activity = curr_activity


def finalize_entry(key, session_arr):
    global user_sessions
    user_sessions[f"{key}"] = session_arr


def new_session_dictionary(end, start, activities):
    """
    Creates a dictionary for a user session.

    :param end: the datetime at which the session ended
    :param start: the datetime at which the session started
    :param activities: the list of activities included in the current user session
    :return: a dictionary with the pertinent session information
    """
    my_dictionary = {
        "ended_at": f"{end}",
        "started_at": f"{start}",
        "activity_ids": f"{activities}",
        "duration_seconds": f"{end.timestamp() - start.timestamp()}"
    }

    return my_dictionary


def new_session(activities_arr, activity_id):
    """
    Creates a new session by clearing the activities array and appending the current activity_id
    onto the new session activities list.

    :param activities_arr: the array containing all activity ids of the current session
    :param activity_id: the activity id of the current activity
    :return: the array containing the activity ids
    """
    activities_arr.clear()
    activities_arr.append(activity_id)

    return activities_arr


insert_activites()
build_user_sessions()
print()
