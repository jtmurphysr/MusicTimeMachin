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
       print("3. MyNewChart (describe what it offers)")
       
       while True:
           choice = input("\nEnter your choice (1, 2, or 3): ").strip()
           if choice == '1':
               return 'billboard'
           elif choice == '2':
               return 'soundcloud'
           elif choice == '3':
               return 'mynewchart'
           else:
               print("Invalid choice. Please enter 1, 2, or 3.")
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
           
           # Run the appropriate flow
           if chart_choice == 'billboard':
               run_billboard_flow()
           elif chart_choice == 'soundcloud':
               run_soundcloud_flow()
           elif chart_choice == 'mynewchart':
               run_mynewchart_flow()
           
           print("\nThank you for using Music Time Machine!")
       
       except KeyboardInterrupt:
           print("\n\nProgram interrupted by user. Exiting...")
           sys.exit(0)
       except Exception as e:
           print(f"\nAn error occurred: {e}")
           sys.exit(1)
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

## Example: Implementing an Apple Music Charts Scraper

Here's a hypothetical example of implementing an Apple Music Charts scraper:

```python
from .base_scraper import BaseMusicScraper
import requests
from bs4 import BeautifulSoup
import lxml

class AppleMusicChartScraper(BaseMusicScraper):
    """
    Scraper for Apple Music charts.
    
    This scraper extracts track data from Apple Music's charts.
    """
    
    def __init__(self):
        """Initialize the Apple Music scraper."""
        super().__init__()
        self.genre = "pop"  # Default genre
        self.base_url = "https://music.apple.com/us/playlist/top-100"
        self.tracks_data = []
        
    def scrape(self, genre=None):
        """
        Scrape Apple Music chart data.
        
        Args:
            genre (str, optional): Genre to scrape. Defaults to None (uses pop).
            
        Returns:
            bool: True if scraping was successful, False otherwise.
        """
        try:
            # Use the provided genre or the default
            self.genre = genre or self.genre
            
            # Construct the URL based on genre
            url = f"{self.base_url}-{self.genre}/pl.xxxxxxxxxxx"
            
            # Implementation would continue with HTTP request, parsing, etc.
            # ...
            
            return True
            
        except Exception as e:
            print(f"Error scraping Apple Music Chart: {e}")
            return False
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