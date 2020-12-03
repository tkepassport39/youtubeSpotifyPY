import os
from os import path
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

# creating an empty array to hold video titles
vidTitles = []
# get list of all track ids to import to spotify
all_track_ids = []

######## YOUTUBE ########
def fetch_youtube_video_titles(youtube_dev_key, youtube_playlist_id):

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=youtube_dev_key)

    # try to grab youtube playlist data
    try:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId= youtube_playlist_id
        ).execute()
    except:
        print("Error getting Youtube playlist")
        exit()
    # if no exceptions continue running the following code
    else:
        # serializing json
        json_object = json.dumps(request, indent = 4)
        
        # write the new response to a json file
        with open('data.json', 'w') as outfile:
            outfile.write(json_object)

        # read the new json file
        with open('data.json', 'r') as openFile:
            data2 = json.load(openFile)

        # grab the titles of the videos in my playlist and append to array
        for a in data2['items']:
            vidTitles.append(a['snippet']['title'])

        return True


######## SPOTIFY ########
def add_tracks_to_spotify(
    sp_client_id, 
    sp_client_secret, 
    sp_redirect_uri,
    sp_username,
    sp_playlist
    ):

    # assign the env variables
    client_id = sp_client_id
    client_secret = sp_client_secret
    redirectURI = sp_redirect_uri
    user = sp_username

    scope = "playlist-modify-public, playlist-modify-private, user-read-recently-played"
    
    try:
        # generate token 
        token = util.prompt_for_user_token(
            user,scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirectURI
            )
        sp = spotipy.Spotify(auth=token)
    except:
        print("Error spotify auth")
        exit()  
    else:
        # ignore these captions if it comes in the name of the youtube song
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
            '[music video]',
            '(audio / remix)',
            '(full version)',
            '(Official Lyric Video)',
            '(Clip officiel)',
            '(Dirty Version)',
            'Official Music Video',
            '|',
            '(Audio)',
            '(Official Performance Video)'
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
                print("Song name : {} --- uri : {}".format(track['name'], track['uri']))
                trackID = track['id']
                all_track_ids.append(trackID)    
        
        # grabs songs from current spotify plalist
        playlist_tracks = sp.user_playlist_tracks(user=user, playlist_id=sp_playlist, fields='items,uri,name,id,total')
        
        """ 
        If the track id already exists in spotify playlist 
        then remove it so that duplicate are not created
        """
        for pt in playlist_tracks['items']:
            # grab track id
            pl_id = pt['track']['id']

            # remove track id that already exist in the spotify playlist
            if pl_id in all_track_ids:
                all_track_ids.remove(pl_id)

        # check if there are tracks that need to be added to playlist   
        if all_track_ids:
            # add the tracks to my spotify playlist
            sp.user_playlist_add_tracks(
                user=user,
                playlist_id=sp_playlist,
                tracks=all_track_ids,
                position=None
            )


if __name__ == "__main__":
    
    # execute all youtube related stuff
    changeInPlaylist = fetch_youtube_video_titles(config('YOUTUBE_API'), config('YOUTUBE_PLAYLIST'))

    # execute all spotify related stuff
    if (changeInPlaylist):
        add_tracks_to_spotify(
            config('SPOTIPY_CLIENT_ID'),
            config('SPOTIPY_CLIENT_SECRET'),
            config('SPOTIPY_REDIRECT_URI'),
            config('SPOTIFY_USERNAME'),
            config('SPOTIFY_PLAYLIST')
        )