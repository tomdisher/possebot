import requests
import plugins
import os
from random import *
import emoji


def get_nhl_scores():
    all_games = ''
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
    return all_games


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
                logger.error(e)
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
