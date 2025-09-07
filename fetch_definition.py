import requests

MAX_DEFINITIONS = 4
MAX_SENTENCES_PER_POS = 2

def get_definition(word):
    """
        Fetch definitions, example sentences, and audio pronunciation for a given word
        using the free Dictionary API. Limits the number of definitions and example
        sentences per part of speech.
    """
    text_format = ""
    audio = []
    example_sentences = []


    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # Return None if the word is not found or request fails
    if response.status_code != 200:
        return None, None
    # API response
    data = response.json()

    # extract audio pronunciation links
    for d in data[0].get("phonetics", []):
        if d.get("audio"):
            audio.append(d.get("audio"))


    # extract part of speech and definition
    for data_1 in data[0].get("meanings", []):
        part_of_speech = data_1.get("partOfSpeech")
        text_format += f"<h3>====({part_of_speech.upper()})====</h3>"

        counts_of_definition = 0
        counts_of_sentences = 0

        for data_2 in data_1.get("definitions", []):
            definition = data_2.get("definition")
            text_format += f"-{definition}<br>"
            counts_of_definition += 1

            #Add example sentences if available, up to the max per POS
            example_sentence = data_2.get("example")
            if example_sentence and counts_of_sentences < MAX_SENTENCES_PER_POS:
                formatted_sentence = f"{example_sentence} ({part_of_speech.upper()})"
                example_sentences.append(formatted_sentence)
                counts_of_sentences += 1

            if counts_of_definition >= MAX_DEFINITIONS:
                break

    # Append all example sentences
    text_format += "<h3>====Example:====</h3>"
    for each in example_sentences:
        text_format += f"-{each}<br>"

    # censor teh target word for flashcard formatting
    final_format = text_format.replace(f"{word}", "---")
    return final_format,audio[0]



