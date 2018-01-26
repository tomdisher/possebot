"""
example plugin which demonstrates user and conversation memory
"""

import plugins,os,yaml

def random_word(list):
    from random import randrange
    random_index = randrange(0,len(list))
    random_word = list[random_index]
    return random_word

def _initialise(bot):
    plugins.register_user_command(["miller"])
    plugins.register_user_command(["joey"])


def miller(bot, event, *args):
    """remember value for current user, memory must be empty.
    use /bot forgetme to clear previous storage
    """
    question = ''.join(args).strip()
    print(event.user.__dict__)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "millerwords.yml"
    millerwords_path = os.path.join(script_dir, rel_path)
    with open(millerwords_path, 'r') as stream:
        try:
            content = (yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    print(content)
    if "ferret" in question:
        words = content['ferret']
        word = random_word(words)
        yield from bot.coro_send_message(
            event.conv,
            _(word).format(
                event.user.full_name, 'yay'))

    if "keilbasa" in question:
        words = content['keilbasa']
        word = random_word(words)
        yield from bot.coro_send_message(
            event.conv,
            _(word).format(
                event.user.full_name, 'yay'))


def joey(bot, event, *args):
    """remember value for current user, memory must be empty.
    use /bot forgetme to clear previous storage
    """
    question = ''.join(args).strip()
    print(event.user.__dict__)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "joeywords.yml"
    joeywords_path = os.path.join(script_dir, rel_path)
    with open(joeywords_path, 'r') as stream:
        try:
            content = (yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    print(content)
    if "games" in question:
        words = content['games']
        word = random_word(words)
        yield from bot.coro_send_message(
            event.conv,
            _(word).format(
                event.user.full_name, 'yay'))

    elif "wife" in question.lower() and "sister" in question.lower():
        words = content['sisterwife']
        word = random_word(words)
        yield from bot.coro_send_message(
            event.conv,
            _(word).format(
                event.user.full_name, 'yay'))
