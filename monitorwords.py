import plugins

def _initialise(bot):
    plugins.register_handler(_got_a_message, type="message", priority=50)

def _got_a_message(bot, event, command):
    if "merkle" in  event.text.lower():
        yield from bot.coro_send_message(
            event.conv,
            _("YOU SAID THE SECRET WORDDDDDD!!!").format(
                event.user.full_name, 'yay'))
