import requests
import plugins
import os
from random import *
import emoji
import pprint
import json
from nhlbot import *


def format_stats(stats):
    output = ''
    for key, value in stats.items():
        output += "{} : {}\n".format(str(key), str(value))

    return output


def get_meekle_stats():
    os_dropped = randint(1, 10)
    shirts_off = randint(1, 50)
    seinfelds_watched = randint(1, 2000)
    spillzones = randint(1, 500)
    petite_redheads = randint(1, 150)

    result = """Os dropped: {}\n Shirts Off: {}
Seinfelds Watched: {}\n Spillzones: {}
Petite Redheads: {}\n""".format(os_dropped,
                                shirts_off,
                                seinfelds_watched,
                                spillzones,
                                petite_redheads)
    return result


def get_joeyboy_stats():
    woman_wooed = randint(1, 10)
    mountain_mommas = randint(1, 200)
    sister_mommas = randint(1, 100)
    thottsexckx = randint(1, 10)
    result = """Women wooed: {}\n Mountain Mommas: {}
SisterMommas: {}\n thottsexckx: {}\n""".format(
        woman_wooed, mountain_mommas,
        sister_mommas,
        thottsexckx)
    return result


def get_nhl_scores():
    all_games = ''
    try:
        result = requests.get(
            "https://statsapi.web.nhl.com/api/v1/schedule").json()
        games = result['dates'][0]['games']
        for game in games:
            away = "{} {}\n".format(
                game['teams']['away']['team']['name'],
                game['teams']['away']['score'])
            home = "{} {}\n".format(
                game['teams']['home']['team']['name'],
                game['teams']['home']['score'])
            score = away+home
            all_games += score + '\n'
    except IndexError:
        all_games = 'No games scheduled for today'
    return all_games


def get_nhl_team_stats(name):
    result = format_stats(get_team_stats(
        name)['stats'][0]['splits'][0]['stat'])
    result += format_stats(get_team_stats(name)
                           ['stats'][1]['splits'][0]['stat'])
    return result


def aoe_times():
    play_times = ["8pm", "9pm", "10pm", "now"]
    random_index = randrange(len(play_times)-1)
    return play_times[random_index]


def _initialise(bot):
    plugins.register_handler(_got_a_message, type="message",
                             priority=50)


def _got_a_message(bot, event, command):
    if "joeyfluff" in event.text.lower():
        yield from bot.coro_send_message(
            event.conv,
            _("YOU SAID THE SECRET WORDDDDDD {}!!!").format(
                event.user.full_name, 'yay'))
    elif event.text.lower() == "tom bomb":
        yield from bot.coro_send_message(
            event.conv,
            _('Gary actually made the tom bomb. {}'.format(
                emoji.emojize(':poop::poop::poop::poop::poop::poop:' +
                              ':poop::poop::poop::poop::poop::poop:' +
                              ':poop::poop::poop:', use_aliases=True))))
    elif event.text.lower() == 'when palooza':
        yield from bot.coro_send_message(
            event.conv,
            _('Toomie picked May 28!'))
    elif event.text.lower() == 'when aoe':
        yield from bot.coro_send_message(
            event.conv,
            _(aoe_times()))
    elif event.text.lower() == 'where palooza':
        yield from bot.coro_send_message(
            event.conv,
            _("I believe it is Miller's turn to pick"))
    elif event.text.lower() == 'where miller kielbasa':
        yield from bot.coro_send_message(
            event.conv,
            _("Oh, its somewhere you don't wanna know.... :-;"))
    elif event.text.lower() == 'how many socks':
        yield from bot.coro_send_message(
            event.conv,
            _("Meekle uses %s socks" % randint(1, 100)))
    elif event.text.lower() == 'how many kielbasa':
        yield from bot.coro_send_message(
            event.conv,
            _("Miller scarfs down %s kielbasa" % randint(1, 100)))
    elif "!nhl" in event.text.lower():
        action = event.text.lower().split('!nhl ')[1]
        if action.lower() == 'scores':
            text = get_nhl_scores()
            yield from bot.coro_send_message(
                event.conv,
                _(text))
        elif action.startswith('stats'):
            try:
                print(action)
                team = action.split('stats ')[1]
                print('Getting team {}'.format(team))
                result = get_nhl_team_stats(team)
                yield from bot.coro_send_message(
                    event.conv,
                    _(result))
            except Exception as e:
                print(e)
                yield from bot.coro_send_message(
                    event.conv,
                    _('Please pass team name {}'.format(e)))
    elif "!stats" in event.text.lower():
        person = event.text.lower().split('!stats ')[1]
        if person.lower() == 'joeyboy':
            text = get_joeyboy_stats()
            yield from bot.coro_send_message(
                event.conv,
                _(text))
        if person.lower() == 'meekle':
            text = get_meekle_stats()
            yield from bot.coro_send_message(
                event.conv,
                _(text))

    elif "!joeyboy" in event.text.lower():
        # <-- absolute dir the script is in
        from random import randrange
        random_index = randrange(0, 3)
        if random_index == 2:
            try:
                site_url = bot.get_config_option('posseimage_url')
                instanceImageUrl = site_url+'/joey/jodyboy.jpg'
                photo_id = yield from bot.call_shared('image_upload_single',
                                                      instanceImageUrl)
                yield from bot.coro_send_message(event.conv.id_, '',
                                                 image_id=photo_id)
            except Exception as e:
                print(e)
   
        else:
            script_dir = os.path.dirname(__file__)
            rel_path = "joeyboy.txt"
            joeyboywords_path = os.path.join(script_dir, rel_path)
            words = open(joeyboywords_path, 'r')
            words = words.read()
            words = words.splitlines()
            random_index = randrange(0, len(words))
            random_word = words[random_index]
            yield from bot.coro_send_message(
                event.conv,
                _(random_word))
