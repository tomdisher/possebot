import requests
statsapi = "https://statsapi.web.nhl.com/api/v1/"

def find_team(name):
    teams = get_teams()
    key=next( (key for key in teams if name.lower() in key), None )
    return key
def get_teams():
    teams={}
    all_info=requests.get('https://statsapi.web.nhl.com/api/v1/teams/').json()
    for team in all_info['teams']:
        id=team['id']
        name=team['name'].lower()
        teams[name]=id
    return teams

def get_team_id(name):
    teams=get_teams()
    team_url='https://statsapi.web.nhl.com/api/v1/teams/'
    name = find_team(name)
    id = teams[name]
    return id

def get_team_info(name):
    id = get_team_id(name)
    team_url=team_url+str(id)
    print(team_url)
    result=requests.get(team_url).json()
    return result

def get_team_stats(name):
    id = get_team_id(name)
    all_info=requests.get('{}/teams/{}/stats'.format(statsapi, id)).json()['stats']
    return all_info
                          
def current_standings():
    teams={}
    all_info=requests.get('https://statsapi.web.nhl.com/api/v1/standings').json()
    return all_info

def get_scores(day=''):
    print("{}schedule?date={}".format(statsapi,day))
    result = requests.get("{}schedule?date={}".format(statsapi,day)).json()
    games = result['dates'][0]['games']
    for game in games:
        away="{} {}\n".format(game['teams']['away']['team']['name'], game['teams']['away']['score'])
        home="{} {}\n".format(game['teams']['home']['team']['name'], game['teams']['home']['score'])
        score=away+home
        print(score)
