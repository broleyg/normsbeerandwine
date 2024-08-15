import requests
import requests_oauthlib
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import os

os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = 'http://localhost:8080/'
os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = 'http://localhost:8080/'
os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"

def authenticate():
    oauth = OAuth2(None, None, from_file='secrets.json')
    if not oauth.token_is_valid():
        oauth.refresh_access_token()

def dump_leagure():
    game = yfa.Game(oauth, 'nfl')
    print(game.game_id())


def main(): 
    authenticate()


if __name__ == '__main__':
    main()