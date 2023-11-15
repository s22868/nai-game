"""
Authors: Mateusz Budzyński, Igor Gutowski

This script provides a function to suggest movies for a given user based on their similarity to other users.

The dataset used in this script is a dictionary of dictionaries containing movie ratings of users.
The dataset is stored in a JSON file and loaded into a Python dictionary using the json module.

The similarity between two users is calculated using the Euclidean distance algorithm.

The script generates a list of 5 movies that are recommended to the user and a list of 5 movies that are not recommended to the user.
"""

import json
import numpy as np

"""
Configuration:
DATAFILE - file with data in JSON format
NAME - username from data file
"""
DATA_FILE = "data.json"
NAME = "Igor Gutowski"


def euclidean_distance(person1, person2):
    common_movies = set(person1.keys()) & set(person2.keys())

    if len(common_movies) == 0:
        return -1

    # Euclidean Distance Algorithm --- https://en.wikipedia.org/wiki/Euclidean_distance
    # sqrt(sum((x-y)^2))

    squared_diff = []
    for item in person1:
        if item in person2:
            squared_diff.append(np.square(person1[item] - person2[item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


with open(DATA_FILE, "r", encoding="utf-8") as f:
    data_json = json.loads(f.read())

def suggest_movie(name):
    """
    Suggest movies for a given user based on their similarity to other users.

    Parameters:
    - user (str): The user for whom movie suggestions are to be made.

    Raises:
    TypeError: If the specified user is not found in the dataset.
    """

    # Check if the user exists in the dataset
    if name not in data_json:
        raise TypeError(f"Cannot find {name} in the dataset")

    # Get a list of all users except the given user
    data = list(data_json.keys())
    data.remove(name)

    # Calculate Euclidean distances between the given user and others
    distance = {
        data_name: euclidean_distance(data_json[name], data_json[data_name])
        for data_name in data
        if euclidean_distance(data_json[name], data_json[data_name]) != -1
    }

    # Find the smallest Euclidean distance (most similar)
    sorted_distance = sorted(distance.items(), key=lambda dist: dist[1])
    most_similar = sorted_distance[0][0]

    # Sort movies rated by the most similar user and suggest top 5 and bottom 5
    sorted_movies = sorted(
        data_json[most_similar].items(), key=lambda rating: rating[1], reverse=True
    )
    recommended_movies = [movie for movie, _ in sorted_movies[:5]]
    not_recommended_movies = [movie for movie, _ in sorted_movies[-6:-1]]
    
    print(NAME)
    print("Rekomendowane:")
    print(recommended_movies)
    print("Nierekomendowane:")
    print(not_recommended_movies)


suggest_movie(NAME)
