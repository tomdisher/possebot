"""
plugin to return random meekle image
"""

import plugins
import urllib.request
import os
import base64
import hangups
import logging
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from random import randrange

logger = logging.getLogger(__name__)
members = ["joey", "meekle", "toomie", "gary",
           "alex", "miller", "bizic", "drewski", "keener"]


def sanitize_possemember(person):
    if not person:
        random_index = randrange(0, len(members))
        return members[random_index]
    return process.extractOne(person, members)[0]


def _initialise(bot):
    plugins.register_user_command(["possepic"])


def get_url(link):
    try:
        response = urllib.request.urlopen(link)
    except urllib.error.HTTPError as e:
        module_name = 'possepersonpicture'
        logger.error(link)
        logger.error('Error getting {} in {}.  {}'.format(link,
                                                          module_name, e))
        return ''
    return response


def get_image_list(link):
    response = get_url(link)
    if response == '':
        return []
    data = response.read()
    text = data.decode('utf-8')
    soup = BeautifulSoup(text, "html.parser")
    images = soup.find_all('a', href=True)
    images = [x for x in images if x.text != '../']
    return images


def get_member_url(bot, dirty_member):
    site_url = bot.get_config_option('posseimage_url')
    sanitized_member = sanitize_possemember(dirty_member)
    link = site_url+sanitized_member+"/"
    return link


def possepic(bot, event, *args):
    dirty_member = ''.join(args).strip()
    link = get_member_url(bot, dirty_member)
    images = get_image_list(link)

    if len(images) > 0:
        random_index = randrange(0, len(images))
        image_name = images[random_index]['href']
        instanceImageUrl = link+image_name
        image_data = get_url(instanceImageUrl)
        filename = os.path.basename(instanceImageUrl)
        legacy_segments = [hangups.ChatMessageSegment(
            instanceImageUrl,
            hangups.SegmentType.LINK,
            link_target=instanceImageUrl)]
        logger.debug("uploading {} from {}".format(filename, instanceImageUrl))

        try:
            photo_id = yield from bot.call_shared('image_upload_single',
                                                  instanceImageUrl)
        except KeyError:
            logger.warning('image plugin not loaded - using legacy code')
            photo_id = yield from bot._client.upload_image(image_data,
                                                           filename=filename)
        except Exception as e:
            message = "So sorry. Unable to upload image. Tell admins"
            logger.error(e)
            yield from bot.coro_send_message(
                event.conv,
                _(message))

        try:
            yield from bot.coro_send_message(event.conv.id_, '',
                                             image_id=photo_id)
        except Exception as e:
            message = "So sorry. Unable to upload image. Tell admins"
            logger.error(e)
            yield from bot.coro_send_message(
                event.conv,
                _(message))

    else:
        yield from bot.coro_send_message(
            event.conv,
            _("No images uploaded yet for %s" % dirty_member).format(
                event.user.full_name, 'yay'))
