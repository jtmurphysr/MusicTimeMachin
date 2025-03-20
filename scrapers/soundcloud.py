from .base_scraper import BaseMusicScraper
from bs4 import BeautifulSoup
import requests

"""
SoundCloud Top EDM Scraper Module

This module provides functionality to scrape SoundCloud's current top EDM charts
and create Spotify playlists from the scraped tracks.

The SoundCloudEDMScraper class inherits from BaseMusicScraper and implements
the chart-specific scraping logic for SoundCloud's website. By default, it scrapes
the 'danceedm' genre, but can be configured for other genres available on SoundCloud.

Example usage:
    scraper = SoundCloudEDMScraper()  # Default is danceedm genre
    if scraper.scrape():
        playlist_url = scraper.create_playlist("Top EDM Tracks This Week")
        
    # Or with a different genre:
    techno_scraper = SoundCloudEDMScraper(genre="techno")
    if techno_scraper.scrape():
        playlist_url = techno_scraper.create_playlist("Top Techno Tracks")
"""

class SoundCloudEDMScraper(BaseMusicScraper):
    """
    Scraper for SoundCloud top EDM chart.
    
    This class is responsible for scraping the SoundCloud top EDM chart
    and creating a Spotify playlist with those songs.
    """
    
    def __init__(self, genre="danceedm"):
        """
        Initialize the SoundCloud scraper.
        
        Args:
            genre (str, optional): The genre to scrape. Defaults to "danceedm".
        """
        super().__init__()
        self.genre = genre
        self.base_url = "https://soundcloud.com/charts/top"
    
    def scrape(self):
        """
        Scrape the SoundCloud top EDM chart.
        
        Returns:
            bool: True if scraping was successful, False otherwise.
        """
        try:
            # Construct the URL for the specific genre
            url = f"{self.base_url}?genre={self.genre}"
            print(f"Fetching data from: {url}")
            
            # Make the request
            response = requests.get(url, headers=self.headers)
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all chart items based on the HTML structure
            chart_items = soup.select('li article')
            print(f"Found {len(chart_items)} tracks in the chart")
            
            if len(chart_items) == 0:
                # If no tracks found using the selector, save the HTML for debugging
                with open('soundcloud_debug.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                print("No tracks found. HTML saved to 'soundcloud_debug.html' for debugging.")
                return False
            
            # Extract track information
            self.tracks_data = []
            for item in chart_items:
                try:
                    # Extract title and artist based on the HTML structure
                    h2_element = item.select_one('h2[itemprop="name"]')
                    
                    if h2_element:
                        # Title is the text of the first <a> tag
                        title_element = h2_element.select_one('a[itemprop="url"]')
                        # Artist is the text of the second <a> tag
                        artist_element = h2_element.select_one('a:nth-of-type(2)')
                        
                        if title_element and artist_element:
                            title = title_element.text.strip()
                            artist = artist_element.text.strip()
                            self.tracks_data.append((title, artist))
                            print(f"Found track: {title} by {artist}")
                except Exception as e:
                    print(f"Error extracting track info: {e}")
            
            print(f"Successfully extracted data for {len(self.tracks_data)} tracks")
            
            # Save the data to a file for reference
            self.save_tracks_to_file(
                filename=f"soundcloud_{self.genre}_top.txt",
                title=f"SoundCloud {self.genre.capitalize()} Top Tracks"
            )
            
            return len(self.tracks_data) > 0
        
        except Exception as e:
            print(f"Error scraping SoundCloud: {e}")
            return False
    
    def create_playlist(self, playlist_name, limit=30):
        """
        Create a Spotify playlist with songs from the SoundCloud chart.
        
        Args:
            playlist_name (str): The name for the playlist.
            limit (int, optional): Maximum number of songs to add to the playlist. Defaults to 30.
            
        Returns:
            str or None: The URL of the created playlist if successful, None otherwise.
        """
        if not self.tracks_data:
            print("No tracks data available. Please run scrape() first.")
            return None
        
        # Search for each song on Spotify and collect URIs
        spotify_uris = []
        for i, (title, artist) in enumerate(self.tracks_data[:limit], 1):
            print(f"({i}/{limit}) Searching for: {title} - {artist}")
            uri = self.search_song(title, artist)
            if uri:
                spotify_uris.append(uri)
        
        print(f"Found {len(spotify_uris)} tracks on Spotify")
        
        # Create the playlist
        description = f"Top SoundCloud {self.genre.capitalize()} tracks"
        return self.make_playlist(spotify_uris, playlist_name, description) 