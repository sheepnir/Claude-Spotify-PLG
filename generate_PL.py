import anthropic
import os
import re
from keys import ANTHROPIC_API_KEY

def get_api_key():
    if ANTHROPIC_API_KEY != "your_api_key_here":
        return ANTHROPIC_API_KEY
    else:
        api_key = input("Please enter your Anthropic API key: ")
        # Update the keys.py file with the new API key
        with open('keys.py', 'w') as f:
            f.write(f'ANTHROPIC_API_KEY = "{api_key}"')
        return api_key

def get_ai_response(prompt, api_key):
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.7,
        system="You are a music expert with extensive knowledge of songs across various genres and eras. Given a prompt, generate a list of 100 song suggestions for a Spotify playlist. Each suggestion should be in the format 'Artist - Song Title'. Aim for a diverse mix of songs that fit the theme or mood of the prompt.",
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
    
    # Format the output
    formatted_output = "AI-generated song list for your Spotify playlist:\n\n"
    for i, (artist, song) in enumerate(song_list, 1):
        formatted_output += f"{i:3d}. {artist.strip()} - {song.strip()}\n"
    
    return formatted_output

# Get API key
api_key = get_api_key()

# Get user input
user_prompt = input("Enter a theme or mood for your Spotify playlist: ")

# Get AI response
try:
    response = get_ai_response(user_prompt, api_key)
    
    # Format and display the response
    formatted_playlist = format_playlist(response)
    print("\n" + formatted_playlist)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please check your API key and internet connection.")