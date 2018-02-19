

import plugins
import os
from random import *
import emoji


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
            _('I believe it is Toomie\'s turn to pick'))
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
    elif "!joeyboy" in event.text.lower():
        # <-- absolute dir the script is in
        script_dir = os.path.dirname(__file__)
        rel_path = "joeyboy.txt"
        joeyboywords_path = os.path.join(script_dir, rel_path)
        words = open(joeyboywords_path, 'r')
        words = words.read()
        words = words.splitlines()
        from random import randrange
        random_index = randrange(0, len(words))
        random_word = words[random_index]
        yield from bot.coro_send_message(
            event.conv,
            _(random_word))
