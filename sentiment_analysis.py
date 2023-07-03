import re

characters = [
    "ROMEO", "MONTAGUE", "LADY MONTAGUE", "BENVOLIO", "ABRAM", "BALTHASAR", "JULIET", "CAPULET", "LADY CAPULET", "NURSE", "TYBALT", "PETRUCHIO", "SAMPSON", "GREGORY", "PETER", "ESCALUS", "PARIS", "MERCUTIO", "FRIAR LAWRENCE", "FRIAR JOHN"
]

def parse_dialogue(filename):
    dialogue = ''
    speaker = ''
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip() 
            words = line.split()
            if words: # check if the line is not empty
                first_word = words[0].rstrip(',')
                if first_word.isupper() and first_word in characters: 
                    if speaker: 
                        yield speaker, dialogue
                    speaker = first_word
                    dialogue = ' '.join(words[1:])
                else: 
                    dialogue += ' ' + line
        # Yield the final piece of dialogue
        if speaker: 
            yield speaker, dialogue

counter = 0
for speaker, dialogue in parse_dialogue('romeo_and_juliet.txt'):
    if counter < 30:
        print(f"{counter}:: {speaker}: {dialogue}")
        counter += 1
    else:
        break

