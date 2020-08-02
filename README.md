# Automate Youtube Spotify playlist sync

*Note: This code was made for my personal use.*

## Problem
I listen to music on both youtube and spotify from time to time. When I'm coding on my computer I listen music on Youtube and when I'm out and about I listen to my playlists on Spotify. At times I find new songs on Youtube and want to add it to my spotify playlist. I have to manually search the song in spotify and then save it to a particular playlist. Why not automate this?

## Solution
I created this project to help resolve this problem. All I have to do now is just save a song into one of my public playlists in youtube and the code will take care of the rest. What is the rest per say? Searching for the song and automatically adding it to my spotify playlist. This is only a one way sync (youtube -> spotify) as per my preference.No more manual work!

## Steps for Setup 

What do I need?
* A computer running python (I would recommend the latest version if possible)
* A Youtube API key
* A Spotify API Client ID and Client Secret
* Your Youtube and Spotify playlist IDs (This you can find by looking at the URL)

### Get Youtube api key and playlist ID
API key:
* Go to the following [link](https://console.developers.google.com/apis/credentials?) to setup/get your API keys which you will need to make requests. 
* Click on "Create credentials". 
* Copy the API Key on a notepad somewhere as you will need this later on.

playlist ID:
* Create a playlist under library if you haven't done so yet. 
* Once you have created it look at the URL. You will notice "&list=", everything after the equal sign is the playlist ID. Copy this for later use.


### Get Spotify api client information and Playlist ID
API client information: 
* The same as you did for youtube you will need to do for spotify. You can go to this [link](https://developer.spotify.com/dashboard/login) to sign into your spotify account and "Create an app". You will need to copy the Client ID and Client Secret to a notepad.

* You will also need to setup a Redirect URI link as part of your spotify app. This will be used for oauth or else it can't look up your spotify playlist 
* Click on "edit settings" on the dashboard screen. Under redirect URI I just put "http://localhost"

Playlist ID:
* Log into spotify on your web browser
* Create a new playlist or you can use an existing one
* In the url you will see "playlist/" 
* Everything after the forward slash is your actual playlist ID
* Copy the ID for later use


## Running the code

**How to setup your env variables**

To setup your env variables you will need to create a ".env" file in the root of this repository. The file needs to contain the following:

```
export YOUTUBE_API=your_info_here
export YOUTUBE_PLAYLIST='your_info_here'
export SPOTIPY_CLIENT_ID='your_info_here'
export SPOTIPY_CLIENT_SECRET='your_info_here'
export SPOTIPY_REDIRECT_URI='http://localhost'
export SPOTIFY_PLAYLIST=your_info_here
export SPOTIFY_USERNAME=your_info_here
```

On the terminal you are using to run this code. You will first need to load your env varibales. 

Run the following command: 
```
source .env
```

Next, you will run the main code. 
```
python main.py
```

Your web browser will open asking you to log into your spotify account and grant permissions for the program to be able to pull your playlist information. After, copy the whole URL and paste it into your terminal. Tada...the sync will happen between your youtube playlist and spotify playlist.
