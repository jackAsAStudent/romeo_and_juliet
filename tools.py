import re

def create_character_dict(characters):
    character_dict = {}
    for i in range(len(characters)):
        for j in range(i+1, len(characters)):
            character_dict[(characters[i], characters[j])] = []
            character_dict[(characters[j], characters[i])] = []
    return character_dict

def remove_brackets(text):
    return re.sub(r'\[.*?\]', '', text)