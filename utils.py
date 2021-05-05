from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from requests.exceptions import ReadTimeout


def progress_bar(complete, total, width=25, ch='='):
    """ Creates a progress bar based on the number of completed
        tasks over the number of total tasks. Returns enclosed
        in brackets, with percentage at the end

    Args:
        complete(int): total complete tasks
        total(int): total tasks
        width(int): number of characters wide bar should be
        ch(str): the character to use for each segment of the loading bar
    
    Note:
        assumes both numbers are positive.

    Returns:
        bar(str): the progress bar as a string

    Examples:
        progress_bar(0, 100)  -> '[                         ] 0.0%'
        progress_bar(30, 100) -> '[=======>                 ] 30.0%'
        progress_bar(3, 100)  -> '[>                        ] 3.0%'
        progress_bar(48, 100) -> '[============>            ] 48.0%'
    
    """


    if(complete == total):
        return "\033[32;1m[{}] 100.0%\033[0m".format(ch * width)
    else:
        ratio = complete / total
        filled = int(ratio * width)
        empty = width - filled - 1
        
        return "\033[36m[{}>{}] {:.1f}%\033[0m".format(ch * filled, ' ' * empty, round(100*ratio, 1))

def progress_frac(complete, total):
    ccount = len(str(total)) - len(str(complete))

    return "[ {}{} / {} ]".format(' '*ccount, complete, total)


# messy way to get info about what attributes are generally missing.
# I would add a better way, but this is just a script, so it's not supremely
# important
missing_tracker = defaultdict(int)
tracks_attribs = ["artists", "duration_ms", "release_date", "explicit", "popularity"]
features_attribs = ["danceability", "energy", "tempo", "loudness", "time_signature"]

def check_missing(track, ttype):
    global missing_tracker
    if(ttype == "track"):
        for att in tracks_attribs:
            if(att == "release_date"):
                if(att not in track["album"]):
                    missing_tracker[att] += 1
            elif(att not in track):
                missing_tracker[att] += 1
    elif(ttype == "features"):
        for att in features_attribs:
            if(att not in track):
                missing_tracker[att] += 1

def get_missing():
    global missing_tracker
    return missing_tracker

def get_spotify_client():
    with open("auth/client_creds.json") as creds_fp:
        creds = json.load(creds_fp)

    auth_manager = SpotifyClientCredentials(client_id=creds["client_id"], client_secret=creds["client_secret"])
    sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10, retries=10)
    
    return sp

def get_songs(spotify, songs, song_dict = None):
    """ Gets a set of up to 50 spotify songs from a list of tracks

        Args:
            spotify(spotipy.Spotify): the current spotify client
            songs(list): the songs to be aquired
            song_dict(defaultdict<list>): The initial value of the dictionary to add
                the songs too.
        
        Returns:
            song_data: if you passed song_dict, this will be the same reference

    """
    if(song_dict is None):
        song_dict = defaultdict(list)
    
    #song_list = list(songs.keys())
    res = None
    try:
        res = spotify.tracks(songs)
    except ReadTimeout:
        print("\033[K\033[1000DHTTP timeout. Trying again...", end="")
        # gross
        try:
            res = spotify.tracks(songs)
        except:
            print("failed. Skipping...")
            return song_dict
        else:
            print("success.")


    if(len(songs) > 50):
        raise ValueError("Too many songs")


    for track in res["tracks"]:
        sid = None
        try:
            sid = track["id"]
        
            check_missing(track, "track")       
            # number of artists
            song_dict[sid].append(len(track["artists"]))
            # primary artist
            song_dict[sid].append(track["artists"][0]["id"])
            # release year
            song_dict[sid].append(track["album"]["release_date"][:4])
            # track_length
            song_dict[sid].append(track["duration_ms"])
            # is-explicit
            song_dict[sid].append(track["explicit"])
            # popularity
            song_dict[sid].append(track["popularity"])
        except:
            if(sid):
                song_dict.pop(sid, None)

    return song_dict

def get_song_info(spotify, songs, song_dict):
    """ Gets audio features from spotify's api for up to
        100 tracks

        Args:
            spotify(spotipy.Spotify): the spotify client
            songs(list): songs to be gotten
            song_dict(dict): All songs must already be present and populated through
                get_songs

        Returns:
            song_dict(dict): same reference as the argument
    """
    if(len(songs) > 100):
        raise ValueError("Too many songs: " + str(len(songs)))
    
    res = None
    try:
        res = spotify.audio_features(songs)
    except ReadTimeout:
        print("\033[K\033[1000DHTTP timeout. Trying again...", end="")
        try:
            res = spotify.audio_features(songs)
        except:
            print("failed. Skipping...")
            return song_dict
        else:
            print("success.")

    for track in res:
        global missing_tracker
        sid = None
        try:
            sid = track["id"]
            if sid not in song_dict:
                missing_tracker["l1drops"] += 1
                continue
        
            check_missing(track, "features")

            # danceability
            song_dict[sid].insert(-1, track["danceability"])
            # energy
            song_dict[sid].insert(-1, track["energy"])
            # tempo
            song_dict[sid].insert(-1, track["tempo"])
            # loudness
            song_dict[sid].insert(-1, track["loudness"])
            # time signature
            song_dict[sid].insert(-1, track["time_signature"])
        except:
            if(sid):
                song_dict.pop(sid, None)
            missing_tracker["l2drops"] += 1
    return song_dict



def get_artist_info(spotify, artists, artist_dict):
    """ Gets artist information from spotify web api

        Args:
            spotify(spotipy.Spotify): the spotify client
            songs(list): songs to be gotten
            song_dict(dict): All songs must already be present and populated through
                get_songs

        Returns:
            song_dict(dict): same reference as the argument
    """
    if(len(artists) > 50):
        raise ValueError("Too many artists: " + str(len(artists)))
    
    res = None
    try:
        res = spotify.artists(artists)
    except ReadTimeout:
        print("\033[K\033[1000DHTTP timeout. Trying again...", end="")
        try:
            res = spotify.audio_features(artists)
        except:
            print("failed. Skipping...")
            return artist_dict
        else:
            print("success.")
    
    for artist in res["artists"]:
        sid = None
        try:
            sid = artist["id"]
            # artist_popularity
            artist_dict[sid].append(artist['popularity'])
            # genres
            artist_dict[sid].append(artist['genres'])
        except Exception as e:
            print('\n', e, '\n')
            if(sid and sid in artist_dict):
                artist_dict.pop(sid, None)
    return artist_dict



