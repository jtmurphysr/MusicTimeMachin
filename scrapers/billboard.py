from .base_scraper import BaseMusicScraper
from bs4 import BeautifulSoup
import requests

"""
Billboard Hot 100 Scraper Module

This module provides functionality to scrape Billboard Hot 100 charts from any date
and create Spotify playlists from the scraped tracks.

The BillboardTop100Scraper class inherits from BaseMusicScraper and implements
the chart-specific scraping logic for Billboard's website.

Example usage:
    scraper = BillboardTop100Scraper()
    if scraper.scrape("2021-01-01"):
        playlist_url = scraper.create_playlist("New Year 2021 Hits", "2021-01-01")
"""

class BillboardTop100Scraper(BaseMusicScraper):
    """
    Scraper for Billboard Hot 100 chart.
    
    This class is responsible for scraping the Billboard Hot 100 chart for a specific date
    and creating a Spotify playlist with those songs.
    """
    
    def __init__(self):
        """Initialize the Billboard scraper."""
        super().__init__()
        self.base_url = "https://www.billboard.com/charts/hot-100"
    
    def scrape(self, target_date):
        """
        Scrape the Billboard Hot 100 chart for a specific date.
        
        Args:
            target_date (str): The date to search for in format YYYY-MM-DD.
            
        Returns:
            bool: True if scraping was successful, False otherwise.
        """
        try:
            # Construct the URL for the specific date
            url = f"{self.base_url}/{target_date}"
            print(f"Fetching data from: {url}")
            
            # Make the request
            response = requests.get(url, headers=self.headers)
            
            # Save the HTML for debugging if needed
            with open('billboard_debug.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all chart rows
            chart_rows = soup.select('ul.o-chart-results-list-row')
            print(f"Found {len(chart_rows)} chart rows")
            
            if not chart_rows:
                print("No chart rows found. The Billboard Hot 100 page structure might have changed.")
                return False
            
            # Extract song information
            self.tracks_data = []
            for row in chart_rows:
                # Find the title within this row
                title_element = row.select_one('h3.c-title')
                # Find the artist within this row
                artist_element = row.select_one('span.c-label.a-no-trucate')
                
                if title_element and artist_element:
                    title = title_element.text.strip()
                    artist = artist_element.text.strip()
                    
                    # Also extract the chart position if available
                    position_element = row.select_one('span.c-label.a-font-primary-bold-l')
                    position = position_element.text.strip() if position_element else "N/A"
                    
                    self.tracks_data.append((position, title, artist))
            
            # Print the results
            print(f"Extracted data for {len(self.tracks_data)} songs")
            
            # Save the data to a file for reference
            self.save_tracks_to_file(
                filename=f"billboard_hot100_{target_date}.txt",
                title=f"Billboard Hot 100 Songs for {target_date}"
            )
            
            return len(self.tracks_data) > 0
        
        except Exception as e:
            print(f"Error scraping Billboard Hot 100: {e}")
            return False
    
    def create_playlist(self, playlist_name, target_date, limit=30):
        """
        Create a Spotify playlist with songs from the Billboard Hot 100.
        
        Args:
            playlist_name (str): The name for the playlist.
            target_date (str): The date used for scraping in format YYYY-MM-DD.
            limit (int, optional): Maximum number of songs to add to the playlist. Defaults to 30.
            
        Returns:
            str or None: The URL of the created playlist if successful, None otherwise.
        """
        if not self.tracks_data:
            print("No tracks data available. Please run scrape() first.")
            return None
        
        # Search for each song on Spotify and collect URIs
        spotify_uris = []
        for i, (position, title, artist) in enumerate(self.tracks_data[:limit], 1):
            print(f"({i}/{limit}) Searching for: #{position}: {title} - {artist}")
            uri = self.search_song(title, artist)
            if uri:
                spotify_uris.append(uri)
        
        print(f"Found {len(spotify_uris)} tracks on Spotify")
        
        # Create the playlist
        description = f"Billboard Hot 100 songs for {target_date}"
        return self.make_playlist(spotify_uris, playlist_name, description) 