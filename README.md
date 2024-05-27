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

## Folder Structure
* Images : Contains all the images needed for description.
* data-preprocessing.ipynb : Contains the extraction and cleaning of the dataset.
* Data-Visualization.ipynb : As the name implies, It contains Visualizations of the dataset.
* Clustering-Phase.ipynb: As the name implies, It contains the Clustering phase for the dataset .
* Spotipy.py : Contains the functions to have access to the Spotify developer api and make recommendations based on spotify endpoints.
  We'll need a [Spotify for developers](https://developer.spotify.com/) account for this. This is equivalent to a Spotify account and does not necessitate Spotify Premium. Go to the dashboard and select "create an app" from there. We now have access to the public and private keys required to use the API.

Now that we have an app, we can get a client ID and a client secret for this app. Both of these will be required to authenticate with the Spotify web API for our application, and can be thought of as a kind of username and password for the application. It is best practice not to share either of these, but especially don’t share the client secret key. To prevent this, we can keep it in a separate file, which, if you’re using Git for version control, should be Gitignored.

Spotify credentials should be stored the in the a `Spotify.yaml` file with the first line as the **credential id** and the second line as the **secret key**:
```python
Client_id : ************************
client_secret : ************************
```
To access this credentials, please use the following code:
```python
stream= open("Spotify/Spotify.yaml")
spotify_details = yaml.safe_load(stream)
auth_manager = SpotifyClientCredentials(client_id=spotify_details['Client_id'],
                                        client_secret=spotify_details['client_secret'])
sp = spotipy.client.Spotify(auth_manager=auth_manager)
```
* app.py : This file is the main app to run.
* recommend.py: Contains all the functions to process recommendations based on the dataset that I used.
* requirements.txt : Lists the Python libraries required for this project.

### Deployment
Please visit the following link to access the app's final version: https://huggingface.co/spaces/isaacedeg/Zico-Recommendation
The website can be accessed and tested out there. Due to the limitations of file sizes and RAM limits, I decided to go with
[huggingface](https://huggingface.co/) because the free version is not severely limited.  

You can test the app on localhost by cloning the repository data, cd into the folder and run the following commands:
```python
streamlit run app.py
```
Installing dependencies:
```python
pip install -r requirements.txt
```
