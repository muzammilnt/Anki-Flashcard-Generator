import requests
import socket


URL = "http://localhost:8765/"

def upload_anki(word,definition,card_type,mp3=None):

    """
        upload a single note to Anki via AnkiConnect.
        Default deck name is : vocabulary-auto
    """

    payload = {
        "action": "addNotes",
        "version": 5,
        "params": {
            "notes": [
                {
                    "deckName": "vocabulary-auto",
                    "modelName": card_type,
                    "fields": {
                        "Front": word,
                        "Back": definition
                    },
                    "tags": [
                        "automate"
                    ],
                    "audio": [{
                        "url" : mp3,
                        "fields" : ["Front"],
                        "filename": f"{word}.mp3",
                        "skipHash": "7e2c2f954ef6051373ba916f000168dc"

                    }]


                }
            ]
        }
    }

    requests.post(URL,json=payload)

# check if AnkiConnect is running and listening
def is_anki_listening(host="127.0.0.1", port =8765,timeout= 1):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host,port))
            return True
        except (ConnectionRefusedError,socket.timeout):
            return False

# Create a deck if not existed
def ensure_deck_exists():
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": "vocabulary-auto"}
    }
    requests.post(URL, json=payload)
