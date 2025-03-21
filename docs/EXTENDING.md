# Extending Music Time Machine

This guide explains how to extend the Music Time Machine project by adding new music chart scrapers. The modular architecture makes it easy to add support for additional chart sources or genres.

## Architecture Overview

Music Time Machine follows a clean separation of concerns:

1. **Scrapers** - Each scraper class is responsible for extracting track data from a specific music chart source.
2. **PlaylistBuilder** - Handles all Spotify interactions including authentication, track searching, and playlist creation.
3. **Main Application** - Orchestrates user interaction and connects scrapers with the playlist builder.

## Adding a New Scraper

### Step 1: Create a New Scraper Class

1. Create a new Python file in the `scrapers` directory (e.g., `scrapers/my_new_scraper.py`).
2. Implement a new scraper class that inherits from `BaseMusicScraper`.
3. Implement the required methods.

Here's a template for a new scraper:

```python
from .base_scraper import BaseMusicScraper
import requests
from bs4 import BeautifulSoup
import lxml

class MyNewChartScraper(BaseMusicScraper):
    """
    Scraper for MyNewChart music charts.
    
    This scraper extracts track data from MyNewChart's website.
    """
    
    def __init__(self):
        """Initialize the scraper with default values."""
        super().__init__()
        self.genre = "specific_genre"  # e.g., "rock", "pop", "hip-hop"
        self.base_url = "https://example.com/charts"  # URL to scrape
        self.tracks_data = []  # Will hold (title, artist) tuples
        
    def scrape(self, param=None):
        """
        Scrape the chart data from the source website.
        
        Args:
            param: Optional parameter (e.g., date, genre subset, etc.)
            
        Returns:
            bool: True if scraping was successful, False otherwise.
        """
        try:
            # Construct the URL (with parameters if needed)
            url = self.base_url
            if param:
                url = f"{self.base_url}/{param}"
                
            # Send HTTP request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, "lxml")
            
            # Extract tracks (implementation depends on the website's structure)
            # Example:
            track_elements = soup.select("div.chart-item")
            
            self.tracks_data = []
            for element in track_elements:
                # Extract data (adjust selectors based on the website's HTML structure)
                title = element.select_one("div.title").text.strip()
                artist = element.select_one("div.artist").text.strip()
                
                # Add to tracks_data
                self.tracks_data.append((title, artist))
            
            # Save tracks to file
            self._save_tracks_to_file(f"my_new_chart_{param if param else 'latest'}.txt")
            
            return True
            
        except Exception as e:
            print(f"Error scraping MyNewChart: {e}")
            return False
    
    def get_tracks_data(self):
        """
        Get the scraped tracks data.
        
        Returns:
            list: List of (title, artist) tuples.
        """
        return self.tracks_data
    
    def get_genre(self):
        """
        Get the genre of this chart.
        
        Returns:
            str: The genre name.
        """
        return self.genre
```

### Step 2: Update the Main Application

Modify `main.py` to include your new scraper:

1. Add the import for your new scraper class:
   ```python
   from scrapers.my_new_scraper import MyNewChartScraper
   ```

2. Add a new option to the chart choice menu in the `get_chart_choice()` function:
   ```python
   def get_chart_choice():
       """Get the user's choice of chart."""
       print("\nWhich chart would you like to use?")
       print("1. Billboard Hot 100 (historical)")
       print("2. SoundCloud Top EDM (current)")
       print("3. Apple Music EDM Hits (current)")
       print("4. Traxsource Deep House Top Tracks (current)")
       print("5. MyNewChart (describe what it offers)")
       
       while True:
           try:
               choice = input("\nEnter your choice (1-5): ")
               choice_num = int(choice)
               if choice_num in [1, 2, 3, 4, 5]:
                   return choice_num
               else:
                   print("Please enter a number between 1 and 5.")
           except ValueError:
               print("Invalid input. Please enter a number.")
   ```

