"""
plugin to return random meekle image
"""

import plugins
import urllib.request
import os
import hangups
import logging

logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["meeklepic"])


def meeklepic(bot, event, *args):
    link = "http://funny.drewstud.com/meekle/meeklelist.txt"
    response = urllib.request.urlopen(link)
    data = response.read()
    text = data.decode('utf-8')
    images=text.splitlines()
    images = [x for x in images if x]
    
    from random import randrange
    random_index = randrange(0,len(images))
    image_name = images[random_index]
    instanceImageUrl = "http://funny.drewstud.com/meekle/"+image_name
    image_data = urllib.request.urlopen(instanceImageUrl)
    filename = os.path.basename(instanceImageUrl)
    legacy_segments = [hangups.ChatMessageSegment( instanceImageUrl,
                                                   hangups.SegmentType.LINK,
                                                   link_target = instanceImageUrl )]
    logger.debug("uploading {} from {}".format(filename, instanceImageUrl))

    try:
        photo_id = yield from bot.call_shared('image_upload_single', instanceImageUrl)
    except KeyError:
        logger.warning('image plugin not loaded - using legacy code')
        photo_id = yield from bot._client.upload_image(image_data, filename=filename)

    yield from bot.coro_send_message(event.conv.id_, legacy_segments, image_id=photo_id)



