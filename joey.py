"""
example plugin which demonstrates user and conversation memory
"""

import plugins


def _initialise(bot):
    plugins.register_user_command(["joey"])


def joey(bot, event, *args):
    """remember value for current user, memory must be empty.
    use /bot forgetme to clear previous storage
    """
    question = ''.join(args).strip()
    print(event.user.__dict__)
    if "games" in question.lower():
        yield from bot.coro_send_message(
            event.conv,
            _("JOEY GETS LAID!").format(
                event.user.full_name, 'yay'))
    elif "wife" in question.lower() and "sister" in question.lower():
        yield from bot.coro_send_message(
            event.conv,
            _("Joey wife looks like sister :(").format(
                event.user.full_name, 'yay'))



