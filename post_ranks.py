from scriptbase import ScriptBase
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json

class PostRanks(ScriptBase):

    def define_args(self):    
        self.parser.add_argument('-r', '--harris', help='Rank file for the Harris Top 160', default='harris.json')
        self.parser.add_argument('-b', '--behrens', help='Rank file for the Behrens Ranks', default='behrens.json')
        self.parser.add_argument('-m', '--harmon', help='Rank file for the Harmon Ranks', default='harmon.json')
                
    def load_translation(self):
        with open('translate.json', 'r') as t:
            self.translator = json.load(t)

    def load_ranks(self):
        rank_filename = self.args.harris
        rank_filename = self.args.behrens
        #rank_filename = self.args.harmon
        self.log(f'Loading ranks from {rank_filename}')

        self.ranked = {}
        with open(rank_filename, 'r') as i:
            self.ranked = json.load(i)

    def load_players(self):
        with open('include.json', 'r') as f:
            self.include = json.load(f)

        with open('exclude.json', 'r') as f:
            self.exclude = json.load(f)

    def save_rankings(self):
        url = 'https://football.fantasysports.yahoo.com/f1/222481/10/editprerank'

        headers = {
            'Origin': 'https://football.fantasysports.yahoo.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'F=d=TwkFfZo9vDLQzMaWp2Wpt0khcJZH3sGn_CTH; PH=l=en-US; Y=v=1&n=1opfkipoc4sd8&l=1heb4o6/o&p=m260qv000000000&r=7s&intl=us; tbla_id=72713f36-0066-48d2-bea4-3729866486c3-tuctbd2f9c3; axids=gam=y-CL9.D59G2uJS5_Sxpc18MC9ovwTZVaAP0yGyrwzwWCfcE0afbg---A&dv360=eS1qOWFjNWNSRTJ1SHFMVGtIMkpmY3J1YnpLZWF3a25RZXl4RV9iWFdCS2p5SzlIZENnU2E4V084ZXR5eGlBYklIelhVNH5B&ydsp=y-JxhSKyFE2uK3fDqNWoraMZDZlWaMq0qF2bWhZ5dP7A39Ss_2DgIqaBteb31PQxpLLED2~A&tbla=y-4Kf2WkFG2uIq8MjTkY6bJi9Wmt9rDK3P9IaZt80qZ3vMDrdMrw---A; GUC=AQEACAJmr3dm2kIfPQRX&s=AQAAAOg-KrJN&g=Zq4vZw; A1=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; A3=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; ucs=tr=1723747431000; A1S=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiSlRFR1I2QzJaS05KTFkzRERXRlpIVFFWU1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJmNjNxUXZVZWhRbkgifX0.gQdJVwWUlKNIwsbwW5SNqe8l-xwubTwlzYc473xq3qPIEIt-1lCUKGUpNVapvlzmL0VJTtaZQULzBUjOa38X75GKplsU2q_LzZm6i8lnYdIPlppxHk8jhryIdt5u35IwCV57eBqTxouhaQW8HO-eFrRUjCRYE-Artv8JH7PqLqM; T=af=JnRzPTE3MjM2NjEwMzEmcHM9Vm5XanJUdElEWXNRNFZIc0o1Q2V3QS0t&d=bnMBeWFob28BZwFKVEVHUjZDMlpLTkpMWTNERFdGWkhUUVZTWQFhYwFBQVQ2WWMwYwFhbAFicm9sZXlnAXNjAWRlc2t0b3Bfd2ViAWZzAVBHTVBFbWxrMll0eAF6egFaOWlybUJnM0kBYQFRQUUBbGF0AVo5aXJtQgFudQEw&kt=EAA8XJ7saGE6rNhAtV2yQ72Ag--~I&ku=FAAARaVpLUAp8FNyszuwobI4O4gMGNQ8JIGBkkygOHeerWNrue8UEwq94XXlVprBZfjMBT_s_xJ_am6.yXWaN9l026wnFMuobzT3OgnM4Yuuob02pw6Tleh0a79syvg50lqH9.UraEfsJSixAzuMHIvsDDsRA5pMJlui27_AG7sfpo-~E; SPT=d=F2xR47BCZj8gYi6zX3JVm8Gk0p3U4lmXZxiV6hB60A1RTgh5Gz9MjwH7QPq4dORyY9XFybhpfe1mrnrxtyATtYR93b8goiAb9b4tLsniOLAs31.BRQQMqz0-&v=1; cmp=t=1723661034&j=0&u=1YNN; gpp=DBAA; gpp_sid=-1; SPTB=d=BWCsDPBctD6_5IRIwZZ4APDvEqbwcQhLWDnTusV8bm05Hrp7ZgFnJxQy9GMf7P.m14L89W8wMH_LFah6EuyzldSDRpMVkRZc9UNkjbGvkdM-&v=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
            'crumb': 'qJXN/WYerUJ',
            'all_players': '',
            'my_players': ranked_list,
            'excluded_players': exclude_list,
            'save': 1,
            'pos': 'ALL',
            'submit-editprerank': 'Save Changes'
        }

        http_session = self.new_http_session()
        response=http_session.post(url=url, data=save_data, headers=headers)

    def run(self):
        self.http_session = self.new_http_session()

        self.load_translation()
        self.load_players()
        #self.pull_players()
        self.load_ranks()
        self.save_rankings()

if __name__ == '__main__':
    script = PostRanks()
    script.run_script()