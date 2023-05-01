def get_user_tracks(sp):
    total = sp.current_user_saved_tracks()['total']
    tracks = []
    for i in range(0, total, 50):
        response = sp.current_user_saved_tracks(limit=50, offset=i)
        for track in response['items']:
            tracks.append({
                'id': track['track']['id'], 'added_at': track['added_at'], 'name': track['track']['name'],'album_name': track['track']['album']['name'],
                'release_date': track['track']['album']['release_date'], 'release_date_precision': track['track']['album']['release_date_precision'],
                'artist': track['track']['artists'][0]['name'],'popularity': track['track']['popularity'],
                'explicit': track['track']['explicit']
            })
    return tracks

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def get_features(sp, track_ids):
    features = []
    for chunk in chunker(track_ids, 100):
        features.extend(sp.audio_features([id for id in chunk if id]))
    return features

def get_playlist_tracks(sp, playlist_id):
    total = sp.playlist_tracks(playlist_id)['total']
    tracks = []
    for i in range(0, total, 50):
        response = sp.playlist_tracks(playlist_id, limit = 50, offset=i)
        tracks.extend([item['track']['id'] for item in response['items']])
    return tracks

def add_tracks_to_playlists(sp, queries, playlist_ids, df):
    for (query, playlist_id) in zip(queries, playlist_ids):
        query_df = df.query(query)
        playlist_tracks = get_playlist_tracks(sp, playlist_id)
        new_tracks = query_df[~query_df['id'].isin(playlist_tracks)]['id'].to_list()
        new_tracks = ['spotify:track:' + track for track in new_tracks]
        for chunk in chunker(new_tracks, 50):
            sp.playlist_add_items(playlist_id, chunk)