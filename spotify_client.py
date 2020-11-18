import spotipy

from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self):
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def get_playlist_items(self, playlist_id, offset=0):
        playlist_items = self.spotify.playlist_items(playlist_id, offset=offset)['items']

        if len(playlist_items) == 100:
            return playlist_items + self.get_playlist_items(playlist_id, offset+100)
        return playlist_items
        
    def get_track(self, track_id):
        return self.spotify.track(track_id)
    
    def get_playlist(self, playlist_id):
        return self.spotify.playlist(playlist_id)