#!/usr/bin/python3

import json
import utils
from collections import defaultdict
from tabulate import tabulate

def load_data():
    with open('./data/processed.json') as fp:
        data = json.load(fp)

    return data

def get_artists(dataset):
    """ Gets all unique artists from the dataset """
    artists = { dataset[song][1] for song in dataset }
    
    return list(artists)

def slice_artists(artists):
    """ slices a list of artists in to a list of slices with size 50 """

    i = 0
    slices = []
    while(i < len(artists)):
        if(len(artists) - i > 50):
            slices.append(artists[i:50+i])
        else:
            slices.append(artists[i:])

        i += 50

    return slices

def process_genres(artist_data):
    genres = defaultdict(int)
    for artist in artist_data:
        for genre in artist_data[artist][1]:
            genres[genre] += 1
    
    return genres

if(__name__ == "__main__"):
    print("Loading song data...", end='', flush=True)
    song_data = load_data()
    print('done', flush=True)
    print("Parsing and slicing artists...", end='', flush=True)
    artists = get_artists(song_data)
    slices = slice_artists(artists)
    print('done\n', flush=True)

    spotify = utils.get_spotify_client()
    
    artist_data = defaultdict(list)
    tot = len(slices)

    for i, aslice in enumerate(slices):
        print("\033[K\033[1000D",utils.progress_frac(i+1,tot), " \033[3mFetching Artist Data\033[0m    ", 
                utils.progress_bar(i+1,tot, width=30), flush=True, sep='', end='')
        artist_data = utils.get_artist_info(spotify, aslice, artist_data)
    
    print("done", flush=True)
    
    print("Processing Genres...", end='', flush=True)
    genres = process_genres(artist_data)
    print("done")

    print("Saving artist data to output/artists.json")
    with open('./output/artists.json', 'w') as fp:
        json.dump(artist_data, fp)

    print("Saving pretty artist data to output/artists-pretty.json")
    with open('./output/artists-pretty.json', 'w') as fp:
        json.dump(artist_data, fp, indent=2)

    print("Saving genres to output/genres.json")
    with open('./output/genres.json', 'w') as fp:
        json.dump(genres, fp)

    print("Saving pretty genres to output/genres-pretty.json")
    with open('./output/genres-pretty.json', 'w') as fp:
        json.dump(genres, fp, indent=2)
    



