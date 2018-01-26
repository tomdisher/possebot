import plugins, os

def _initialise(bot):
    plugins.register_handler(_got_a_message, type="message", priority=50)

def _got_a_message(bot, event, command):
    if "merkle" in  event.text.lower():
        yield from bot.coro_send_message(
            event.conv,
            _("YOU SAID THE SECRET WORDDDDDD!!!").format(
                event.user.full_name, 'yay'))
    elif "!joeyboy" in event.text.lower():
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "joeyboy.txt"
        joeyboywords_path = os.path.join(script_dir, rel_path)
        words = open(joeyboywords_path, 'r')
        words = words.read()
        words = words.splitlines()
        from random import randrange
        random_index = randrange(0,len(words))
        random_word = words[random_index]
        yield from bot.coro_send_message(
            event.conv,
            _(random_word).format(
                event.user.full_name, 'yay'))
