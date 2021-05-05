from collections import defaultdict

genre_words= {
    "jazz" : ['jazz', 'bop', 'bossa', 'gypsy', 'fusion', 'calypso'],
    "hip hop": ["hiphop", "hip hop", "rap", "boom bap"],
    "folk" : ["ballad", "folk", "traditional", 'hula', 'fiddle', 'hist'],
    "indie": ["indie"],
    "rock": ["rock"],
    "r&b": ["soul", "r&b"],
    "metal": ["metal", "djent", "grunge", "sludge", 'prog', 'hardcore', 'thrash', 'core'],
    "pop": ["pop", 'euro'],
    "punk": ["punk", "emo"],
    "instrumental": ["instrumental", "classical", "baroque", "ensemble", "orchestra", "vgm",
        "violin", "piano", "cello", "soundtrack", "score", 'choir', 'guitar', 'acoustic',
        'symph', 'brass'],
    "religious": ["worship", "praise" ],
    "country": ["country", "grass" ],
    "electronic": ["edm", "step", "jungle", "vaporwave", "idm", "electro", "techno", "synth", "dance", "house", "club", "perreo", "glitch"],
    "ambient": ["ambient", "muzak"],
    "reggae": ["reggae"],
    "disco": ["disco", "tek"],
    "funk": ["funk"],
    "blues": ["blues"],
    "experimental": ["experimental", "psych", 'alternative'],
    "show tunes": ["musical", "show tunes"],
    "idol": ["idol", "k-", "j-", "k pop", "j pop"]
}

def categorize_all(genres):
    tracker = defaultdict(list)

    for genre in genres:
        added_one = False
        for category, substrs in genre_words.items():
            for substr in substrs:
                if(substr in genre):
                    tracker[category].append(genre)
                    added_one = True
                    break
        if (not added_one): 
            tracker["misc"].append(genre)
    
    return tracker
