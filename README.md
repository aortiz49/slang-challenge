# Slang Internship Challenge 2022

# Problem
This challenge involved the consumption of a REST API to obtain information regarding user activity in the app. 
Each activity is comprised of an activity id, a user id, a start time indicating when the activity began, and an end time indicating when the activity was answered. The activites are in no particular order.

The challenge is to organize this data such that it is grouped by user id. Each user will have an array of sessions containing the start time and end time of the session and the activity ids of each activity within the session. 

Below is a diagram detailing the restriction of what constitutes a user session.

<img width="775" alt="Screen Shot 2022-04-09 at 4 41 15 PM" src="https://user-images.githubusercontent.com/3698510/162592429-d8bf7b6e-f960-471b-842d-b6e81525e84e.png">

## Approach
I thought about how to implement this solution for a few hours and planned the algorithm on paper. After a lot of trial and error, (and 7 sheets of paper), I arrived at the conclusion that simply using a list and sorting it for each user was too time consuming. I decided to use a dictionary keyed by `activity_id` to store all the information for a particular activity since the access time for a Python dictionary has a time complexity of O(n). 

While parsing the file, I decided to use a dictionary with `user_id` as they key whose value was a min-heap. I created each min-heap with `first_seen_at` as the invariant and the `activity_id` as the value to store the activities. This allowed me to always be able to pop the activites from the priority queue in chronological order. 

Once I had both of these data structures, I iterated over each user and executed my algorithm that determined which activites belonged to a user session.

## Analysis
Since the primary operation in this algorithm was `pop()` for each of the n activities, I believe the asymptotic time complexity for this algorthim is O(nlogn). 
I'm not entirely sure if my estimation of the overall time complexity is correct since I didn't want to go over the time limit too long. 

Thank you for this opportunity,

Andy Ortiz

