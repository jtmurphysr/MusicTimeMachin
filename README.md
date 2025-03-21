# Music Time Machine

A Python application that creates Spotify playlists from popular music charts including Billboard Hot 100, SoundCloud Top EDM, Apple Music EDM Hits, and Traxsource Deep House.

## Description

Music Time Machine allows you to create Spotify playlists based on various music charts. You can:

1. Travel back in time with Billboard Hot 100 charts from any date in the past
2. Discover current trending EDM tracks from SoundCloud's Top Charts
3. Get the latest EDM hits from Apple Music
4. Find deep house gems from Traxsource's top Deep House tracks

The application scrapes the selected chart, searches for each song on Spotify, and creates a new playlist in your Spotify account with the found tracks.

Perfect for reliving musical memories or discovering what's trending now!

## Features

- Choose between multiple chart sources:
  - Billboard Hot 100 (historical)
  - SoundCloud Top EDM (current)
  - Apple Music EDM Hits (current)
  - Traxsource Deep House Top Tracks (current)
- Billboard: Scrape Hot 100 charts from any date in the past
- SoundCloud, Apple Music, and Traxsource: Get current top tracks
- Automatic Spotify song matching
- Playlist creation with custom name
- Default playlist names include relevant dates
- Saves track lists to text files for reference
- Clean object-oriented design with separation of concerns:
  - Scrapers focus solely on data extraction
  - PlaylistBuilder handles all Spotify interactions
- Modular architecture for easy extension with new chart sources
- Environment variable management for secure credential storage

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/MusicTimeMachine.git
   cd MusicTimeMachine
   ```

2. Create a virtual environment and install the required dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your Spotify API credentials:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
   ```

## Getting Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new application
4. Set the redirect URI to `http://127.0.0.1:8888/callback`
5. Copy the Client ID and Client Secret to your `.env` file

## Usage

Run the script:
```
python main.py
```

You will be guided through the following steps:

1. Choose a chart source:
   - Billboard Hot 100 (historical charts)
   - SoundCloud Top EDM (current chart)
   - Apple Music EDM Hits (current chart)
   - Traxsource Deep House Top Tracks (current chart)

2. For Billboard, enter a date in the format YYYY-MM-DD (e.g., 1999-12-31)

3. Enter a name for your playlist or accept the default name:
   - For Billboard: "Billboard Hot 100 - {selected_date}"
   - For SoundCloud: "SoundCloud Top EDM Tracks - {today's_date}"
   - For Apple Music: "Apple Music EDM Hits - {today's_date}"
   - For Traxsource: "Traxsource Deep House - {today's_date}"

4. Confirm playlist creation

The script will then:
- Fetch the selected chart
- Search for those songs on Spotify
- Create a new playlist in your Spotify account
- Add the found songs to the playlist
- Provide you with a link to the created playlist

The first time you run the script, it will open a browser window for you to authorize the application with your Spotify account.

## Project Structure

- `main.py` - The main script that handles user interaction and runs the workflows
- `scrapers/` - Package containing all chart scrapers
  - `__init__.py` - Package initialization file
  - `base_scraper.py` - Abstract base class defining the scraper interface
  - `billboard.py` - Implementation of Billboard Hot 100 scraper
  - `soundcloud.py` - Implementation of SoundCloud Top EDM scraper
  - `AppleMusic_EDM.py` - Implementation of Apple Music EDM Hits scraper
  - `traxsource_deep_house.py` - Implementation of Traxsource Deep House scraper
- `playlist_builder.py` - Module that handles all Spotify interactions and playlist creation
- `env_variables.py` - A utility class for managing environment variables
- `.env` - Contains your Spotify API credentials (not included in the repository)
- `requirements.txt` - Lists the required Python packages
- `.gitignore` - Specifies files that should not be tracked by Git
- `CHANGELOG.md` - Tracks changes between versions
- `docs/` - Documentation directory
  - `EXTENDING.md` - Guide for adding new chart scrapers to the project

## Dependencies

- beautifulsoup4 - For scraping music chart websites
- lxml - XML parser for BeautifulSoup
- requests - For making HTTP requests
- spotipy - Python client for the Spotify Web API
- python-dotenv - For loading environment variables from .env file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Billboard](https://www.billboard.com/) for providing historical chart data
- [SoundCloud](https://soundcloud.com/) for providing current EDM chart data
- [Apple Music](https://www.apple.com/apple-music/) for providing current EDM hits data
- [Traxsource](https://www.traxsource.com/) for providing Deep House chart data
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for enabling playlist creation
- [Spotipy](https://spotipy.readthedocs.io/) for the excellent Python wrapper around the Spotify API

## Extending the Project

Want to add support for a new music chart or genre? Check out the [Extending Guide](docs/EXTENDING.md) for detailed instructions on implementing new scrapers and integrating them into the application. 