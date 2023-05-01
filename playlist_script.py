import pandas as pd
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from secret import client_id, client_secret, redirect_uri, playlist_ids
from utils import *

scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
)

user_tracks = sp.current_user_saved_tracks()

tracks = get_user_tracks(sp)
tracks_df = pd.DataFrame(tracks).drop_duplicates(subset=['id'])
features = get_features(sp, tracks_df['id'].to_list())
features_df = pd.DataFrame([feature for feature in features if feature]).drop(columns=["uri","track_href","analysis_url","type"])
df = pd.merge(tracks_df, features_df, left_on="id", right_on="id", how="left")
df['release_year'] = df['release_date'].astype(str).str[0:4].astype(int)
df = df.sort_values(by = 'added_at', ascending=True, ignore_index=True)

queries = [
    'release_year >= 1960 & release_year < 1970',
    'release_year >= 1970 & release_year < 1980',
    'release_year >= 1980 & release_year < 1990',
    'release_year >= 1990 & release_year < 2000',
    'release_year >= 2000 & release_year < 2010',
    'release_year >= 2010 & release_year < 2020',
    'release_year >= 2020 & release_year < 2030',
    'danceability >= 0.5',
    'acousticness >= 0.5',
    'energy >= 0.5',
    'instrumentalness >= 0.5',
    'valence >= 0.5',
    'speechiness >= 0.33',
    'valence < 0.5',
    'energy < 0.5'
]

add_tracks_to_playlists(sp, queries, playlist_ids, df)