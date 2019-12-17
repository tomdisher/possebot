"""
plugin to return random posse quote
"""

import urllib.request
import os
import logging
import hangups
import plugins
import requests
import json
from requests.auth import HTTPBasicAuth
from fuzzywuzzy import process

logger = logging.getLogger(__name__)
commands = ["add"]
_internal = {}


def sanitize_command(command):
    sanitized = process.extractOne(command, commands)
    if sanitized[1] == 0:
        sanitized = ''
    else:
        return sanitized[0]


def get_auth():
    return HTTPBasicAuth(_internal['posseapi_user'], _internal['posseapi_pass'])


def _initialise(bot):
    plugins.register_user_command(["possequote"])
    api_user = bot.get_config_option('posseapi_user')
    api_pass = bot.get_config_option('posseapi_pass')
    api_url = bot.get_config_option('posseapi_url')
    if api_user:
        _internal['posseapi_user'] = api_user
    if api_pass:
        _internal['posseapi_pass'] = api_pass
    if api_url:
        _internal['posseapi_url'] = api_url


def possequote(bot, event, *args):
    dirty_command = ''.join(args).strip().lower()
    sanitized_command = sanitize_command(dirty_command)
    auth = get_auth()
    api_url = _internal['posseapi_url']
    api_url = api_url+'/possequote'
    if sanitized_command == "add":
        try:
            quote = ' '.join(args).partition(" ")[2]
            logger.info("quote to add is : {}".format(quote))
            payload = {'quote': quote}
            requests.post(api_url, auth=auth, data=json.dumps(payload))
            logger.info("payload is '{}'".format(payload))
            logger.info("quote '{}' has been added by {}".format(
                quote, event.user.full_name))
            yield from bot.coro_send_message(
                event.conv,
                _("'" + quote + "' has been to the posse archive"))
        except Exception as e:
            logger.error('error with possequote: {}'.format(e))
            yield from bot.coro_send_message(
                event.conv.id_,
                _("Something horrible has happened!!!!"))
    else:
        quote = requests.get(api_url)
        quote = quote.json()[1]
        yield from bot.coro_send_message(
            event.conv.id_,
            _(quote))
