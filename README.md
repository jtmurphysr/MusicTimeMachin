# Music Time Machine

A Python application that creates Spotify playlists from Billboard Hot 100 charts of any date in the past.

## Description

Music Time Machine allows you to travel back in time and create a Spotify playlist with songs from the Billboard Hot 100 chart for any specific date. The application:

1. Scrapes the Billboard Hot 100 chart for the specified date
2. Searches for each song on Spotify
3. Creates a new playlist in your Spotify account with the found songs

Perfect for reliving musical memories or discovering what was popular on a significant date in your life!

## Features

- Scrape Billboard Hot 100 charts from any date
- Automatic Spotify song matching
- Playlist creation with custom name
- Environment variable management for secure credential storage

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/MusicTimeMachine.git
   cd MusicTimeMachine
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your Spotify API credentials:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```

## Getting Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new application
4. Set the redirect URI to `http://localhost:8888/callback`
5. Copy the Client ID and Client Secret to your `.env` file

## Usage

Run the script:
```
python main.py
```

You will be prompted to:
1. Enter a date in the format YYYY-MM-DD (e.g., 1999-12-31)
2. Enter a name for your playlist

The script will then:
- Fetch the Billboard Hot 100 chart for that date
- Search for those songs on Spotify
- Create a new playlist in your Spotify account
- Add the found songs to the playlist

The first time you run the script, it will open a browser window for you to authorize the application with your Spotify account.

## Project Structure

- `main.py` - The main script that handles the Billboard scraping and Spotify playlist creation
- `env_variables.py` - A utility class for managing environment variables
- `.env` - Contains your Spotify API credentials (not included in the repository)
- `requirements.txt` - Lists the required Python packages
- `.gitignore` - Specifies files that should not be tracked by Git

## Dependencies

- beautifulsoup4 - For scraping the Billboard website
- lxml - XML parser for BeautifulSoup
- requests - For making HTTP requests
- spotipy - Python client for the Spotify Web API
- python-dotenv - For loading environment variables from .env file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Billboard](https://www.billboard.com/) for providing historical chart data
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for enabling playlist creation
- [Spotipy](https://spotipy.readthedocs.io/) for the excellent Python wrapper around the Spotify API 