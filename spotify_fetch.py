#!/usr/bin/python3
import utils
from collections import defaultdict
import json
import pprint

def load_songs(path):
    with open(path) as fp:
        songs_dict = json.load(fp)

    return songs_dict

def save_songs(path, songs_dict):
    with open(path, "w") as fp:
        json.dump(songs_dict, fp)


def split_songs(song_list):
    slices_50 = []
    slices_100 = []
    
    curr_50, curr_100 = [],[]

    for song in song_list:
        if(len(curr_50) == 50):
            slices_50.append(curr_50)
            curr_50 = []
        if(len(curr_100) == 100):
            slices_100.append(curr_100)
            curr_100 = []

        curr_50.append(song)
        curr_100.append(song)

    if(len(curr_50) != 0):
        slices_50.append(curr_50)
    if(len(curr_100) != 0):
        slices_100.append(curr_100)

    return slices_50, slices_100


if __name__ == "__main__":
    songs = load_songs("./output/all.json")

    slices_50, slices_100 = split_songs(list(songs.keys()))

    print("Songs:", len(songs))
    print("Split_50:", len(slices_50))
    print("Split_100:", len(slices_100), "\n")

    pp = pprint.PrettyPrinter(indent=2)

    sp = utils.get_spotify_client()
    
    songs_dict = defaultdict(list)
    
    for i, sslice in enumerate(slices_50):
        print("\033[K\033[1000DGetting Song Metadata: " + str(i + 1) + "/" + str(len(slices_50))
                + "    Dropped: " + str((i * 50) - len(songs_dict)), flush=True, end='')
        songs_dict = utils.get_songs(sp, sslice, songs_dict)
    l1_total = len(songs_dict)
    print("\nFinished stage 1 with", l1_total, "out of", len(songs), "songs")
    for i, sslice in enumerate(slices_100):
        print("\033[K\033[1000DGetting Song Attributes: " + str(i + 1) + "/" + str(len(slices_100)) 
                + "    Dropped: " + str(l1_total - len(songs_dict)), flush=True, end='')
        songs_dict = utils.get_song_info(sp, sslice, songs_dict)
    
    print("\nDropped", len(songs) - len(songs_dict), "out of", len(songs), "songs")
    #print("Dropped", 300 - len(songs_dict), "out of", 300, "songs")
    print("missing_reason info")
    pp.pprint(dict(utils.get_missing()))
    save_songs("output/finished-now.json", songs_dict)
    print("saved to output/finished-now.json")
    

