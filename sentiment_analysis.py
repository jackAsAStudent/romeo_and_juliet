from character_dict import create_character_dict
from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

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


if __name__ == '__main__':
    sentiments = create_character_dict(characters)
    print(sentiments)

    load_dotenv()
    cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
    cog_key = os.getenv('COG_SERVICE_KEY')

    # Create client using endpoint and key
    credential = AzureKeyCredential(cog_key)
    cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

    counter = 0
    for speaker, dialogue in parse_dialogue('romeo_and_juliet.txt'):
        if counter < 30:
            entities = cog_client.recognize_entities(documents=[dialogue])[0]
            for entity in entities.entities:
                if entity.category == 'Person' and entity.text.upper() in characters:
                    sentiment = cog_client.analyze_sentiment(documents=[dialogue])[0]
                    sentiments[speaker, entity.text.upper()].append(sentiment.confidence_scores.positive)
                    print(f"Character: {entity.text.upper()} Sentiment: {sentiment.confidence_scores.positive}")
            print(f"{counter}:: {speaker}: {dialogue}")
            counter += 1
        else:
            break


