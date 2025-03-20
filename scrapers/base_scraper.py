import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from env_variables import EnvConfig

"""
Base Scraper Module

This module defines the BaseMusicScraper abstract base class, which serves as the
foundation for all chart scrapers in the Music Time Machine application.

The base class handles common functionality like:
- Web request handling
- Error handling and user feedback
- Track data storage and file output

This class focuses exclusively on data extraction, with playlist creation
now being handled by the separate PlaylistBuilder class.
"""

class BaseMusicScraper(ABC):
    """
    Base class for music chart scrapers.
    
    This abstract class defines the common interface and functionality for all music scrapers.
    Specific scrapers like Billboard and SoundCloud should inherit from this class.
    
    The scraper's primary responsibility is to retrieve and process music chart data.
    Playlist creation is handled by the separate PlaylistBuilder class.
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
    
    @abstractmethod
    def scrape(self, *args, **kwargs):
        """
        Scrape music chart data from the source.
        
        This method must be implemented by all concrete scraper classes.
        It should populate the self.tracks_data attribute with the scraped track information.
        
        Returns:
            bool: True if scraping was successful, False otherwise.
        """
        pass
    
    def get_tracks_data(self):
        """
        Get the scraped tracks data.
        
        Returns:
            list: The list of track data tuples.
        """
        return self.tracks_data
    
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