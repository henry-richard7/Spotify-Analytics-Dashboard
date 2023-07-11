import requests
from random import shuffle

def token():
        """
        Retrieves an access token from the Spotify API.

        Returns:
            str: The access token.
        """
        url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
        response = requests.get(url).json()
        return response["accessToken"]

def releated_artist(artist_id):
    """
    Retrieves a list of related artists based on the provided artist ID.

    Args:
        artist_id (str): The ID of the artist to retrieve related artists for.

    Returns:
        list: A list of dictionaries containing information about the related artists. Each dictionary contains the following keys:
            - name (str): The name of the artist.
            - followers (int): The total number of followers the artist has.
            - genres (str): A comma-separated string of genres associated with the artist. If no genres are available, this value is None.
            - image (str): The URL of the artist's image.
            - external_url (str): The external URL of the artist on Spotify.

    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists?limit=50"
    similar_artists = []
    artists = requests.get(
            url, headers={"Authorization": f"Bearer {token()}"}
        ).json()['artists']
     
    for artist in artists:
          similar_artists.append({
               'name':artist['name'],
               'followers':artist['followers']['total'],
               'genres' : ",".join(artist.get('genres')) if artist.get('genres') else None,
               'image':artist['images'][0]['url'],
               'external_url':artist['external_urls']['spotify']
          })
    shuffle(similar_artists)
    return similar_artists[:5]

def get_recommendations(artist_id,energy,danceability,valence,loudness,acousticness,speechiness,instrumentalness):
     """
     Retrieves a list of recommended tracks from Spotify based on the specified parameters.

     Args:
          artist_id (str): The ID of the artist to use as a seed for recommendations.
          energy (float): The target energy level of the recommended tracks.
          danceability (float): The target danceability level of the recommended tracks.
          valence (float): The target valence level of the recommended tracks.
          loudness (float): The target loudness level of the recommended tracks.
          acousticness (float): The target acousticness level of the recommended tracks.
          speechiness (float): The target speechiness level of the recommended tracks.
          instrumentalness (float): The target instrumentalness level of the recommended tracks.

     Returns:
          List[Dict[str, Any]]: A list of dictionaries representing the recommended tracks.
               Each dictionary contains the following information for a track:
               - 'trackName' (str): The name of the track.
               - 'trackId' (str): The ID of the track.
               - 'artists' (str): The names of the artists associated with the track.
               - 'duration' (int): The duration of the track in milliseconds.
               - 'explicit' (str): Indicates whether the track contains explicit content.
               - 'albumName' (str): The name of the album the track belongs to.
               - 'albumImg' (str): The URL of the album cover image.
               - 'albumId' (str): The ID of the album the track belongs to.
               - 'releaseDate' (str): The release date of the album the track belongs to.
     """
     params = f"""?limit=50
     &seed_artists={artist_id}
     &target_energy={energy}
     &target_danceability={danceability}
     &target_valence={valence}
     &target_loudness={loudness}
     &target_acousticness={acousticness}
     &target_speechiness={speechiness}
     &target_instrumentalness={instrumentalness}
     """.replace("\n","").replace("     ","")

     url = f"https://api.spotify.com/v1/recommendations{params}"

     tracks = []

     response = requests.get(
            url, headers={"Authorization": f"Bearer {token()}"}
        ).json()
     #print(url)
     
     for track in response['tracks']:
          tracks.append(
               {
               "trackName":track['name'],
               "trackId":track['id'],
               "artists": ", ".join([x['name'] for x in track['artists']]),
               "duration" : track['duration_ms'],
               "explicit": "Explicit" if track['explicit'] else "Non Explicit",
               "albumName" : track['album']['name'],
               "albumImg":track['album']['images'][1]['url'],
               "albumId" : track['album']['id'],
               "releaseDate" : track['album']['release_date']
               }
          )
     shuffle(tracks)
     return tracks[:5]
     
     
def get_artist_meta(artist_id):
        """
        Retrieves the metadata of an artist based on their unique artist ID.

        Parameters:
            artist_id (str): The unique ID of the artist.

        Returns:
            dict: A dictionary containing the artist's metadata, including the artist ID,
            number of followers, image URL, popularity, and genres (if available).
        """
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        artist_data = {}
        artist_metas = requests.get(
            url, headers={"Authorization": f"Bearer {token()}"}
        ).json()
        
        artist_data["artistID"] = artist_id
        artist_data["followers"] = artist_metas["followers"]["total"]
        try:
            artist_data["img"] = artist_metas["images"][0]["url"]
        except:
            artist_data[
                "img"
            ] = "https://i.scdn.co/image/ab6761610000e5eb15d8e761586590f74af0dd37"
        artist_data["popularity"] = artist_metas["popularity"]
        try:
            artist_data["genres"] = ", ".join(artist_metas["genres"])
        except:
            artist_data["genres"] = None

        return artist_data