import sys
import argparse
import requests
import urllib3

class ScriptBase:

    def __init__(self):
        self.description = "placeholder for exploit description"
        self.parser = argparse.ArgumentParser()
        self.args = None
        self.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

        self.parser.add_argument('-v', '--verbose', help='show more information as the program is executing', action='store_true')
        self.parser.add_argument('-p', '--proxy', help='use localhost intercepting proxy on port 8080', action='store_true')
        self.http_session = None
        urllib3.disable_warnings()

    def define_args(self):    
        pass

    def run(self):
        pass

    def new_http_session(self):
        http_session = requests.session()        
        if self.args.proxy:
            http_session.proxies = self.proxies
        http_session.verify = False            
        return http_session

    def log(self, msg):
        print ('(+) {}'.format(msg))

    def run_script(self):
        self.define_args()
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
        self.log('START script')
        self.log('-------------')

        self.run()
        self.log('-------------')
        self.log('END script')
        self.log('')
        self.log(self.parser.epilog)

if __name__ == '__main__':
    script = ScriptBase()
    script.run_script()