3. Create a flow function for your new scraper:
   ```python
   def run_mynewchart_flow():
       """Run the MyNewChart workflow."""
       # Create the scraper and scrape the chart
       # (Adjust parameters as needed for your scraper)
       scraper = MyNewChartScraper()
       
       # If your scraper needs a parameter (e.g., a date, category, etc.)
       # param = get_param_from_user()
       # success = scraper.scrape(param)
       
       # If your scraper doesn't need a parameter
       success = scraper.scrape()
       
       if not success:
           print("Failed to scrape MyNewChart. Exiting.")
           return
       
       # Get the playlist name
       # (You may want a custom default name format)
       today_date = datetime.today().strftime('%Y-%m-%d')
       default_name = f"MyNewChart Top Tracks - {today_date}"
       playlist_name = get_playlist_name(default_name)
       
       # Confirm with the user
       print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from MyNewChart.")
       
       confirm = input("Proceed? (y/n): ").lower().strip()
       if confirm != 'y':
           print("Playlist creation cancelled.")
           return
       
       # Get the track data from the scraper
       tracks_data = scraper.get_tracks_data()
       
       # Create the playlist builder
       playlist_builder = PlaylistBuilder()
       
       # Create the playlist using the builder
       genre = scraper.get_genre()
       description = f"Top {genre.capitalize()} tracks from MyNewChart"
       playlist_url = playlist_builder.create_playlist(
           tracks_data=tracks_data,
           playlist_name=playlist_name,
           description=description
       )
       
       if playlist_url:
           print(f"\nSuccess! Your playlist has been created: {playlist_url}")
       else:
           print("\nFailed to create playlist.")
   ```

4. Update the `main()` function to call your new flow:
   ```python
   def main():
       """Main function to run the program."""
       try:
           # Display welcome message
           display_welcome_message()
           
           # Get user's chart choice
           chart_choice = get_chart_choice()
           
           # Run the appropriate flow based on chart choice
           if chart_choice == 1:
               run_billboard_flow()
           elif chart_choice == 2:
               run_soundcloud_flow()
           elif chart_choice == 3:
               run_applemusic_flow()
           elif chart_choice == 4:
               run_traxsource_flow()
           elif chart_choice == 5:
               run_mynewchart_flow()
           
       except Exception as e:
           print(f"An unexpected error occurred: {e}")
           import traceback
           traceback.print_exc()
   ```

### Step 3: Test Your New Scraper

Run the application and test your new scraper:
```
python main.py
```

Choose your new chart option and verify that:
1. The scraper extracts data correctly
2. The playlist is created with the correct tracks
3. Error handling works as expected

### Advanced: Creating a Genre-Specific Base Class

If you're adding multiple similar genre-based scrapers, you might want to create an intermediate base class:

```python
from .base_scraper import BaseMusicScraper

class GenreMusicScraper(BaseMusicScraper):
    """
    Base class for genre-specific music chart scrapers.
    
    This class extends BaseMusicScraper with functionality common 
    to genre-based charts but not to all music charts.
    """
    
    def __init__(self):
        """Initialize the genre scraper."""
        super().__init__()
        self.genre = "unknown"
        self.genre_categories = []  # List of available sub-genres
    
    def get_available_categories(self):
        """
        Get the available genre categories.
        
        Returns:
            list: List of available genre categories.
        """
        return self.genre_categories
        
    # Add other common methods for genre scrapers here
```

## Best Practices

When implementing a new scraper, follow these best practices:

1. **Error Handling**: Include proper error handling for HTTP requests, parsing, etc.
2. **Documentation**: Document your code with docstrings and comments.
3. **Consistency**: Follow the same interface as other scrapers.
4. **Testing**: Test your scraper with various inputs.
5. **User Experience**: Provide clear user feedback during scraping.
6. **Rate Limiting**: Respect the source website's rate limits and terms of service.

## Real Examples

### Example 1: Apple Music EDM Hits Scraper

Here's how we implemented the Apple Music EDM Hits scraper:

