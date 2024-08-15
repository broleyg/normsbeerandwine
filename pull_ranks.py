import json

from scriptbase import ScriptBase
from bs4 import BeautifulSoup


class PullRanks(ScriptBase):

    def define_args(self):    
        self.parser.add_argument('-r', '--harris', help='URL for the Harris Top 160', default='https://www.harrisfootball.com/top-160-ranks-draft')
        self.parser.add_argument('-b', '--behrens', help='URL for the Behrens Ranks', default='https://partners.fantasypros.com/api/v1/consensus-rankings.php?sport=NFL&year=2024&week=0&id=1663&position=ALL&type=ST&scoring=HALF&filters=7&export=json')
        self.parser.add_argument('-m', '--harmon', help='URL for the Harmon Ranks', default='https://partners.fantasypros.com/api/v1/consensus-rankings.php?sport=NFL&year=2024&week=0&id=1663&position=ALL&type=ST&scoring=HALF&filters=747&export=json')
                
    def load_translation(self):
        with open('translate.json', 'r') as t:
            self.translator = json.load(t)

    def load_players(self):

        with open('exclude.json', 'r') as f:
            self.exclude = json.load(f)

        with open('include.json', 'r') as f:
            self.include = json.load(f)

    def pull_ranks(self):
        self.players = {}
        url = self.args.harris
        self.log(f'{url}')

        response = self.http_session.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        elements = soup.find_all("td", text='PPR Scoring')
        if len(elements) == 1:
            ppr_element = elements[0]
            ppr_table = ppr_element.parent.parent
            table_rows = ppr_table.find_all('tr')        
            for table_row in table_rows:                
                value = table_row.contents[3].text
                if value not in ('','RB','QB','WR','TE','PPR Scoring'):
                    player_name = self.normalize_name(table_row.contents[3].text.strip())
                    if player_name in self.include:
                        player = {}
                        try:
                            player_id = self.include[player_name]['player_id']
                            player['player_id'] = player_id
                            player['rank_ecr'] = table_row.contents[1].text
                            player['player_position_id'] = table_row.contents[5].text
                            player['player_name'] = player_name
                            self.players[player_name] = player
                        except Exception as e:
                            player_id = ''
                            self.log(f'{player_name} is not found, no player_id identified!')

                    else:
                        self.log(f'unable to find {player_name} in master Yahoo player list')

        with open('harris.json', mode='w') as f:
            f.write(json.dumps(self.players, indent=2))

        url = self.args.behrens
        response = self.http_session.get(url)
        ranks = response.json()
        self.players = self.filter_ranks(ranks)

        with open('behrens.json', mode='w') as f:
            json.dump(self.players,f,indent=2)

        url = self.args.harmon
        response = self.http_session.get(url)
        ranks = response.json()
        self.players = self.filter_ranks(ranks)

        with open('harmon.json', mode='w') as f:
            json.dump(self.players,f,indent=2)

    def normalize_name(self, player_name):
        if player_name in self.translator:          
            old_name = player_name              
            player_name = self.translator[old_name]
            self.log(f'translating from {old_name} to {player_name}')
        return player_name        


    def filter_ranks(self, ranks):
        filtered_players = {}

        for player in ranks['players']:
            if player['player_position_id'] in ('QB,RB,WR,TE'):
                ranked_player = {}
                player_name = self.normalize_name(player['player_name'].strip())

                if player_name in self.include:
                    ranked_player = {}
                    try:
                        player_id = self.include[player_name]['player_id']

                        if str(player_id) != str(player['player_yahoo_id']):
                            self.log(f'{player_name} has id as {player["player_yahoo_id"]} but yahoo says its {player_id}')

                        ranked_player['player_id'] = player_id
                        ranked_player['rank_ecr'] =  player['rank_ecr']
                        ranked_player['player_position_id'] = player['player_position_id']
                        ranked_player['player_name'] = player_name
                        filtered_players[player_name] = ranked_player
                    except Exception as e:
                        player_id = ''
                        self.log(f'{player_name} is not found, no player_id identified!')

                else:
                    self.log(f'unable to find {player_name} in master Yahoo player list')                        
                
        return filtered_players

    def run(self):
        self.http_session = self.new_http_session()

        self.load_translation()
        self.load_players()
        self.pull_ranks()

if __name__ == '__main__':
    script = PullRanks()
    script.run_script()