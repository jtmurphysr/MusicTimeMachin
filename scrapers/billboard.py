from .base_scraper import BaseMusicScraper
from bs4 import BeautifulSoup
import requests

"""
Billboard Hot 100 Scraper Module

This module provides functionality to scrape Billboard Hot 100 charts from any date.
The BillboardTop100Scraper class inherits from BaseMusicScraper and implements
the chart-specific scraping logic for Billboard's website.

Example usage:
    scraper = BillboardTop100Scraper()
    if scraper.scrape("2021-01-01"):
        tracks_data = scraper.get_tracks_data()
        # tracks_data can now be used with a PlaylistBuilder to create playlists
"""

class BillboardTop100Scraper(BaseMusicScraper):
    """
    Scraper for Billboard Hot 100 chart.
    
    This class is responsible for scraping the Billboard Hot 100 chart for a specific date.
    It retrieves and formats track data, which can then be used to create playlists.
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
    
    def get_chart_date(self):
        """
        Get the date used for the last scraping operation.
        This can be useful for generating appropriate descriptions.
        
        Returns:
            str: The date string that was used in the last scrape operation.
        """
        # This is a helper method specific to Billboard scraping
        # to help with playlist generation information
        return getattr(self, 'last_scrape_date', None) 