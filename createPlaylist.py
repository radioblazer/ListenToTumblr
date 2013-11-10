import os, sys, inspect
from urlparse import urlparse
from sys import argv
import pytumblr
import soundcloud
# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
# if cmd_subfolder not in sys.path:
#    sys.path.insert(0, cmd_subfolder)
def createPlaylist(argv):
    tumblr_consumer_key = argv[1] 
    tumblr_consumer_secret = argv[2]
    tumblr_token = argv[3]
    tumblr_secret_token = argv[4]
    soundcloud_consumer_key = argv[5]
    soundcloud_consumer_secret = argv[6]
    soundcloud_token = argv[7] 
    soundcloud_secret_token = argv[8]
    privacy = "private"
    album_name = "Tumblr Mix"
    number_of_posts = 50
    
    # create a Tumblr client object with access token
    tumblr_client = pytumblr.TumblrRestClient(
        tumblr_consumer_key, 
        tumblr_consumer_secret,
        tumblr_token,
        tumblr_secret_token
    )

    # create a SoundCloud client object with access token
    soundcloud_client = soundcloud.Client(access_token=soundcloud_token)
    # retrieve recent audio posts from the user's dashboard
    tumblr_dash = tumblr_client.dashboard(limit=number_of_posts, type='audio')

    # a dictionary to hold the songs
    songs = {}

    # find all SoundCloud track ID's from Tumblr dashboard
    for x in range(50):
        try:
            if "soundcloud.com" in tumblr_dash['posts'][x]['source_url']:
                parsed = urlparse(tumblr_dash['posts'][x]['audio_url'])
                split_path = parsed.path.split('/')
                # save the ID of soundcloud track
                songs[x] = int(split_path[2])
        except:
            pass



    # create an array of track ids
    tracks = map(lambda id: dict(id=id), songs.values())

    # create the playlist
    created_playlist = soundcloud_client.post('/playlists', playlist={
        'title': album_name,
        'sharing': privacy,
        'tracks': tracks
    })
createPlaylist(argv)
