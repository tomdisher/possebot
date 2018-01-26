"""
example plugin which demonstrates user and conversation memory
"""

import plugins


def _initialise(bot):
    plugins.register_user_command(["miller"])


def miller(bot, event, *args):
    """remember value for current user, memory must be empty.
    use /bot forgetme to clear previous storage
    """
    question = ''.join(args).strip()
    print(event.user.__dict__)
    if "ferret" in question:
        yield from bot.coro_send_message(
            event.conv,
            _("You know he is one,  " + event.user.full_name).format(
                event.user.full_name, 'yay'))

    if "keilbasa" in question:
        yield from bot.coro_send_message(
            event.conv,
            _("All I know is that he eats is every chance he gets").format(
                event.user.full_name, 'yay'))
