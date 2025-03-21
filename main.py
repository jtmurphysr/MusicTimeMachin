from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from env_variables import EnvConfig
from scrapers.billboard import BillboardTop100Scraper
from scrapers.soundcloud import SoundCloudEDMScraper
from scrapers.AppleMusic_EDM import AppleMusicEDMScraper
from scrapers.traxsource_deep_house import TraxsourceDeepHouseScraper
from playlist_builder import PlaylistBuilder
import sys
from datetime import datetime

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
Version: 2.1.0
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
        int: The user's chart choice (1, 2, 3, or 4).
    """
    print("\nWhich chart would you like to use?")
    print("1. Billboard Hot 100 (historical)")
    print("2. SoundCloud Top EDM (current)")
    print("3. Apple Music EDM Hits (current)")
    print("4. Traxsource Deep House Top Tracks (current)")
    
    while True:
        try:
            choice = input("\nEnter your choice (1, 2, 3, or 4): ")
            choice_num = int(choice)
            if choice_num in [1, 2, 3, 4]:
                return choice_num
            else:
                print("Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

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
    
    # Get the track data from the scraper
    tracks_data = scraper.get_tracks_data()
    
    # Create the playlist builder
    playlist_builder = PlaylistBuilder()
    
    # Create the playlist using the builder
    description = f"Billboard Hot 100 songs for {target_date}"
    playlist_url = playlist_builder.create_playlist(
        tracks_data=tracks_data,
        playlist_name=playlist_name,
        description=description
    )
    
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
    today_date = datetime.today().strftime('%Y-%m-%d')
    default_name = f"SoundCloud Top EDM Tracks - {today_date}"
    playlist_name = get_playlist_name(default_name)
    
    # Confirm with the user
    print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from SoundCloud Top EDM chart.")
    
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
    description = f"Top SoundCloud {genre.capitalize()} tracks"
    playlist_url = playlist_builder.create_playlist(
        tracks_data=tracks_data,
        playlist_name=playlist_name,
        description=description
    )

    if playlist_url:
        print(f"\nSuccess! Your playlist has been created: {playlist_url}")
    else:
        print("\nFailed to create playlist.")

def run_applemusic_flow():
    """Run the Apple Music EDM Hits workflow."""
    # Create the scraper and scrape the chart
    scraper = AppleMusicEDMScraper()
    success = scraper.scrape()

    if not success:
        print("Failed to scrape Apple Music EDM Hits chart. Exiting.")
        return
    
    # Get the playlist name
    today_date = datetime.today().strftime('%Y-%m-%d')
    default_name = f"Apple Music EDM Hits - {today_date}"
    playlist_name = get_playlist_name(default_name)
    
    # Confirm with the user
    print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from Apple Music EDM Hits chart.")
    
    confirm = input("Proceed? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Playlist creation cancelled.")
        return
    
    # Get the track data from the scraper
    tracks_data = scraper.get_tracks_data()
    
    # Create the playlist builder
    playlist_builder = PlaylistBuilder()
    
    # Create the playlist using the builder
    description = f"Apple Music EDM Hits"
    playlist_url = playlist_builder.create_playlist(
        tracks_data=tracks_data,
        playlist_name=playlist_name,
        description=description
    )

    if playlist_url:
        print(f"\nSuccess! Your playlist has been created: {playlist_url}")
    else:
        print("\nFailed to create playlist.")

def run_traxsource_flow():
    """Run the Traxsource Deep House workflow."""
    # Create the scraper and scrape the chart
    scraper = TraxsourceDeepHouseScraper()
    tracks_data = scraper.scrape()
    
    if not tracks_data:
        print("Failed to scrape Traxsource Deep House chart. Exiting.")
        return
    
    # Get the playlist name
    today_date = datetime.today().strftime('%Y-%m-%d')
    default_name = f"Traxsource Deep House - {today_date}"
    playlist_name = get_playlist_name(default_name)
    
    # Confirm with the user
    print(f"\nReady to create Spotify playlist '{playlist_name}' with tracks from Traxsource Deep House top chart.")
    
    confirm = input("Proceed? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Playlist creation cancelled.")
        return
    
    # Get the track data from the scraper
    tracks_data = scraper.get_tracks_data()
    
    # Create the playlist builder
    playlist_builder = PlaylistBuilder()
    
    # Create the playlist using the builder
    description = f"Traxsource Deep House Top Tracks"
    playlist_url = playlist_builder.create_playlist(
        tracks_data=tracks_data,
        playlist_name=playlist_name,
        description=description
    )

    if playlist_url:
        print(f"\nSuccess! Your playlist has been created: {playlist_url}")
    else:
        print("\nFailed to create playlist.")

def main():
    """
    Main function to run the application flow.
    """
    # Configuration
    try:
        # Display welcome message
        display_welcome_message()
        
        # Get chart choice
        chart_choice = get_chart_choice()
        
        # Run appropriate flow based on chart choice
        if chart_choice == 1:
            run_billboard_flow()
        elif chart_choice == 2:
            run_soundcloud_flow()
        elif chart_choice == 3:
            run_applemusic_flow()
        elif chart_choice == 4:
            run_traxsource_flow()
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()