import anthropic
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from keys import ANTHROPIC_API_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

def get_api_key():
    if ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
        return ANTHROPIC_API_KEY
    else:
        api_key = input("Please enter your Anthropic API key: ")
        # Update the keys.py file with the new API key
        with open('keys.py', 'w') as f:
            f.write(f'ANTHROPIC_API_KEY = "{api_key}"\n')
        return api_key

def get_playlist_name(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        temperature=0.9,
        system="You are a creative playlist namer. Given a theme or mood, generate a catchy and creative name for a Spotify playlist. The name should be short, memorable, and reflect the theme. Provide only the name, without any additional text or explanation.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a creative name for a playlist with the theme: {prompt}"
                    }
                ]
            }
        ]
    )
    # Handle both string and list responses
    if isinstance(message.content, list):
        return ' '.join([block.text for block in message.content if hasattr(block, 'text')]).strip()
    else:
        return message.content.strip()

def get_ai_response(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4000,
        temperature=0.7,
        system="You are a music expert with extensive knowledge of songs across various genres and eras. Given a prompt, generate a list of EXACTLY 100 song suggestions for a Spotify playlist. Each suggestion MUST be in the format 'Artist - Song Title'. Aim for a diverse mix of songs that fit the theme or mood of the prompt. Do not include any additional text or explanations, just the numbered list of 100 songs.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return message.content

def format_playlist(response):
    # Check if response is a list and get the text content
    if isinstance(response, list):
        response = ' '.join([block.text for block in response if hasattr(block, 'text')])
    
    # Extract the song list using regex
    song_list = re.findall(r'\d+\.\s(.+?)\s-\s(.+?)(?=\n\d+\.|\Z)', response, re.DOTALL)
    
    return song_list

def create_spotify_playlist(playlist_name, songs, user_prompt):
    # Set up Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_REDIRECT_URI,
                                                   scope="playlist-modify-public user-read-private"))

    # Get the current user's ID
    user_id = sp.me()['id']

    # Create a new playlist
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=f"Generated playlist for the theme: {user_prompt}")

    # Search for songs and add them to the playlist
    track_ids = []
    for artist, title in songs:
        results = sp.search(q=f"track:{title} artist:{artist}", type="track", limit=1)
        if results['tracks']['items']:
            track_ids.append(results['tracks']['items'][0]['id'])

    # Add tracks to playlist in batches of 100
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(playlist['id'], track_ids[i:i+100])

    return playlist['external_urls']['spotify']

# Get API key
api_key = get_api_key()

# Get user input
user_prompt = input("Enter a theme or mood for your Spotify playlist: ")

# Get playlist name
playlist_name = get_playlist_name(user_prompt, api_key)
print(f"\nPlaylist Name: {playlist_name}\n")

# Get AI response for song list
try:
    response = get_ai_response(user_prompt, api_key)
    
    # Format the response
    song_list = format_playlist(response)
    
    print("AI-generated song list for your Spotify playlist:")
    for i, (artist, song) in enumerate(song_list, 1):
        print(f"{i:3d}. {artist.strip()} - {song.strip()}")
    
    print(f"\nTotal songs in the playlist: {len(song_list)}")

    # Create Spotify playlist
    playlist_url = create_spotify_playlist(playlist_name, song_list, user_prompt)
    print(f"\nSpotify playlist created! You can access it here: {playlist_url}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please check your API keys and internet connection.")