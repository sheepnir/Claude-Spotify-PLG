# AI-Powered Spotify Playlist Generator

This Python script uses the Anthropic API to generate creative playlist names and song lists based on a given theme or mood, and then creates the playlist on your Spotify account.

## Prerequisites

- Python 3.7 or higher
- A Spotify account (Premium recommended for full API access)
- Anthropic API key
- Spotify Developer account and registered app

## Setup

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/spotify-playlist-generator.git
   cd spotify-playlist-generator
   ```

2. Install the required Python packages:

   ```
   pip install anthropic spotipy
   ```

3. Create a `keys.py` file in the project directory with the following content:

   ```python
   # Anthropic API Key
   ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

   # Spotify API Credentials
   SPOTIFY_CLIENT_ID = "your_spotify_client_id_here"
   SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret_here"
   SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
   ```

4. Set up your Spotify Developer account and app:

   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new app
   - Get your Client ID and Client Secret
   - Add `http://localhost:8888/callback` as a Redirect URI in your app settings

5. Replace the placeholder values in `keys.py` with your actual API keys and credentials.

## Usage

1. Run the script:

   ```
   python generate_playlist.py
   ```

2. When prompted, enter a theme or mood for your playlist.

3. The script will:

   - Generate a creative playlist name
   - Create a list of 100 songs fitting the theme
   - Create a new public playlist on your Spotify account
   - Add the generated songs to the playlist

4. The first time you run the script, it will open a web browser for you to log in to your Spotify account and authorize the app.

5. Once complete, the script will provide a URL to your new Spotify playlist.

## Note

- Keep your `keys.py` file secure and never share it publicly.
- The script searches for each song on Spotify and adds the first match it finds. Sometimes, it might not find an exact match for every song.
- Due to API limitations, it might take a while to create the playlist, especially if many songs need to be searched.
- Make sure you're using a Spotify Premium account for full API functionality.

## Troubleshooting

If you encounter any issues:

- Ensure all API keys and credentials in `keys.py` are correct.
- Check your internet connection.
- Verify that you've authorized the app in your Spotify account.

For any other problems, please open an issue in this repository.

## License

[MIT License](LICENSE)
