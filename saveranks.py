import requests
import urllib3



def save_rankings():
    url = 'https://football.fantasysports.yahoo.com/f1/222481/10/editprerank'

    proxies = {
        'http': 'http://127.0.0.1:8080', 
        'https': 'http://127.0.0.1:8080'
    }


    headers = {
        'Origin': 'https://football.fantasysports.yahoo.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'F=d=TwkFfZo9vDLQzMaWp2Wpt0khcJZH3sGn_CTH; PH=l=en-US; Y=v=1&n=1opfkipoc4sd8&l=1heb4o6/o&p=m260qv000000000&r=7s&intl=us; tbla_id=72713f36-0066-48d2-bea4-3729866486c3-tuctbd2f9c3; axids=gam=y-CL9.D59G2uJS5_Sxpc18MC9ovwTZVaAP0yGyrwzwWCfcE0afbg---A&dv360=eS1qOWFjNWNSRTJ1SHFMVGtIMkpmY3J1YnpLZWF3a25RZXl4RV9iWFdCS2p5SzlIZENnU2E4V084ZXR5eGlBYklIelhVNH5B&ydsp=y-JxhSKyFE2uK3fDqNWoraMZDZlWaMq0qF2bWhZ5dP7A39Ss_2DgIqaBteb31PQxpLLED2~A&tbla=y-4Kf2WkFG2uIq8MjTkY6bJi9Wmt9rDK3P9IaZt80qZ3vMDrdMrw---A; GUC=AQEACAJmr3dm2kIfPQRX&s=AQAAAOg-KrJN&g=Zq4vZw; A1=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; A3=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; ucs=tr=1723747431000; A1S=d=AQABBEJ02WQCEONw3HWLAassclJq07CDW-EFEgEACAJ3r2baZtxI0iMA-eABAAcIQnTZZLCDW-EID92BJPlnLNQKOc1b7lVySgkBBwoB9Q&S=AQAAAjRMjQB7UTDkVc9XF9Unoto; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiSlRFR1I2QzJaS05KTFkzRERXRlpIVFFWU1kiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJmNjNxUXZVZWhRbkgifX0.gQdJVwWUlKNIwsbwW5SNqe8l-xwubTwlzYc473xq3qPIEIt-1lCUKGUpNVapvlzmL0VJTtaZQULzBUjOa38X75GKplsU2q_LzZm6i8lnYdIPlppxHk8jhryIdt5u35IwCV57eBqTxouhaQW8HO-eFrRUjCRYE-Artv8JH7PqLqM; T=af=JnRzPTE3MjM2NjEwMzEmcHM9Vm5XanJUdElEWXNRNFZIc0o1Q2V3QS0t&d=bnMBeWFob28BZwFKVEVHUjZDMlpLTkpMWTNERFdGWkhUUVZTWQFhYwFBQVQ2WWMwYwFhbAFicm9sZXlnAXNjAWRlc2t0b3Bfd2ViAWZzAVBHTVBFbWxrMll0eAF6egFaOWlybUJnM0kBYQFRQUUBbGF0AVo5aXJtQgFudQEw&kt=EAA8XJ7saGE6rNhAtV2yQ72Ag--~I&ku=FAAARaVpLUAp8FNyszuwobI4O4gMGNQ8JIGBkkygOHeerWNrue8UEwq94XXlVprBZfjMBT_s_xJ_am6.yXWaN9l026wnFMuobzT3OgnM4Yuuob02pw6Tleh0a79syvg50lqH9.UraEfsJSixAzuMHIvsDDsRA5pMJlui27_AG7sfpo-~E; SPT=d=F2xR47BCZj8gYi6zX3JVm8Gk0p3U4lmXZxiV6hB60A1RTgh5Gz9MjwH7QPq4dORyY9XFybhpfe1mrnrxtyATtYR93b8goiAb9b4tLsniOLAs31.BRQQMqz0-&v=1; cmp=t=1723661034&j=0&u=1YNN; gpp=DBAA; gpp_sid=-1; SPTB=d=BWCsDPBctD6_5IRIwZZ4APDvEqbwcQhLWDnTusV8bm05Hrp7ZgFnJxQy9GMf7P.m14L89W8wMH_LFah6EuyzldSDRpMVkRZc9UNkjbGvkdM-&v=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }


    load_data = {
        'loadMorePlayer': 'true',
        'my_players_load': 'true',
        'excluded_players_load': 'true',
        'count': 1100,
        'pos': 'ALL'
    }


    save_data = {
        'stage': 1,
        'crumb': 'qJXN/WYerUJ',
        #'all_players': '32723,31002,40040,40030,31833,32671,29369,30121,34218,32696,33389,32676,29235,32675,40900,40896,9265,30125,29399,7200,32687,25812,30971,40068,33991,26662,40881,33393,40055,32692,40875,27564,40029,33500,31838,32711,33965,31883,30972,25785,34207,29279,40168,34120,40059,40118,33413,31868',
        'all_players': '',
        #'my_players': '30123',
        'my_players': '',
        #'excluded_players': '30121',
        'excluded_players': '',
        'save': 1,
        'pos': 'ALL',
        'submit-editprerank': 'Save Changes'
    }


    http_session = requests.session()   
    urllib3.disable_warnings()
    http_session.verify = False     
    http_session.proxies = proxies
  
    response=http_session.post(url=url, data=save_data, headers=headers)
    print(response)

save_rankings()