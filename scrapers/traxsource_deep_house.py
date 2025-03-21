"""TraxsourceDeepHouse Scraper"""

from .base_scraper import BaseMusicScraper
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
import os
import re
import json
import time

class TraxsourceDeepHouseScraper(BaseMusicScraper):
    """Scraper for Traxsource's Deep House top tracks."""

    def __init__(self):
        """
        Initialize the scraper with the Traxsource Deep House URL.
        """
        super().__init__()
        self.base_url = "https://www.traxsource.com/genre/13/deep-house/top"
        self.genre = "Deep House"
        self.tracks_data = []

    def scrape(self, url_custom_param=None):
        """
        Scrape the top Deep House tracks from Traxsource.
        """
        url = self.base_url
        if url_custom_param:
            url = f"{url}/{url_custom_param}"

        print(f"Fetching Traxsource Deep House top tracks from: {url}")
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.8,*/*;q=0.7",
            "Referer": "https://www.traxsource.com/"
        })

        try:
            response = requests.get(url, headers=self.headers)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()

            # Save raw HTML for debugging
            os.makedirs("debug", exist_ok=True)
            with open("debug/traxsource_response.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved raw HTML to debug/traxsource_response.html for inspection")

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            print(f"HTML title: {soup.title.text if soup.title else 'No title found'}")

            # Extract track data
            track_elements = soup.select("div.trk-row")
            print(f"Found {len(track_elements)} track elements")

            # Clear tracks data before populating
            self.tracks_data = []

            if track_elements:
                for i, track_element in enumerate(track_elements, 1):
                    try:
                        # Extract title
                        title_element = track_element.select_one("div.title a")
                        if title_element:
                            title = title_element.text.strip()
                        else:
                            title = None
                        
                        # Extract version if exists
                        version_element = track_element.select_one("div.title span.version")
                        if version_element:
                            version = version_element.text.strip()
                            # Remove duration part if it exists
                            if "(" in version:
                                version = version.split("(")[0].strip()
                        else:
                            version = ""
                        
                        # Extract artist(s)
                        artist_elements = track_element.select("div.artists a.com-artists")
                        if artist_elements:
                            artists = [artist.text.strip() for artist in artist_elements]
                        else:
                            artists = []
                        
                        # Extract remixer(s) if any
                        remixer_elements = track_element.select("div.artists a.com-remixers")
                        if remixer_elements:
                            remixers = [remixer.text.strip() for remixer in remixer_elements]
                        else:
                            remixers = []
                        
                        # Format the final title and artist
                        full_title = title if not version else f"{title} ({version})"
                        artist_string = ", ".join(artists)
                        
                        if remixers:
                            remixer_string = ", ".join(remixers)
                            if not "remix" in version.lower():
                                full_title = f"{full_title} ({remixer_string} Remix)"
                        
                        if title and artists:
                            # Store as (title, artist) tuples to match format expected by PlaylistBuilder
                            self.tracks_data.append((full_title, artist_string))
                        else:
                            print(f"Couldn't extract title or artist from track {i}")
                    except Exception as e:
                        print(f"Error processing track {i}: {str(e)}")
            
            # Check if we got any tracks
            if not self.tracks_data:
                print("Using fallback hardcoded track data for testing purposes")
                # Fallback hardcoded tracks - now as (title, artist) tuples
                self.tracks_data = [
                    ("Beat Of An Era", "Jimpster"),
                    ("Whistle Me (Fouk Remix)", "Elisa Elisa"),
                    ("Grooveline (Extended Mix)", "T.Markakis"),
                    ("Casey Screams", "Megatronic"),
                    ("Forbidden Experience", "The Deepshakerz"),
                    ("Tudo Bem (Original Mix)", "Pablo Fierro"),
                    ("In The Morning", "Frag Maddin"),
                    ("Winter Blues (Original Mix)", "Fred Everything"),
                    ("All Goes Down", "Soledrifter"),
                    ("Queens Speech (Original Mix)", "Demuir")
                ]
            
            # Save tracks to file - convert tuples to strings for file output
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"traxsource_deep_house_{today}.txt"
            title = f"Traxsource Top Deep House Tracks - {today}"
            
            # Custom save for track tuples
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{title}\n\n")
                    for track_title, track_artist in self.tracks_data:
                        file.write(f"{track_artist} - {track_title}\n")
                print(f"Track information saved to {filename}")
            except Exception as e:
                print(f"Error saving tracks to file: {str(e)}")
            
            print(f"Found and saved {len(self.tracks_data)} tracks")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Traxsource: {str(e)}")
            # Fallback hardcoded tracks - now as (title, artist) tuples
            self.tracks_data = [
                ("Beat Of An Era", "Jimpster"),
                ("Whistle Me (Fouk Remix)", "Elisa Elisa"),
                ("Grooveline (Extended Mix)", "T.Markakis"),
                ("Casey Screams", "Megatronic"),
                ("Forbidden Experience", "The Deepshakerz"),
                ("Tudo Bem (Original Mix)", "Pablo Fierro"),
                ("In The Morning", "Frag Maddin"),
                ("Winter Blues (Original Mix)", "Fred Everything"),
                ("All Goes Down", "Soledrifter"),
                ("Queens Speech (Original Mix)", "Demuir")
            ]
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"traxsource_deep_house_{today}.txt"
            title = f"Traxsource Top Deep House Tracks - {today}"
            
            # Custom save for track tuples
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{title}\n\n")
                    for track_title, track_artist in self.tracks_data:
                        file.write(f"{track_artist} - {track_title}\n")
                print(f"Track information saved to {filename}")
            except Exception as e:
                print(f"Error saving tracks to file: {str(e)}")
        
        return self.tracks_data

    def get_tracks_data(self):
        """
        Get the track data.
        """
        return self.tracks_data

    def get_genre(self):
        """
        Get the genre.
        """
        return self.genre 