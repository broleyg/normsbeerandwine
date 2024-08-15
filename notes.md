* Yahoo Client App
- App Name = fftools
- App ID = OsZ6BS0Z
- App Registration = https://developer.yahoo.com/apps/OsZ6BS0Z/

- FantasyPros ECR rankings 
curl "https://partners.fantasypros.com/api/v1/consensus-rankings.php?sport=NFL&year=2024&week=0&id=1663&position=ALL&type=ST&scoring=HALF&filters=7%3A9%3A
285%3A747%3A4338&export=json" > yahoo.json

* References
- [Fantasy Sports API](https://developer.yahoo.com/fantasysports/guide/)
- [API](https://developer.yahoo.com/apps/OsZ6BS0Z/)

* What I'd like
- Setting draft order
- Pre draft ...
  - Identify player's whose names vary by expert site and create mapping
- In draft ...
  - tell me what positions have already been taken overall and by each team
  - tell me what position each team is likely to pick next
  - tell me what position i should take next based on prior selection and remaining availability
- In season ...
  - figure out the time in the evening / morning when players become available each week
  - predict what positions a team will need to draft
  - automate waiver selections 


* API notes
** Objects
- [Game](https://developer.yahoo.com/fantasysports/guide/#game-resource)
- [League](https://developer.yahoo.com/fantasysports/guide/#league-resource)
    - Settings
    - Standings
    - Scoreboard
- [Team](https://developer.yahoo.com/fantasysports/guide/#team-resource)
    - Matchups
    - Stats
- [Roster](https://developer.yahoo.com/fantasysports/guide/#roster-resource)
    - Filters: a given week
    - Players
    - Set lineups
- [Player](https://developer.yahoo.com/fantasysports/guide/#player-resource)
    - Filers: player ids
    - Stats
- [Transaction](https://developer.yahoo.com/fantasysports/guide/#transaction-resource)
    - Adds/Drops
    - Waiver claims
    - Pending trades
    - Change waiver priorities
    - Accpet/Reject trades
    - Allow/Disallow trades
    - Vote against trades
    - Cancel waiver claim 
    - Cancel proposed trade
- [User](https://developer.yahoo.com/fantasysports/guide/#user-resource)

** Collections
- [Games](https://developer.yahoo.com/fantasysports/guide/#games-collection)
- [Leagues](https://developer.yahoo.com/fantasysports/guide/#leagues-collection)
- [Teams](https://developer.yahoo.com/fantasysports/guide/#teams-collection)
- [Players](https://developer.yahoo.com/fantasysports/guide/#players-collection)
     - Filters: position, status, start, count, sort_type=season/week, sort_week
- [Transactions](https://developer.yahoo.com/fantasysports/guide/#transactions-collection)
    - Add/Drop players
    - Propose trades
- [User](https://developer.yahoo.com/fantasysports/guide/#users-collection)


* Auth

POST /oauth2/get_token HTTP/2
Host: api.login.yahoo.com
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
Authorization: Basic ZGoweUptazlibmxxV2xWaFlrWlhjV05hSm1ROVdWZHJPVlF6VG1GT2EwcFVUVVp2YldOSGJ6bE5RVDA5Sm5NOVkyOXVjM1Z0WlhKelpXTnlaWFFtYzNZOU1DWjRQVE5pOjY0NDQxODg0YTg1YzkwOGI0MjgyZDBhMmY2YWMxYzcyNjJiN2RhOTQ=
Content-Type: application/x-www-form-urlencoded
Content-Length: 221

code=742e6kh&redirect_uri=oob&grant_type=authorization_code&client_id=dj0yJmk9bnlqWlVhYkZXcWNaJmQ9WVdrOVQzTmFOa0pUTUZvbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTNi&client_secret=64441884a85c908b4282d0a2f6ac1c7262b7da94


HTTP/2 200 OK
Date: Fri, 02 Aug 2024 21:53:04 GMT
Cache-Control: no-store
Cache-Control: no-cache
Cache-Control: must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=15552000
Referrer-Policy: strict-origin-when-cross-origin
Content-Type: application/json
Content-Length: 1059
Server: ATS
Age: 0
Expect-Ct: max-age=31536000, report-uri="http://csp.yahoo.com/beacon/csp?src=yahoocom-expect-ct-report-only"

{"access_token":"50OleiWZuRkmZW3SE2clxDlA0Pw1MTbmpRVO0Tm10huMnJUswaPUcxpChj4G5c5aUg5DA9c2y3us_pilKM0x_HVIU4Ldv2zcyLYtVqE0Dk8E6k8c.39OXe35cP0hY4rydzowvrLmCljKYBoQhCXhSAZ0yPwoUPgucuc0UaA7FjXFekLfGoTjwBKD4oQkHD5kO11jyCnplJfYZKj.70ywI.fulKpP.9SVrSze2MQCcaJBYDemlcumlyRTDCCdvm1Qrg0Jlg9a1DI0vJwlVyeorG55mLnXykA1SUmynjvediczuB4rYgEJ4oAioAu4V01BBrqBEKGaWT7v5vRDR4q1G22nhScIF0qlFQTNwTqB0ZfA8NLY3Em3nMRIvk_FftpBsD6xa21IvvYTskHxJ9DvQCe63ptqiQaVDoIjlix0QQOGrLA_HgMuDyfYlYQOkjgok3GZvpDpbnXbMVCONdTf0jDWaaU4SOPpnO2WAM_9zY1QhCInOpCtjJ8igcIU8rghhZL6iboBP5W5N_vTmDkUThOocyuDs3..ulOVEJdmF6YEZTzTyqMgAgk7RIikeXXxp7Z5U3W8fIDRqS6MA.9ttAgUQsIe1MwBo1S6IjBOboJ.VeA2fWitzYAS3Y_iZVIoXsjx6TWw2laKRpwFoP3D.lUik5jXvvPq4DMOBCa_9YhXNvjgbqPdLKd4EDUR_czPAV4Tg8T4KJhZnEEEkFoUi725eoJEC9NVXoIFlpKZQ7DwIFQM8qLEKndks876oGrwFhxG5zgPEkIu8NAcyQJ2X0I7ABRRd9xqibl4NuN0bPUtHN76G3iI1jQH9KLntCaLPfluP.BEs0BqjsoVAZGbRWavkNOzbunzsfeN25FCr2A0VbplcSyASlVh_339IdrX2.mPFn275FG34vjC.oBOqRAJ7_v9TA--","refresh_token":"ALjV2mQMl7jC9y4Z6IUOR5fxT9ez~000~BJyoM6jB1CtddfGDF8g-","expires_in":3600,"token_type":"bearer"}

POST /oauth2/get_token HTTP/1.1
Host: api.login.yahoo.com
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
Authorization: Basic ZGoweUptazlibmxxV2xWaFlrWlhjV05hSm1ROVdWZHJPVlF6VG1GT2EwcFVUVVp2YldOSGJ6bE5RVDA5Sm5NOVkyOXVjM1Z0WlhKelpXTnlaWFFtYzNZOU1DWjRQVE5pOjY0NDQxODg0YTg1YzkwOGI0MjgyZDBhMmY2YWMxYzcyNjJiN2RhOTQ=
Content-Type: application/x-www-form-urlencoded
Content-Length: 271

refresh_token=ALjV2mQMl7jC9y4Z6IUOR5fxT9ez~000~BJyoM6jB1CtddfGDF8g-&redirect_uri=oob&grant_type=refresh_token&client_id=dj0yJmk9bnlqWlVhYkZXcWNaJmQ9WVdrOVQzTmFOa0pUTUZvbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTNi&client_secret=64441884a85c908b4282d0a2f6ac1c7262b7da94


HTTP/2 200 OK
Date: Fri, 02 Aug 2024 21:22:50 GMT
Cache-Control: no-store
Cache-Control: no-cache
Cache-Control: must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=15552000
Referrer-Policy: strict-origin-when-cross-origin
Content-Type: application/json
Content-Length: 1059
Server: ATS
Age: 0
Expect-Ct: max-age=31536000, report-uri="http://csp.yahoo.com/beacon/csp?src=yahoocom-expect-ct-report-only"

{"access_token":"8xamhkKZuRkoVNjChOyCunc8Dwoyp_3iwDeHGliQ4DZgZc4Sr7VXOTRv52EkhxxtZ9w.OO9ka.NmdyVy6IwLmbhHsNWd86Smqj6Ahm97BauJ3XMr7cqorzsjhvaZI3SODdjFQtRAZSOScU9AhtS5yssaDoWNhVOEwDY_AVbGkN_fTXKIYfcXCidCnZNIJI1Tv9smE_FC_3IFAKg7YgdNK87BBk8aeA1D9w0ffT5S6wn864NMh1eM7vFHGmbSS3oCcJOsq_k_GcValirs3ela9dhqrbwVysMjLUzZFyleS7pCu3BlnoZR7hmpgWZ584VAKAhVNPu_cHm1IQB3tE9Pfurms9_.Gt3ezlMm3CRir09KFRaNh4CTn4DzH.xn7HWateCOQUpQhNKm.4DMfPNSsKE20bQ93Dzcf9Szq1fEgjQqhDUtY7D10.Hx5WGXRPf5OeS8.og8PT15f9dMBIQOm91sUjfi7nme0bOeuFp3OhundFOWFU3OqfSC.tA2QXT2nu1QmVD60BSFoYsrHAiOXm218squxxDIxKd4vnsNUrGcbpwt.EjI7BQOlkK8mo0DuMXyiRelOmTW9.aZ9r.8XTAcwTQwPOn3QO2V5r2T1Wnw2bxdcpLYsp3hACSvYu06G8yHSLzL0cMBlF9r2obLaxsz8PtkYeCTICHZtMoOQ2uE0CCj5Tipo3gjAalIsRehzxOonxMR.bW1sMM4HTXmPr1zvdRgK.NF2AlHRNfSwDFKhk8YN3575I84UmjbVlZjeusYa4MqaUVb4h7lFlgWOO5__P7UgDR4HAqjPPW7nUbzHzb0QwjvyV4w4E4t_TIoyn0NYYymT2vwUmpgZH_8du_ZQk3SGyLLUSh5LPrico3waPZgMSTiTXgZcnU05Fu.vjPQSEwep69jCM1Pjb.XVkpEJ9360IA-","refresh_token":"ALjV2mQMl7jC9y4Z6IUOR5fxT9ez~000~BJyoM6jB1CtddfGDF8g-","expires_in":3600,"token_type":"bearer"}


*Games*
Get current season NFL teams
https://fantasysports.yahooapis.com/fantasy/v2/game/nfl




https://fantasysports.yahooapis.com/fantasy/v2/games;is_available=1



https://football.fantasysports.yahoo.com/f1/222481






#ROS\ Ranks\ Staging_7534 > table > tbody

document.querySelector("#ROS\\ Ranks\\ Staging_7534 > table > tbody")

//*[@id="ROS Ranks Staging_7534"]/table/tbody

/html/body/div/div[2]/section/div/div/div/div/div[2]/div[2]/div/div/div/table/tbody