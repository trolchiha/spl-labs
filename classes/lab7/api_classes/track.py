import json
from requests import get, exceptions

from classes.lab7.auth.auth import get_auth_header, get_token
from classes.lab7.settings import BASE_URL

class Track:
    def __init__(self, name):
        self.id = None
        self.track_name = None
        self.artist = None
        self.album = None
        self.spotify_link = None
        self.init_track(name)

    def __init__(self):
        self.id = None
        self.track_name = None
        self.artist = None
        self.album = None
        self.spotify_link = None

    def __str__(self):
        return str(self.get_track_formatted_json())

    def get_track_json_from_api(token, track_name):
        try:
            token = get_token()
            headers = get_auth_header(token)
            url = BASE_URL + "search"
            query = f"?q={track_name}&type=track&limit=1"

            query_url = url + query
            result = get(query_url, headers=headers)
            json_result = json.loads(result.content)["tracks"]["items"]
            if not json_result:
                print("No track with this name exists...")
                return None
            return json_result[0]
        except exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None

        except KeyError as e:
            print(f"Unexpected response format: {e}")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    def init_track(self, name):
        track_json = self.get_track_json_from_api(name)
        
        if track_json is None:
            print("The object was not created")
            return
        
        self.set_values(track_json)
        
    def set_values(self, track_json):
        self.id = track_json["id"]
        self.track_name = track_json["name"]
        artist_id = track_json["artists"][0]["id"]
        artist_name = track_json["artists"][0]["name"]
        artist_link = track_json["artists"][0]["external_urls"]["spotify"]
        self.artist = {"id": artist_id, "name": artist_name, "spotify_link": artist_link}
        album_id = track_json["album"]["id"]
        album_name = track_json["album"]["name"]
        album_link = track_json["album"]["external_urls"]["spotify"]
        self.album =  {"id": album_id, "name": album_name, "spotify_link": album_link}
        self.spotify_link = track_json["external_urls"]["spotify"]
        

    def get_track_formatted_json(self):
        return {
            'id': self.id,
            'track_name': self.track_name,
            'artist': self.artist,
            'album': self.album,
            'spotify_link': self.spotify_link
        }