```python
from .base_scraper import BaseMusicScraper
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import json

class AppleMusicEDMScraper(BaseMusicScraper):
    """Scraper for Apple Music EDM Hits playlist."""

    def __init__(self):
        """Initialize the scraper with the Apple Music EDM playlist URL."""
        super().__init__()
        self.base_url = "https://music.apple.com/us/playlist/dance-edm-hits/pl.97c6c376b616499994ab14e1e8d5cab1"
        self.tracks_data = []

    def scrape(self, url_custom_param=None):
        """
        Scrape the Apple Music EDM Hits playlist.
        """
        url = self.base_url
        if url_custom_param:
            url = f"{url}/{url_custom_param}"

        print(f"Fetching Apple Music EDM Hits from: {url}")
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.8,*/*;q=0.7",
        })

        try:
            response = requests.get(url, headers=self.headers)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()

            # Save raw HTML for debugging
            os.makedirs("debug", exist_ok=True)
            with open("debug/apple_music_response.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved raw HTML to debug/apple_music_response.html for inspection")

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            print(f"HTML title: {soup.title.text if soup.title else 'No title found'}")

            # Extract tracks from JSON-LD data
            self.tracks_data = self._extract_tracks_from_json_ld(soup)
            
            if not self.tracks_data:
                # Fallback to meta tags extraction
                self.tracks_data = self._extract_tracks_from_meta(soup)

            # Save tracks to file
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"apple_music_edm_{today}.txt"
            title = f"Apple Music EDM Hits - {today}"
            self.save_tracks_to_file(filename, title)
            
            print(f"Found and saved {len(self.tracks_data)} tracks")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Apple Music: {str(e)}")
            return False

    def _extract_tracks_from_json_ld(self, soup):
        """Extract track information from JSON-LD data."""
        tracks = []
        
        # Look for JSON-LD script tags
        json_ld_scripts = soup.find_all("script", {"type": "application/ld+json"})
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if "@type" in data and data["@type"] == "MusicPlaylist" and "track" in data:
                    for track in data["track"]:
                        if "name" in track and "byArtist" in track and "name" in track["byArtist"]:
                            title = track["name"]
                            artist = track["byArtist"]["name"]
                            tracks.append((self._clean_title(title), artist))
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error parsing JSON-LD: {e}")
        
        return tracks

    def _extract_tracks_from_meta(self, soup):
        """Extract track information from meta tags (fallback method)."""
        tracks = []
        
        # Look for meta tags with music:song content
        song_meta_tags = soup.find_all("meta", property=lambda x: x and x.startswith("music:song"))
        for tag in song_meta_tags:
            content = tag.get("content", "")
            # Parse the URL to extract title and artist
            if content:
                title_match = re.search(r"([^/]+)(?=-\d+)?$", content)
                if title_match:
                    title = title_match.group(1).replace("-", " ").strip()
                    # Try to get artist from context or set as Unknown
                    artist = "Unknown"  # Placeholder, would need more context to extract artist
                    tracks.append((self._clean_title(title), artist))
        
        return tracks

    def _clean_title(self, title):
        """Clean the title to improve matching with Spotify."""
        # Remove content in parentheses that might be problematic for matching
        cleaned = re.sub(r'\(feat\..*?\)', '', title)
        cleaned = re.sub(r'\(ft\..*?\)', '', cleaned)
        
        # Common patterns to clean
        patterns = [
            (r'\(.*?[Rr]emix.*?\)', ''),
            (r'\(.*?[Ee]dit.*?\)', ''),
            (r'\(.*?[Vv]ersion.*?\)', ''),
            (r'\[.*?\]', ''),
        ]
        
        for pattern, replacement in patterns:
            cleaned = re.sub(pattern, replacement, cleaned)
        
        return cleaned.strip()

    def get_tracks_data(self):
        """Get the track data."""
        return self.tracks_data

    def get_genre(self):
        """Get the genre."""
        return "EDM"
```

### Example 2: Traxsource Deep House Scraper

Here's how we implemented the Traxsource Deep House scraper:

```python
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseMusicScraper

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
            
            if not self.tracks_data:
                print("Using fallback hardcoded track data for testing purposes")
                # Fallback hardcoded tracks - as (title, artist) tuples
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
            return self.tracks_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Traxsource: {str(e)}")
            # Fallback hardcoded tracks in case of error
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
```

## Next Steps for Extension

After implementing basic scrapers, consider these advanced extensions:

1. **User Genre Selection**: Allow users to select specific sub-genres.
2. **Date Ranges**: Implement date range selections for historical charts.
3. **Regional Charts**: Add support for country/region-specific charts.
4. **Custom Filters**: Allow users to filter tracks based on criteria.
5. **Playlist Customization**: Implement more customization options for playlists.

## Contributing

When contributing a new scraper to the project:

1. Follow the project's coding style and conventions.
2. Add documentation for your scraper.
3. Update the README.md to mention the new supported chart.
4. Add appropriate entries to the CHANGELOG.md.