import os
import json
# allows to import env var
from decouple import config

# imports for youtube api 
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors

# imports for spotify api
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

# grabbing my api key env variable 
DEV_KEY = config('YOUTUBE_API')

# creating an empty array to hold video titles
vidTitles = []
# get list of all track ids to import to spotify
all_track_ids = []

def main():

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    #DEV_KEY = "key_here"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=DEV_KEY)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId=config('YOUTUBE_PLAYLIST')
    ).execute()

    # serializing json
    json_object = json.dumps(request, indent = 4)

    # write the response to a json file
    with open('data.json', 'w') as outfile:
        outfile.write(json_object)
        
    # read the json file
    with open('data.json', 'r') as openFile:
        data = json.load(openFile)
        for a in data['items']:
            #grab the titles of the videos in my playlist
            vidTitles.append(a['snippet']['title'])
    
    # debug to make sure my vidTitles are there
    # for title in vidTitles:
    #     print('youtube titles : ' + title)

    #### SPOTIFY ####

    client_id = config('SPOTIPY_CLIENT_ID')
    client_secret = config('SPOTIPY_CLIENT_SECRET')
    redirectURI = config('SPOTIPY_REDIRECT_URI')
    user = config('SPOTIFY_USERNAME')

    # get spotipy credentails from env variables
    # auth_manager = SpotifyClientCredentials()
    # sp = spotipy.Spotify(auth_manager=auth_manager)


    scope = "playlist-modify-public, playlist-modify-private, user-read-recently-played"
    # oauth_manager = spotipy.oauth2.SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI, scope=scope, show_dialog=True, cache_path=None)
    token = util.prompt_for_user_token(user,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirectURI)
    sp = spotipy.Spotify(auth=token)

    # ignore this captions if it comes in the name of the youtube song
    ignoreCaption = [
        '(official video)',
        '[official video]',
        '(video oficial)',
        '( video oficial )',
        '[video oficial]',
        '(official music video)',
        '( official music video )',
        '[official music video]',
        '(official audio)',
        '[official audio]',
        '(instrumental)',
        '(Versión Urbana - Official Video)',
        '(Animated Video)', 
        '(music video)',
        '(audio / remix)',
        '(full version)'
    ]

    for songs in vidTitles:

        for ig in ignoreCaption:
            # convert both strings to lowercase for easier comparison
            lowercaseCaption = ig.lower()
            songName = songs.lower()
            if lowercaseCaption in songName:
                # if song has one of the ignoreCaptions then replace it with empty string
                songs = songName.replace(lowercaseCaption,"")

        # search for x song titles
        results = sp.search(q=songs, limit=1, type='track')

        # grab track ID to be used to add to spotify playlist
        for track in results['tracks']['items']:
            # debug make sure I am grabbing the correct songs
            #print("name : {} - uri : {}".format(track['name'], track['uri']))
            trackID = track['id']
            all_track_ids.append(trackID)    
    
    # grabs songs from current spotify plalist
    playlist_tracks = sp.user_playlist_tracks(user=user, playlist_id=config('SPOTIFY_PLAYLIST'), fields='items,uri,name,id,total')
    
    # If the track id already exists in spotify playlist 
    # then remove it so that duplicate are not created
    for pt in playlist_tracks['items']:
        # grab track id
        pl_id = pt['track']['id']

        # remove track id that already exist in the spotify playlist
        if pl_id in all_track_ids:
            all_track_ids.remove(pl_id)

    # check if there are tracks that need to be added to playlist   
    if all_track_ids:
        # add the tracks to my spotify playlist
        sp.user_playlist_add_tracks(user=user,playlist_id=config('SPOTIFY_PLAYLIST'),tracks=all_track_ids,position=None)

if __name__ == "__main__":
    main()