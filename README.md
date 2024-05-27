# Spotify-Recommendation-System
The goal of this project is to create a recommendation system that would allow users to discover music based on a given playlist or song that they already enjoy. This project begins with data collection, pre-processing, visualizations and a self-growing dataset to ensure that the model will work well in the future and continues through model deployment.


## Description
For this project, I'm using the Million Playlist Dataset, which, as its name implies, consists of one million playlists.
contains a number of songs, and some metadata is included as well, such as the name of the playlist, duration, number of songs, number of artists, etc.

It is created by sampling playlists from the billions of playlists that Spotify users have created over the years. 
Playlists that meet the following criteria were selected at random:
- Created by a user that resides in the United States and is at least 13 years old
- Was a public playlist at the time the MPD was generated
- Contains at least 5 tracks
- Contains no more than 250 tracks
- Contains at least 3 unique artists
- Contains at least 2 unique albums
- Has no local tracks (local tracks are non-Spotify tracks that a user has on their local device
- Has at least one follower (not including the creator
- Was created after January 1, 2010 and before December 1, 2017
- Does not have an offensive title
- Does not have an adult-oriented title if the playlist was created by a user under 18 years of age

Check out the dataset [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)

