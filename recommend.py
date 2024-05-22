import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_song(song_name, artist_name, data):
    """Finds the song details in the dataset."""
    if song_name not in data['track_name'].values:
        print(f"'{song_name}' not found in the dataset. Please enter a valid song name.")
        return None
    song = data[(data['track_name'] == song_name) & (data['artist_name'] == artist_name)]
    return song.iloc[0]

def get_song_data(song, artist_name, data):
    song_data = find_song(song, artist_name, data)
    return song_data

def flatten_dict_list(dict_list):
    flattened_dict = {}
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    for dic in dict_list:
        for key,value in dic.items():
            flattened_dict[key].append(value) # creating list of values
    return flattened_dict


number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy',
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

def get_mean_vector(song_list, artist_name, data):
    song_vectors = []
    song_dict = flatten_dict_list(song_list)
    for song in song_dict['track_name']:
        song_data = get_song_data(song, artist_name, data)
        if song_data is None: 
            print('Warning: {} does not exist in database'.format(song['name']))
            break
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)

    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0) 

def recommend_songs(input_song_name, artist_name, data, num_recommendations=10):
    input_song = [{'track_name': input_song_name}]
    mean_vector = get_mean_vector(input_song, artist_name, data)
    
    similarity_scores = cosine_similarity([mean_vector], data[number_cols])

    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    recommendations = data.iloc[similar_song_indices][['track_name', 'popularity', 'track_id']].sort_values(by='popularity', ascending=False)

    return recommendations['track_id'].tolist()


def get_track_id(input_song_name, input_artist_name, data):
    try:
        result = data[(data['track_name'] == input_song_name) & (data['artist_name'] == input_artist_name)]
        return result.iloc[0, data.columns.get_loc('track_id')]
    except IndexError:
        return None