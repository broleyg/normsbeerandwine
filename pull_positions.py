import json
import yahoo_fantasy_api as yfa
import os

from scriptbase import ScriptBase
from bs4 import BeautifulSoup
from yahoo_oauth import OAuth2


# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
#os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = 'http://localhost:8080/'
#os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = 'http://localhost:8080/'
#os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"

class PullPositions(ScriptBase):
                
    def pull_players(self):
        oauth = OAuth2(None, None, from_file='secrets.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        game = yfa.Game(oauth, 'nfl')
        league_id =game.league_ids(year=2024)[0]
        league = game.to_league(league_id)

        self.exclude = {}
        self.include = {}

        results = league.player_details('CeeDee Lamb')
        if len(results) == 1:
            player = results[0]
            player_name = player['name']['full']
            player['player_name'] = player['name']['full']
            self.include[player_name]= player
            
        positions = ['QB','RB','WR','TE','K','DEF']
        for position in positions: #league.positions():
            #for player in league.free_agents(position):
            players = league._fetch_players('A', position)
            for player in players:
                if position == 'QB' or position == 'RB' or position == 'WR' or position == 'TE':
                    self.include[player['name']]= player
                else: # position == 'TE' or position == 'K' or position == 'DEF'
                    self.exclude[player['name']]= player

        with open('exclude.json', 'w') as f:
            json.dump(self.exclude,f,indent=2)

        with open('include.json', 'w') as f:
            json.dump(self.include, f, indent=2)

    def run(self):
        self.pull_players()

if __name__ == '__main__':
    script = PullPositions()
    script.run_script()