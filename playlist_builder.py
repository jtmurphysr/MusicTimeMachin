import spotipy
from spotipy.oauth2 import SpotifyOAuth
from env_variables import EnvConfig

"""
Playlist Builder Module

This module contains the PlaylistBuilder class, which is responsible for 
creating Spotify playlists from track data regardless of the source.

By separating playlist creation from data scraping, we maintain a cleaner
separation of concerns and make the system more maintainable and extensible.
"""

class PlaylistBuilder:
    """
    Class responsible for creating Spotify playlists from track data.
    
    This class handles Spotify authentication, track searching, and playlist creation,
    allowing scraper classes to focus solely on data extraction.
    """
    
    def __init__(self):
        """Initialize the PlaylistBuilder with Spotify authentication."""
        self.config = EnvConfig()
        self.spotify_client = self._setup_spotify_client()

    def _setup_spotify_client(self):
        """
        Set up and return an authenticated Spotify client.
        
        Returns:
            spotipy.Spotify: An authenticated Spotify client.
        """
        try:
            # We need additional scopes for modifying library and playlists
            scope = "user-library-read user-library-modify playlist-modify-public"

            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.config.spotify_client_id,
                client_secret=self.config.spotify_client_secret,
                redirect_uri=self.config.spotify_redirect_uri,
                scope=scope,
                open_browser=True))

            return sp
        except Exception as e:
            print(f"Error setting up Spotify client: {e}")
            print("Please check your Spotify credentials in your .env file.")
            return None
    
    def search_song(self, title, artist):
        """
        Search for a song on Spotify and return its URI.
        
        Args:
            title (str): The title of the song.
            artist (str): The artist of the song.
            
        Returns:
            str or None: The Spotify URI of the song if found, None otherwise.
        """
        if not self.spotify_client:
            return None
            
        try:
            # Create search query
            query = f"track:{title}"
            if artist:
                query += f" artist:{artist}"

            # Perform search
            results = self.spotify_client.search(q=query, type='track', limit=1)
            
            # Get uri - this is what spotify needs
            items = results.get('tracks', {}).get('items', [])
            if items:
                uri = items[0]['uri']
                print(f"Found: {items[0]['name']} - {items[0]['artists'][0]['name']}")
                return uri
            
            print(f"No results found for {query}")
            return None
        except Exception as e:
            print(f"Error searching for song: {e}")
            return None
    
    def create_playlist(self, tracks_data, playlist_name, description, limit=30):
        """
        Create a Spotify playlist with the given tracks.
        
        Args:
            tracks_data (list): A list of tuples containing track info (title, artist) or (position, title, artist)
            playlist_name (str): The name for the playlist.
            description (str): Description for the playlist.
            limit (int, optional): Maximum number of songs to add. Defaults to 30.
            
        Returns:
            str or None: The URL of the created playlist if successful, None otherwise.
        """
        if not tracks_data:
            print("No tracks data available to create a playlist.")
            return None
            
        if not self.spotify_client:
            return None
        
        # Search for each song on Spotify and collect URIs
        spotify_uris = []
        for i, track_info in enumerate(tracks_data[:limit], 1):
            # Handle different formats of track_info
            if len(track_info) == 3:  # (position, title, artist)
                position, title, artist = track_info
                print(f"({i}/{limit}) Searching for: #{position}: {title} - {artist}")
            else:  # (title, artist)
                title, artist = track_info
                print(f"({i}/{limit}) Searching for: {title} - {artist}")
                
            uri = self.search_song(title, artist)
            if uri:
                spotify_uris.append(uri)
        
        print(f"Found {len(spotify_uris)} tracks on Spotify")
        
        # Create the playlist
        if not spotify_uris:
            print("No songs found to add to playlist.")
            return None
            
        try:
            playlist = self.spotify_client.user_playlist_create(
                user=self.spotify_client.me()['id'], 
                name=playlist_name, 
                public=True, 
                description=description
            )
            print(f"Created playlist: {playlist['name']}")
            
            for i in range(0, len(spotify_uris), 100):
                self.spotify_client.playlist_add_items(playlist_id=playlist['id'], items=spotify_uris[i:i+100])
                print(f"Added {len(spotify_uris[i:i+100])} songs to playlist")
            
            return playlist['external_urls']['spotify']  # Return the Spotify URL to the playlist
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None 