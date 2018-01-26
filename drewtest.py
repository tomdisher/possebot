"""
example plugin for testing
"""

import plugins


def _initialise(bot):
    plugins.register_user_command(["drewski"])


def drewski(bot, event, *args):
    """
    /bot drewski to call
    """
    print(event.user.__dict__)
    yield from bot.coro_send_message(
        event.conv,
        _("Why hello there " + event.user.full_name).format(
            event.user.full_name, 'yay'))
