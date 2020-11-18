import json
import time

from spotify_client import SpotifyClient



class LogicManager:
    def __init__(self):
        self.spotify = SpotifyClient()

    @staticmethod
    def find_different_items(new_list, old_list):
        new_items = []

        for i in new_list:
            if i not in old_list:
                new_items.append(i)

        return new_items

    def update_database(self):
        with open("data/playlists.json", mode='r', encoding='utf') as f:
            playlists = json.load(f)

        result = []
        for playlist in playlists:
            items = [x['track']['id'] for x in self.spotify.get_playlist_items(playlist['id'])]
            
            new_items = self.find_different_items(items, playlist['item_ids'])
            del_items = self.find_different_items(playlist['item_ids'], items)

            if new_items or del_items:
                result.append({"id": playlist['id'], "new": new_items, "del": del_items})

            for i in del_items:
                playlist['item_ids'].remove(i)
            playlist['item_ids'].extend(new_items)

        with open("data/playlists.json", mode='w', encoding='utf') as f:
            json.dump(playlists, f, indent=4)

        return result
