import requests
statsapi = "https://statsapi.web.nhl.com/api/v1/"
def get_scores(day=''):
    print("{}schedule?date={}".format(statsapi,day))
    result = requests.get("{}schedule?date={}".format(statsapi,day)).json()
    games = result['dates'][0]['games']
    for game in games:
        away="{} {}\n".format(game['teams']['away']['team']['name'], game['teams']['away']['score'])
        home="{} {}\n".format(game['teams']['home']['team']['name'], game['teams']['home']['score'])
        score=away+home
        print(score)
