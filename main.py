from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from env_variables import EnvConfig

config = EnvConfig()

"""
Music Time Machine

This script creates a Spotify playlist with songs from the Billboard Hot 100 chart
for a specific date in the past. It scrapes the Billboard website for the chart data,
searches for those songs on Spotify, and creates a playlist with the found tracks.
"""

def find_top100(target_date):
    """
    Scrape the Billboard Hot 100 chart for a specific date and create a Spotify playlist.
    
    Args:
        target_date (str): The date to search for in format YYYY-MM-DD.
        
    Returns:
        None: Creates a Spotify playlist as a side effect.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    url = f"https://www.billboard.com/charts/hot-100/{target_date}"
    print(url)
    response = requests.get(url, headers=headers)

    with open('billboard.html', 'w') as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    chart_rows = soup.select('ul.o-chart-results-list-row')
    print(f"Found {len(chart_rows)} chart rows")

    songs_data = []
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

            songs_data.append((position, title, artist))

    # Print the results
    print(f"Extracted data for {len(songs_data)} songs")
    uris=[]

    for position, title, artist in songs_data[:30]:
        print(f"#{position}: {title} - {artist}")
        result = search_song(title, artist)
        if result is not None:
            uris.append(result)

        print("==============")
        print(f"uris: {len(uris)}")
        print("==============")
    make_playlist(uris)


def setup_spotify_client():
    """
    Set up and return an authenticated Spotify client.
    
    Returns:
        spotipy.Spotify: An authenticated Spotify client.
    """
    # We need additional scopes for modifying library and playlists
    scope = "user-library-read user-library-modify playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.spotify_client_id,
        client_secret=config.spotify_client_secret,
        redirect_uri=config.spotify_redirect_uri,
        scope=scope,
        open_browser=True))

    return sp


def search_song(title, artist):
    """
    Search for a song on Spotify and return its URI.
    
    Args:
        title (str): The title of the song.
        artist (str): The artist of the song.
        
    Returns:
        str or None: The Spotify URI of the song if found, None otherwise.
    """
    sp = setup_spotify_client()
    # Create search query
    query = f"track:{title}"
    if artist:
        query += f" artist:{artist}"

    # Perform search
    results = sp.search(q=query, type='track', limit=1)
    #Get uri - this is what spotify needs
    items = results.get('tracks', {}).get('items', [])
    if items:
        uri = items[0]['uri']
        return uri

    # Extract track information
    tracks = results['tracks']['items']

    if not tracks:
        print(f"No results found for {query}")
        return None
    else:
        print(f"Found {len(tracks)} results for {query}")
        for track in tracks:
            print(f"{track['name']} - {track['artists'][0]['name']}")


def make_playlist(songs):
    """
    Create a Spotify playlist with the given songs.
    
    Args:
        songs (list): A list of Spotify URIs for the songs to add to the playlist.
        
    Returns:
        None
    """
    sp = setup_spotify_client()
    playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True, description=f"25 of the Billboard Top 100 songs for {target_date}")
    print(f"Created playlist: {playlist['name']}")
    for i in range(0, len(songs), 100):
        sp.playlist_add_items(playlist_id=playlist['id'], items=songs[i:i+100])
        print(f"Added {len(songs[i:i+100])} songs to playlist")

if __name__ == "__main__":
    global target_date
    target_date = input("Which year do you want to travel to?  Use the format YYYY-MM-DD: ")
    playlist_name = input("What do you want to name your playlist? ")
    find_top100(target_date)