from collections import defaultdict

def get_id(token):
    """ Gets the proper spotify ID from the given token """

    return "spotify:track:" + token

def merge_dicts(dict1, dict2):
    result_dict = defaultdict(int)

    for key in dict1:
        result_dict[key] += dict1[key]

    for key in dict2:
        result_dict[key] += dict2[key]

    return result_dict
