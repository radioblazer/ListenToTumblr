from urlparse import urlparse

import pytumblr
import soundcloud


NUMBER_OF_POSTS = 50
ALBUM_NAME = "ListenToTumblr Mix"
PUBLIC_OR_PRIVATE = "private"

# create a Tumblr client object with access token
tumblr_client = pytumblr.TumblrRestClient(
    '',
    '',
    '',
    ''
)

# create a SoundCloud client object with access token
soundcloud_client = soundcloud.Client(client_id='',
                                      client_secret='',
                                      username='',
                                      password='')

# retrieve NUMBER_OF_POSTS from the user's dashboard
tumblr_dash = tumblr_client.dashboard(limit=NUMBER_OF_POSTS, type='audio')

# a dictionary to hold the songs
songs = {}

# find all SoundCloud track ID's from Tumblr dashboard
for x in range(len(tumblr_dash['posts'])):
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
soundcloud_client.post('/playlists', playlist={
    'title': ALBUM_NAME,
    'sharing': PUBLIC_OR_PRIVATE,
    'tracks': tracks
})

