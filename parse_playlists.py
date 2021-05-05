#!/usr/bin/python3
""" Parses the playlist datasets. If run as a script, reads filenames from argv """

import json
import sys
from collections import defaultdict
import os.path

def load_json(path):
    """ Loads a JSON file into a dictionary

    Args:
        path(str): the path to the json file
    
    Returns:
        playlists(dict): the playlist json as a dictionary 
    """
    if(os.path.exists(path) and os.path.isfile(path)):
        with open(path) as f:
            playlists = json.load(f)
        
        return playlists
    else:
        raise FileNotFoundError("File " + str(path) + " does not exist or is not readable")
    

def parse_playlists(lists_json, songs=None):
    """ Parses one loaded json (dict) file of playlist information
    
    Args:
        lists_json(dict): The data loaded from the spotify dataset
        songs(defaultdict<int>): if you want an initial value that you
            are working with. It needs to be a defaultdict<int>

    Returns:
        songs(defaultdict<int>): dict cointaining a clipped song id
            and the number of occurances

    Notes:
        Raises IndexError if there is no "playlists" key present
    """
    lists = lists_json["playlists"]
    if(songs is None):
        songs = defaultdict(int)

    for playlist in lists:
        if(playlist["num_tracks"] != 0):
            for song in playlist["tracks"]:
                song_id = song["track_uri"][14:]
                songs[song_id] += 1

    return songs


if __name__ == "__main__":
    if(len(sys.argv) < 3):
        sys.stderr.write("USAGE:\n\tparse_playlists.py DEST [FILES]")
        exit(-1)
    
    if(os.path.exists(sys.argv[1])):
        res = input("WARNING: file already exists. Overwrite? (y/N): ")
        if(res != 'y' and res != 'Y'):
            exit(-2)

    songs_dict = defaultdict(int)
    for path in sys.argv[2:]:
        print("Loading '" + path + "'...", end='')
        playlists = load_json(path)
        print("done")
        print("Parsing...", end='')
        parse_playlists(playlists, songs=songs_dict)
        print("done")
    
    with open(sys.argv[1], 'w') as o:
        json.dump(songs_dict, o)

