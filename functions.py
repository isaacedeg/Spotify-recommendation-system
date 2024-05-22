import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from Spotipy import *
from recommend import *
from streamlit_option_menu import option_menu

data = pd.read_csv('Data/spotify-data.csv')
data.dropna(inplace=True)

def update_radio0():
    st.session_state.feature=st.session_state.radio
    

def update_radio2():
    st.session_state.mode=st.session_state.radio2
    
def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

def update_artist_url():
    st.session_state.a_url = st.session_state.artist_url
    
def update_Region():
    st.session_state.rg=st.session_state.Region
    
def update_song_link():
    st.session_state.s_link = st.session_state.song_link

# Function to capitalize the first letter of each word
def capitalize_words(text):
    return ' '.join(word.capitalize() for word in text.split())

def update_song_url():
    input_song = st.session_state.song_url
    result = capitalize_words(input_song)
    if 'a_name' in st.session_state :
        st.session_state.s_url = get_track_id(result, capitalize_words(st.session_state.a_name), data)

def update_artist_name():
    st.session_state.a_name = st.session_state.artist_name
    

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = (st.session_state.p_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=300)

def artist_page():
    st.subheader("User Artist")
    st.markdown('---')
    artist_uri = (st.session_state.a_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/artist/' + artist_uri
    components.iframe(uri_link, height=80)
    
def song_link():
    st.subheader("User Song")
    st.markdown('---')
    song_uri = (st.session_state.s_link).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/track/' + song_uri
    components.iframe(uri_link, height=100)

def songlink_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs
    with st.spinner('Getting Recommendations...'):
        res = song_model(st.session_state.s_link)
        if res == None:
            return
        st.session_state.rs=res
    try:
        if len(st.session_state.rs)>=1:
            st.success('Go to the Result page to view the top 10 Spotify recommendations.')
        else:
            st.error('Model failed. Make sure the song url is correct.')
    except AttributeError:
        st.error('Please Check that the song URL is correct.')
    

def art_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs
    with st.spinner('Getting Recommendations...'):
        res = top_tracks(st.session_state.a_url, st.session_state.rg)
        if res == None:
            return
        st.session_state.rs=res
    try:
        if len(st.session_state.rs)>=1:
            st.success('Go to the Result page to view the Artist top 10 Track recommendations.')
        else:
            st.error('Model failed. Make sure the artist url is correct.')
    except AttributeError:
        st.error('Please Check that the Artist URL is correct.')
    
def song_page():
    if 's_url' not in st.session_state:
        st.session_state.s_url = '0SjQBdIddPvKSWxr8vk6QX'
    st.subheader("User Song")
    st.markdown('---')
    song_uri = st.session_state.s_url
    uri_link = f'https://open.spotify.com/embed/track/{song_uri}'
    components.iframe(uri_link, height=100)
    
def playlist_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs
        
    with st.spinner('Getting Recommendations...'):
        res = playlist_model(st.session_state.p_url)
        if res == None:
            return
        st.session_state.rs=res
    try:
        if len(st.session_state.rs)>=1:
            st.success('Go to the Result page to view the top 10 Spotify recommendations.')
        else:
            st.error('Model failed. Make sure the playlist url is correct.')
    except AttributeError:
        st.error('Please Check that the playlist URL is correct.')
    
def song_recomm():
    with st.spinner('Getting Recommendations...'):
        try:
            res = recommend_songs(capitalize_words(st.session_state.song_url),
                                  capitalize_words(st.session_state.a_name), data)
            st.session_state.rs=res
        except:
            pass
    try:
        if len(st.session_state.rs)>=1:
            st.success('Go to the Result page to view the top 10 Recommendations.')
        else:
            st.error('Model failed. Make sure the song details are correct.')
    except AttributeError:
        st.error("Oops. It seems the song can't be recognized so try out the Spotify Model.")
    

def home_page():
    if 'radio' not in st.session_state:
        st.session_state.feature="Built-in Model"
        
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Song'
        
    if 'Region' not in st.session_state:
        st.session_state.rg="US"
        
    st.session_state.radio=st.session_state.feature
    st.session_state.radio2=st.session_state.mode
    
    st.title('Zico Recommendation System')
    col,col2,col3=st.columns([2,2,3])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    model = col2.radio("Model",options=("Built-in Model","Spotify Model"), key='radio', on_change=update_radio0)
    if model == 'Spotify Model':
        st.session_state.Region = st.session_state.rg
        
        radio=col.radio("Feature",options=("Playlist","Song","Artist Top Tracks"), key='radio2', on_change=update_radio2)
    
        if radio =="Artist Top Tracks":
            if 'a_url' not in st.session_state:
                st.session_state.a_url = 'Example: https://open.spotify.com/artist/6icQOAFXDZKsumw3YXyusw?si=uC6CYFajQyiyHf4rJTOomQ'
            col3.selectbox("Please Choose Region",index=58,key='Region',on_change=update_Region,
                        options=('AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 
                                    'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 
                                    'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 
                                    'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 
                                    'UY'))
        
        if radio == "Playlist" :
            if 'p_url' not in st.session_state:
                st.session_state.p_url = 'Example: https://open.spotify.com/playlist/49aeRwEL9ANFSIcubXpE5u?si=33d87e28b7594ca6'
                
            st.session_state.playlist_url = st.session_state.p_url
            st.text_input(label="Playlist Url",key='playlist_url',on_change=update_playlist_url)
            playlist_page()
            state =st.button('Get Recommendations')
            with st.expander("Here's how to find any Playlist URL in Spotify"):
                st.write(""" 
                    - Search for Playlist on the Spotify app
                    - Right Click on the Playlist you like
                    - Click "Share"
                    - Choose "Copy link to playlist"
                """)
                st.markdown("<br>", unsafe_allow_html=True)
                st.image('Images/spotify_get_playlist_url.png')
            if state:
                playlist_recomm()
    
        elif radio == "Song" :
            if 's_link' not in st.session_state:
                st.session_state.s_link = 'Example: https://open.spotify.com/track/5kDbL56GBwZwGSOxuFODSX?si=29edb5aeb1f64043'
            st.session_state.song_link = st.session_state.s_link
            st.text_input(label="Song Url",key='song_link',on_change=update_song_link)
            song_link()
            state =st.button('Get Recommendations')
            with st.expander("Here's how to find any Song URL in Spotify"):
                st.write(""" 
                    - Search for Song on the Spotify app
                    - Right Click on the Song you like
                    - Click "Share"
                    - Choose "Copy link to Song"
                """)
                st.markdown("<br>", unsafe_allow_html=True)
                st.image('Images/spotify_get_song_url.png')
            if state:
                songlink_recomm()
            
        elif radio == "Artist Top Tracks" :
            st.session_state.artist_url = st.session_state.a_url
            st.text_input(label="Artist Url",key='artist_url',on_change=update_artist_url)
            artist_page()
            state =st.button('Get Recommendations')
            with st.expander("Here's how to find any Artist URL in Spotify"):
                st.write(""" 
                    - Search for Artist on the Spotify app
                    - Right Click on the Artist you like
                    - Click "Share"
                    - Choose "Copy link to Artist"
                """)
                st.markdown("<br>", unsafe_allow_html=True)
                st.image('Images/spotify_get_artist_url.png')
            if state:
                art_recomm()
    else:
        col.radio("Feature",options=["Song"])
        st.text_input(label="Artist Name",key='artist_name',on_change=update_artist_name, placeholder="Example: Rema")
        st.text_input(label="Song Name",key='song_url',on_change=update_song_url, placeholder="Example: Dumebi")
        song_page()
        with st.expander("Note: If Page Not Available for spotify preview, Read Here"):
                st.write(""" 
                    - Make sure the song name and artist name is correct.
                    - Check out the Spotify Model section to paste a URL link.
                """)
                
        state =st.button('Get Recommendations')
        if state:
            song_recomm()
            
            
def result_page():
    if 'rs' not in st.session_state:
        st.error('Please select a model on the Home page and run Get Recommendations')
    else:
        st.success('Top {} Recommendations'.format(len(st.session_state.rs)))
        for uri in st.session_state.rs:
            uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
            components.iframe(uri_link, height=100)
        
            
def spr_sidebar():
    menu=option_menu(
        menu_title=None,
        options=['Home','Result','About'],
        icons=['house','book','info-square'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if menu=='Home':
        st.session_state.app_mode = 'Home'
    elif menu=='Result':
        st.session_state.app_mode = 'Result'
    elif menu=='About':
        st.session_state.app_mode = 'About'

def About_page():
    st.header('Development')
    st.write("""
    Check out the [repository](https://github.com/isaacedeg/Spotify-recommendation-system) for the source code and approaches, and don't hesitate to contact me if you have any questions. I'm excited to read your review.
    Here is my [Github](https://github.com/isaacedeg) and [Linkedin](https://www.linkedin.com/in/isaac-edegware-4ab966291/). Email : isaacedeg@gmail.com
    """)
    st.subheader('Spotify Million Playlist Dataset')
    st.write("""
    For this project, I'm using the Million Playlist Dataset, which, as its name implies, consists of one million playlists.
    contains a number of songs, and some metadata is included as well, such as the name of the playlist, duration, number of songs, number of artists, etc.
    """

    """
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

    Information about the Dataset [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
    """)
    st.subheader('Audio Features Explanation')
    st.write("""
    | Variable | Description |
    | :----: | :---: |
    | Acousticness | A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. |
    | Danceability | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. |
    | Energy | Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
    | Instrumentalness | Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. |
    | Key | The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1. |
    | Liveness | Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live. |
    | Loudness | The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db. |
    | Mode | Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0. |
    | Speechiness | Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. |
    | Tempo | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
    | Time Signature | An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4". |
    | Valence | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |
    
    Information about features: [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
    """)
