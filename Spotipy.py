import yaml
import pandas as pd
import streamlit as st
import spotipy
import os
import spotipy.oauth2
from spotipy.oauth2 import SpotifyClientCredentials

api_key = os.getenv('SpotifyId')
api_secret = os.getenv('SecretKey')
auth_manager = SpotifyClientCredentials(client_id=api_key,
                                        client_secret=api_secret)
sp = spotipy.client.Spotify(auth_manager=auth_manager)

def playlist_model(url):
    Result = []

    uri = url.split('/')[-1].split('?')[0]
    
    def get_IDs(user, playlist_id):
        try:
            track_ids = []
            playlist = sp.user_playlist(user, playlist_id)
            for item in playlist['tracks']['items']:
                track = item['track']
                track_ids.append(track['id'])
            return track_ids
        except Exception:
            st.error('Update the playlist URL as it seems incorrect.')
            return None
    
    track_ids = get_IDs('Zico', uri)
    if track_ids == None:
        return None
    track_ids_uni = list(set(track_ids))
    
    Spotifyresult = pd.DataFrame()
    for i in range(len(track_ids_uni)):
        if Spotifyresult.shape[0] >= 10:
            break
        try:
            ff = sp.recommendations(seed_tracks=list(track_ids_uni[i:i+5]), limit=5)
        except:
            st.error("Recommendations couldn't be processed. Please, Try Again")
            break
        for z in range(5):
            result = pd.DataFrame()
            result['uri'] = ff['tracks'][z]['id']
            Spotifyresult = pd.concat([Spotifyresult, result], axis=0)
            Spotifyresult.drop_duplicates(subset=['uri'], inplace=True,keep='first')
            if Spotifyresult.shape[0] == 10:
                Result.append(Spotifyresult.iloc[:, 0].tolist())
    return Result

def song_model(url):
    Result = []
    uri = url.split('/')[-1].split('?')[0]
    try:
        aa=sp.recommendations(seed_tracks=[uri], limit=10)
    except:
        st.error('Update the song URL as it seems incorrect.')
        return None
    for i in range(10):
        Result.append(aa['tracks'][i]['id'])
    return Result

def top_tracks(url,region):
    Result = []
    uri = url.split('/')[-1].split('?')[0]
    try:
        top=sp.artist_top_tracks(uri,country=region)
    except:
        st.error("Update the Artist URL as it seems incorrect.")
        return None
    for i in range(10):
        Result.append(top['tracks'][i]['id'])
    return Result
