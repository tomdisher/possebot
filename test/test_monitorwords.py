from unittest.mock import MagicMock
import sys, os
import unittest
import gettext
gettext.install('text_monitorwords', localedir=os.path.join(os.path.dirname(__file__), 'locale'))

plugins_mock = MagicMock()
sys.modules['plugins'] = plugins_mock
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import monitorwords

class FakeBot:
    def coro_send_message(self,  fake_conv, message):
        yield message

class FakeUser:
    full_name=''
    
class FakeEvent:
    text = ''
    conv=''
    user = ''
    
    
class MonitorWordsTestCase(unittest.TestCase):
    def setUp(self):
        self.fake_bot = FakeBot()
        self.fake_event = FakeEvent()
        self.fake_user = FakeUser()
        self.fake_event.user = self.fake_user
        
    def test_merkle_found(self):
        self.fake_event.user.full_name='merklepants'
        bomb_message='💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩'
        message_found=False
        self.fake_event.text = 'tom bomb'
        for x in  monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(bomb_message == x):
                message_found=True
        self.assertTrue(message_found)
        

    
