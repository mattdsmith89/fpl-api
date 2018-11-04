import requests
import json

def overview_handler(event, context):
    url = 'https://fantasy.premierleague.com/drf/bootstrap-static'

    try:
        r = requests.get(url)
        result = r.json()

        gameweeks = list(map(
            lambda x: {
                'id': x['id'],
                'name': x['name'],
                'deadline': x['deadline_time']
            },
            result['events']
        ))

        players = list(map(
            lambda x: {
                'id': x['id'],
                'firstName': x['first_name'],
                'lastName': x['second_name'],
                'points': x['total_points'],
                'currentPrice': x['now_cost'],
                'teamId': x['team'],
                'gamesPlayed': result['next-event'] - 1, # TODO: calculate this?
                'minutes': x['minutes'],
                'dreamteam': x['in_dreamteam'],
                'position': next(filter(lambda y: y['id'] == x['element_type'], result['element_types']))['singular_name_short']
            },
            result['elements']
        ))

        teams = list(map(
            lambda x: {
                'id': x['id'],
                'name': x['name'],
                'code': x['short_name']
            },
            result['teams']
        ))

        statusCode = 200
        data = {
            'nextGameweek': result['next-event'],
            'gameweeks': gameweeks,
            'players': players,
            'teams': teams
        }
    except Exception as exp:
        statusCode = 503
        data = { 'message': exp }

    response = {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }

    return response

# def games_played(playerId):
#     url = 'https://fantasy.premierleague.com/drf/element-summary/%i' % (playerId)
#     r = requests.get(url)
#     result = r.json()

#     return len(list(filter(lambda x: x['minutes'] != 0, result['history'])))

resp = overview_handler(0, 0)
