import json, os

def search(word):
    """
    Search for a word in the dictionary.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    # Load the hausa dictionary
    with open(f"{path}/kamus.json", "r") as f:
        # Load the dictionary as a json file
        dictionary = json.load(f)
        # Close the file
        f.close()
        return dictionary.get(word, "Not found")