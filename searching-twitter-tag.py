import requests
import requests_oauthlib
import sys
import json


def init_auth(file):
    (CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET_TOKEN) = open(file, 'r').read().splitlines()
    auth_obj = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET_TOKEN)
    if verify_credentials(auth_obj):
        print('Validated credentials OK')
        return auth_obj
    else:
        print('Credential validation failed')
        sys.exit(1)


def verify_credentials(auth_obj):
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    response = requests.get(url, auth=auth_obj)
    return response.status_code == 200


def search(auth_obj):
    params = {'q': '#EndAnglophoneCrisis'}
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    response = requests.get(url, params=params, auth=auth_obj)
    return response


if __name__ == '__main__':
    auth_obj = init_auth('credential.txt')
    response = search(auth_obj)
    print(json.dumps(response.json(), indent=2))
