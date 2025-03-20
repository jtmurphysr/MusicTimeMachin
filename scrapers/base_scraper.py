import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from env_variables import EnvConfig

"""
Base Scraper Module

This module defines the BaseMusicScraper abstract base class, which serves as the
foundation for all chart scrapers in the Music Time Machine application.

The base class handles common functionality like:
- Spotify authentication and API interaction
- Track searching and playlist creation
- Error handling and user feedback
- Track data storage and file output

By inheriting from this base class, new scrapers can focus solely on the
chart-specific scraping logic while reusing common infrastructure.
"""

class BaseMusicScraper(ABC):
    """
    Base class for music chart scrapers.
    
    This abstract class defines the common interface and functionality for all music scrapers.
    Specific scrapers like Billboard and SoundCloud should inherit from this class.
    """
    
    def __init__(self):
        """Initialize the base scraper with common attributes."""
        self.config = EnvConfig()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.tracks_data = []
    
    def setup_spotify_client(self):
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
        sp = self.setup_spotify_client()
        if not sp:
            return None
            
        try:
            # Create search query
            query = f"track:{title}"
            if artist:
                query += f" artist:{artist}"

            # Perform search
            results = sp.search(q=query, type='track', limit=1)
            
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
    
    def make_playlist(self, songs, playlist_name, description):
        """
        Create a Spotify playlist with the given songs.
        
        Args:
            songs (list): A list of Spotify URIs for the songs to add to the playlist.
            playlist_name (str): The name for the playlist.
            description (str): Description for the playlist.
            
        Returns:
            None
        """
        if not songs:
            print("No songs found to add to playlist.")
            return
            
        sp = self.setup_spotify_client()
        if not sp:
            return
            
        try:
            playlist = sp.user_playlist_create(
                user=sp.me()['id'], 
                name=playlist_name, 
                public=True, 
                description=description
            )
            print(f"Created playlist: {playlist['name']}")
            
            for i in range(0, len(songs), 100):
                sp.playlist_add_items(playlist_id=playlist['id'], items=songs[i:i+100])
                print(f"Added {len(songs[i:i+100])} songs to playlist")
            
            return playlist['external_urls']['spotify']  # Return the Spotify URL to the playlist
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None
    
    @abstractmethod
    def scrape(self, *args, **kwargs):
        """
        Scrape music chart data from the source.
        
        This method must be implemented by all concrete scraper classes.
        """
        pass
    
    @abstractmethod
    def create_playlist(self, playlist_name, *args, **kwargs):
        """
        Create a Spotify playlist with the scraped tracks.
        
        This method must be implemented by all concrete scraper classes.
        
        Args:
            playlist_name (str): The name for the playlist.
        """
        pass
    
    def save_tracks_to_file(self, filename, title):
        """
        Save the scraped track information to a text file.
        
        Args:
            filename (str): The name of the file to save to.
            title (str): The title for the list of tracks.
        """
        if not self.tracks_data:
            print("No tracks to save.")
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n\n")
                for i, track_info in enumerate(self.tracks_data, 1):
                    if len(track_info) == 3:  # Billboard format (position, title, artist)
                        position, title, artist = track_info
                        f.write(f"{i}. #{position}: {title} - {artist}\n")
                    elif len(track_info) == 2:  # SoundCloud format (title, artist)
                        title, artist = track_info
                        f.write(f"{i}. {title} - {artist}\n")
            
            print(f"Track information saved to {filename}")
        except Exception as e:
            print(f"Error saving tracks to file: {e}") 