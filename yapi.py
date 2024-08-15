from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

import os
import requests

# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = 'http://localhost:8080/'
os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = 'http://localhost:8080/'
os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"



oauth = OAuth2(None, None, from_file='oauth2.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

game = yfa.Game(oauth, 'nfl')
print(game.game_id())

league_id =game.league_ids(year=2024)[0]
print(league_id)

league = game.to_league(league_id)

for team_id in league.teams():
    team = league.teams()[team_id]
    print(team_id)
    for key in team.keys():
        print(f'\t{key}={team[key]}')

exclude = {}
include = {}

defenses = league._fetch_players('A', 'DEF')
print(len(defenses))
kickers = league._fetch_players('A', 'K')
print(len(kickers))

positions = ['QB','RB','WR','TE','K','DEF']
for position in positions: #league.positions():
    print(position)
    for player in league.free_agents(position):
        if position == 'QB' or position == 'RB' or position == 'WR':
            include[player['name']]= player
        else: # position == 'TE' or position == 'K' or position == 'DEF'
            exclude[player['name']]= player
print(include)
print(exclude)