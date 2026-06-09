import webbrowser
import random
from urllib import parse
from src.registration import REDIRECT_URI, SCOPE, get_client_id_from_file


def get_encoded_url():
    # Read the existing client_id from file instead of registering a new client
    client_id = get_client_id_from_file()
    f = {
        "client_id": client_id,
        "response_type": "code",
        "scope": SCOPE,
        'redirect_uri': REDIRECT_URI,
        'state': f'random-{random.randint(a=100, b=200)}'
    }
    return parse.urlencode(f)


def open_url():
    url = f"https://in-info-web20.luddy.indianapolis.iu.edu/oauth2/default/authorize?{get_encoded_url()}"
    webbrowser.open(url, new=0, autoraise=True)


if __name__ == '__main__':
    open_url()