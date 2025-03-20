from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from env_variables import EnvConfig
from scrapers.billboard import BillboardTop100Scraper
from scrapers.soundcloud import SoundCloudEDMScraper
import sys

config = EnvConfig()

"""
Music Time Machine

A Python application that creates Spotify playlists from popular music charts.
Users can choose between Billboard Hot 100 charts from any date in the past
or current SoundCloud Top EDM tracks.

The application provides a simple interactive command-line interface that guides
users through the process of selecting a chart source, specifying parameters,
and creating a Spotify playlist.

This script serves as the entry point to the application and orchestrates the 
workflow between user input and the chart scrapers.

Usage:
    python main.py

Author: John Murphy
Version: 2.0.0
"""

def display_welcome_message():
    """Display a welcome message with ASCII art."""
    welcome_message = """
    ╔╦╗╦ ╦╔═╗╦╔═╗  ╔╦╗╦╔╦╗╔═╗  ╔╦╗╔═╗╔═╗╦ ╦╦╔╗╔╔═╗
     ║ ║ ║╚═╗║║     ║ ║║║║║╣    ║ ╠═╣║  ╠═╣║║║║║╣ 
     ╩ ╚═╝╚═╝╩╚═╝   ╩ ╩╩ ╩╚═╝   ╩ ╩ ╩╚═╝╩ ╩╩╝╚╝╚═╝
                                                    
    Create Spotify playlists from music charts!
    """
    print(welcome_message)

def get_chart_choice():
    """
    Get the user's choice of chart.
    
    Returns:
        str: The user's choice - 'billboard' or 'soundcloud'.
    """
    print("\nWhich chart would you like to use?")
    print("1. Billboard Hot 100 (historical)")
    print("2. SoundCloud Top EDM (current)")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice == '1':
            return 'billboard'
        elif choice == '2':
            return 'soundcloud'
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_billboard_date():
    """
    Get the date for Billboard Hot 100 chart.
    
    Returns:
        str: The date in YYYY-MM-DD format.
    """
    while True:
        date_input = input("\nWhich date do you want to travel to? Use the format YYYY-MM-DD: ").strip()
        # Simple validation - could be enhanced
        if len(date_input.split('-')) == 3 and len(date_input) == 10:
            return date_input
        else:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2000-01-01).")

def get_playlist_name(default_name):
    """
    Get the playlist name from the user.
    
    Args:
        default_name (str): The default name to use if the user doesn't provide one.
        
    Returns:
        str: The playlist name.
    """
    name_input = input(f"\nWhat do you want to name your playlist? (default: {default_name}): ").strip()
    return name_input if name_input else default_name

def run_billboard_flow():
    """Run the Billboard Hot 100 workflow."""
    # Get the date
    target_date = get_billboard_date()
    
    # Create the scraper and scrape the chart
    scraper = BillboardTop100Scraper()
    success = scraper.scrape(target_date)
    
    if not success:
        print("Failed to scrape Billboard Hot 100 chart. Exiting.")
        return
    
    # Get the playlist name
    default_name = f"Billboard Hot 100 - {target_date}"
    playlist_name = get_playlist_name(default_name)
    
    # Confirm with the user
    print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from Billboard Hot 100 for {target_date}.")
    
    confirm = input("Proceed? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Playlist creation cancelled.")
        return
    
    # Create the playlist
    playlist_url = scraper.create_playlist(playlist_name, target_date)
    
    if playlist_url:
        print(f"\nSuccess! Your playlist has been created: {playlist_url}")
    else:
        print("\nFailed to create playlist.")

def run_soundcloud_flow():
    """Run the SoundCloud EDM workflow."""
    # Create the scraper and scrape the chart
    scraper = SoundCloudEDMScraper()
    success = scraper.scrape()
    
    if not success:
        print("Failed to scrape SoundCloud EDM chart. Exiting.")
        return
    
    # Get the playlist name
    default_name = "SoundCloud Top EDM Tracks"
    playlist_name = get_playlist_name(default_name)
    
    # Confirm with the user
    print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from SoundCloud Top EDM chart.")
    
    confirm = input("Proceed? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Playlist creation cancelled.")
        return
    
    # Create the playlist
    playlist_url = scraper.create_playlist(playlist_name)
    
    if playlist_url:
        print(f"\nSuccess! Your playlist has been created: {playlist_url}")
    else:
        print("\nFailed to create playlist.")

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
        else:  # soundcloud
            run_soundcloud_flow()
        
        print("\nThank you for using Music Time Machine!")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()