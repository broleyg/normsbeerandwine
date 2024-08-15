import 

class Auth():
    def __init__(self, proxy=True):
        if proxy:
            os.environ['HTTP_PROXY'] = os.environ['http_proxy'] = 'http://localhost:8080/'
            os.environ['HTTPS_PROXY'] = os.environ['https_proxy'] = 'http://localhost:8080/'
            os.environ['REQUESTS_CA_BUNDLE'] =os.environ['requests_ca_bundle'] = "/Users/bruce/workspace/draft/burp_certificate.pem"

def get_authorization_code():
    client_id = 'dj0yJmk9bnlqWlVhYkZXcWNaJmQ9WVdrOVQzTmFOa0pUTUZvbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTNi'
    client_secret  = '64441884a85c908b4282d0a2f6ac1c7262b7da94'
    base_url = 'https://api.login.yahoo.com/'
    redirect_uri = "https://127.0.0.1:5000/dashboard"
    authorization_code = 's6shzn5'
