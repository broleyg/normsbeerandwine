import sys
import argparse
import requests
import urllib3
import json
import re
import os
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa

# https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = 'http://localhost:8080/'
os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = 'http://localhost:8080/'
os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"

class UpdateRanks:

    def __init__(self):
        self.description = "placeholder for exploit description"
        self.parser = argparse.ArgumentParser()
        self.args = None
        self.proxies = {
            'http': 'http://127.0.0.1:8080', 
            'https': 'https://127.0.0.1:8080'
        }

        self.parser.add_argument('-v', '--verbose', help='show more information as the program is executing', action='store_true')
        self.parser.add_argument('-p', '--proxy', help='use localhost intercepting proxy on port 8080', action='store_true')
        self.http_session = None

        self.translate = {
            "Kenny Gainwell": "Kenneth Gainwell",
            "Devon Achane": "De'Von Achane",
            "Chig Okonkwo": "Chigoziem Okonkwo",
            "Travis Etienne": "Travis Etienne Jr.",
            "Ken Walker": "Kenneth Walker III",
            "D.J. Moore": "DJ Moore",
            "Michael Pittman": "Michael Pittman Jr.",
            "A.J. Dillon": "AJ Dillon",
            "Odell Beckham": "Odell Beckham Jr.",
            "Jeff Wilson": "Jeff Wilson Jr.",
            "Kareem Hunt": "Kareem Hunt",
            "Leonard Fournette": "Leonard Fournette",
            "Marvin Mims": "Marvin Mims Jr.",
            "D.J. Chark": "DJ Chark Jr.",
            "John Metchie": "John Metchie III",
            "Patrick Mahomes II": "Patrick Mahomes",
            "Brian Robinson Jr.": "Brian Robinson",
            "Deebo Samuel": "Deebo Samuel Sr.",
            "Marvin Harrison": "Marvin Harrison Jr.",
            "Brian Robinson": "Brian Robinson Jr.",
            "Marquise Brown": "Hollywood Brown",
            "Zeke Elliott": "Ezekiel Elliott",
            "Josh Palmer": "Joshua Palmer",
            "Brian Thomas": "Brian Thomas Jr.",
            "Demario Douglas": "DeMario Douglas",
            "CeeDee Lamb": "CeeDee Lamb"
        }

    def new_http_session(self):
        http_session = requests.session()   
        urllib3.disable_warnings()
        http_session.verify = False     
        if self.args.proxy:
            http_session.proxies = self.proxies
        return http_session

    def log(self, msg):
        print ('(+) {}'.format(msg))

    def parse_line(self,line):
        regex = r'\W(?P<rank>[0-9]{1,3})\W*(?P<name>.*)\W(?P<position>[RWQT][BRE])'
        m = re.search(regex, line)
        if m:
            return m.groupdict()
        else:
            return None
        
    def pull_ranks(self):
        self.log('Pulling PPR ranks from HarrisFootball.com')
        self.log('')
        os.system('curl -s https://www.harrisfootball.com/top-160-ranks-draft | pandoc -f html -t plain > ranks_raw.txt')

        self.ranked = {}
        processing_lines = False
        with open('ranks_raw.txt', 'r') as i:
            with open('ranks.txt', 'w') as o:
                for line in i.readlines():
                        
                    if processing_lines:
                        entry = self.parse_line(line)

                        if entry:
                            name = entry['name'].strip()
                            if name in self.translate.keys():
                                name = self.translate[name]

                            self.log(name)
                            o.write(f'{name}\n')
                            self.ranked[name] = 0
                        #else:
                        #    self.log(f'error line = {line}')

                    if not processing_lines and 'PPR Scoring' in line:
                        processing_lines = True

    def load_ranks(self, rank_filename):
        self.log(f'Loading ranks from {rank_filename}')

        self.ranked = {}

        with open(rank_filename, 'r') as i:
            with open('ranks.txt', 'w') as o:
                for line in i.readlines():

                    entry = line.strip()

                    if entry:
                        name = entry.strip()
                        if name in self.translate.keys():
                            name = self.translate[name]

                        self.log(name)
                        o.write(f'{name}\n')
                        self.ranked[name] = 0
                    #else:
                    #    self.log(f'error line = {line}')

       

    def pull_players(self):
        oauth = OAuth2(None, None, from_file='oauth2.json')

        if not oauth.token_is_valid():
            oauth.refresh_access_token()

        game = yfa.Game(oauth, 'nfl')
        print(game.game_id())

        league_id =game.league_ids(year=2024)[0]
        print(league_id)

        league = game.to_league(league_id)

        #for team_id in league.teams():
        #    team = league.teams()[team_id]
        #    print(team_id)
        #    for key in team.keys():
        #        print(f'\t{key}={team[key]}')

        self.exclude = {}
        self.include = {}

        positions = ['QB','RB','WR','TE','K','DEF']
        for position in positions: #league.positions():
            print(position)
            #for player in league.free_agents(position):
            for player in league._fetch_players('A', position):
                if position == 'QB' or position == 'RB' or position == 'WR' or position == 'TE':
                    self.include[player['name']]= player
                else: # position == 'TE' or position == 'K' or position == 'DEF'
                    self.exclude[player['name']]= player

    def save_rankings(self):
        url = 'https://football.fantasysports.yahoo.com/f1/143087/10/editprerank'
        url = 'https://football.fantasysports.yahoo.com/f1/222481/10/editprerank'

        headers = {
            'Origin': 'https://football.fantasysports.yahoo.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            #'Cookie': 'OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiSlRFR1I2QzJaS05KTFkzRERXRlpIVFFWU1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJxb2plZFBBWnFRTWIifX0.mqP77GSOu9hIIMOsvsoOIAb0X-vEuGfX6OKWRGMn1BZBzEk1VWZh0RlH8stsUCftJfvHu18I68Jrm8ft40lWAXCB5XaYDyWuN7wDjpIHFbWlAelPeNslKdikeKvHcom5KdMoDrui6n4VleQ4Vj9fFRdUOUHeriyM58LCl9eRmkM; T=af=JnRzPTE2OTE5Nzg2MDkmcHM9Z0ZuNlp0VU9FZmNkNnBldW9QemdSUS0t&d=bnMBeWFob28BZwFKVEVHUjZDMlpLTkpMWTNERFdGWkhUUVZTWQFhYwFBRFcwbkhyUwFhbAFicm9sZXlnAXNjAWRlc2t0b3Bfd2ViAWZzAVBHTVBFbWxrMll0eAF6egF4dFkya0JBN0UBYQFRQUUBbGF0AXh0WTJrQgFudQEw&kt=EAABGArG5xzGbV92Zl8FEQEHw--~I&ku=FAAIqP2wlHf.NTXOcABhroGOgxEwZWfN_ZAPxr.5Jth0ywlbEpJ1L32k8axf789OG5.TJMQeggEm.nS8XdvxFEtesOUtudvYLG4K6JOR33hh8ui3dyrQR0HNN4WiFRcKOPfICX7cToHNFVVf1DCDWJmEMewuTcDC.PMDVr6HM_4vpw-~E; F=d=TwkFfZo9vDLQzMaWp2Wpt0khcJZH3sGn_CTH; PH=l=en-US; Y=v=1&n=1opfkipoc4sd8&l=1heb4o6/o&p=m260qv000000000&r=7s&intl=us; GUC=AQEACAJk2tllC0IfPQRX&s=AQAAAHY-Yi9g&g=ZNmLew; A1=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACALZ2mQLZdxI0iMA-eABAAcIQnTZZLCDW-EID9CkE1Y30x-Cck-34FwLDAkBBwoB1A&S=AQAAAr3eDCRUVI99_YArcL-gTGg; A3=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACALZ2mQLZdxI0iMA-eABAAcIQnTZZLCDW-EID9CkE1Y30x-Cck-34FwLDAkBBwoB1A&S=AQAAAr3eDCRUVI99_YArcL-gTGg; SPT=d=nk_Fgq7UF1r1NREnCru.mUBeeC9eePbCgJbx6UMySn42_HSsemlztLmgMmXJjkOGw6Nm75brvDNsM94khjYhoHtwoUoXGmjaefdXUgLUM_D4cC1MG5NT1To-&v=1; A1S=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACALZ2mQLZdxI0iMA-eABAAcIQnTZZLCDW-EID9CkE1Y30x-Cck-34FwLDAkBBwoB1A&S=AQAAAr3eDCRUVI99_YArcL-gTGg&j=US; gpp=DBAA; gpp_sid=-1; gam_id=y-CL9.D59G2uJS5_Sxpc18MC9ovwTZVaAP0yGyrwzwWCfcE0afbg---A; tbla_id=72713f36-0066-48d2-bea4-3729866486c3-tuctbd2f9c3; cmp=t=1692053652&j=0&u=1YNN; SPTB=d=JNBmi3WBKVnnVG1lSZE6o8ArjEK3JTKRtgXRSyZ.RPOmZ6D0HFaUNGi6wSRW55.4aI9O128ZKGQjHY3.B0e9yZx99EXNzuJCrWxsWd.n.tI-&v=1; __gpi=UID=00000d8b3386fa3a:T=1692055220:RT=1692055220:S=ALNI_MYZGavqz0TbqH9Oyd25idtiE3yCPg'
            'Cookie': 'Cookie: F=d=TwkFfZo9vDLQzMaWp2Wpt0khcJZH3sGn_CTH; PH=l=en-US; Y=v=1&n=1opfkipoc4sd8&l=1heb4o6/o&p=m260qv000000000&r=7s&intl=us; tbla_id=72713f36-0066-48d2-bea4-3729866486c3-tuctbd2f9c3; axids=gam=y-CL9.D59G2uJS5_Sxpc18MC9ovwTZVaAP0yGyrwzwWCfcE0afbg---A&dv360=eS1qOWFjNWNSRTJ1SHFMVGtIMkpmY3J1YnpLZWF3a25RZXl4RV9iWFdCS2p5SzlIZENnU2E4V084ZXR5eGlBYklIelhVNH5B&ydsp=y-JxhSKyFE2uK3fDqNWoraMZDZlWaMq0qF2bWhZ5dP7A39Ss_2DgIqaBteb31PQxpLLED2~A&tbla=y-4Kf2WkFG2uIq8MjTkY6bJi9Wmt9rDK3P9IaZt80qZ3vMDrdMrw---A; GUC=AQEACAJmr3dm2kIfPQRX&s=AQAAAOg-KrJN&g=Zq4vZw; A1=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; A3=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; ucs=tr=1723747431000; A1S=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiSlRFR1I2QzJaS05KTFkzRERXRlpIVFFWU1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJmNjNxUXZVZWhRbkgifX0.gQdJVwWUlKNIwsbwW5SNqe8l-xwubTwlzYc473xq3qPIEIt-1lCUKGUpNVapvlzmL0VJTtaZQULzBUjOa38X75GKplsU2q_LzZm6i8lnYdIPlppxHk8jhryIdt5u35IwCV57eBqTxouhaQW8HO-eFrRUjCRYE-Artv8JH7PqLqM; T=af=JnRzPTE3MjM2NjEwMzEmcHM9Vm5XanJUdElEWXNRNFZIc0o1Q2V3QS0t&d=bnMBeWFob28BZwFKVEVHUjZDMlpLTkpMWTNERFdGWkhUUVZTWQFhYwFBQVQ2WWMwYwFhbAFicm9sZXlnAXNjAWRlc2t0b3Bfd2ViAWZzAVBHTVBFbWxrMll0eAF6egFaOWlybUJnM0kBYQFRQUUBbGF0AVo5aXJtQgFudQEw&kt=EAA8XJ7saGE6rNhAtV2yQ72Ag--~I&ku=FAAARaVpLUAp8FNyszuwobI4O4gMGNQ8JIGBkkygOHeerWNrue8UEwq94XXlVprBZfjMBT_s_xJ_am6.yXWaN9l026wnFMuobzT3OgnM4Yuuob02pw6Tleh0a79syvg50lqH9.UraEfsJSixAzuMHIvsDDsRA5pMJlui27_AG7sfpo-~E; SPT=d=F2xR47BCZj8gYi6zX3JVm8Gk0p3U4lmXZxiV6hB60A1RTgh5Gz9MjwH7QPq4dORyY9XFybhpfe1mrnrxtyATtYR93b8goiAb9b4tLsniOLAs31.BRQQMqz0-&v=1; SPTB=d=RQdbRsdCZj8gKdZyI5NW24zu13JfLHn1OTRqgrYxWWUaZ_ePEC3SNM1UnD9rhCBNx7JcXS8WqhnztpDxeZWUfvGs0bBj9oMb_L9BhiV6GFE-&v=1; cmp=t=1723661034&j=0&u=1YNN; gpp=DBAA; gpp_sid=-1'
        }

        exclude_player_list = []
        for name, player in self.exclude.items():
            exclude_player_list.append(player['player_id'])
        exclude_list = str(exclude_player_list)[1:-1]

        
        ranked_player_list = []
        for player in self.ranked.keys():
            try:
                ranked_player_list.append(self.include[player]['player_id'])
            except Exception as e:
                self.log(f'{player} is not found')
        ranked_list = str(ranked_player_list)[1:-1]

        save_data = {
            'stage': 1,
            'crumb': 'ftt9TdPgI7W',
            'all_players': '',
            #'my_players': '32692,30121,33393,30423,30972,26686,30182,29399,40055,31005,30123,31002',
            #'excluded_players': '32676,33272,30977',
            'my_players': ranked_list,
            'excluded_players': exclude_list,
            'save': 1,
            'pos': 'ALL',
            'submit-editprerank': 'Save Changes'
        }

        http_session = self.new_http_session()
        os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"

        response=http_session.post(url=url, data=save_data, headers=headers)

    def update(self):
        self.args = self.parser.parse_args()
        self.log(self.parser.description)    
        self.log('')
        self.log('command line arguments:')
        self.log(vars(self.args))
        if self.args.proxy:
            self.log('proxy = {}'.format(self.proxies))
        else:
            self.log('no proxies in use')

        self.log('')
        self.log('START ')
        self.log('-------------')
        self.pull_ranks()
        #self.load_ranks('behrens.txt')
        #self.load_ranks('harmon.txt')
        #self.load_ranks('pianowski.txt')
        #self.load_ranks('waldman.txt')
        self.pull_players()
        self.save_rankings()
        self.log('-------------')
        self.log('END ')
        self.log('')
        self.log(self.parser.epilog)

if __name__ == '__main__':
    updater = UpdateRanks()
    updater.update()