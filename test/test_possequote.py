from unittest.mock import MagicMock,patch, mock_open
from unittest import mock
import sys, os
import unittest
import gettext

gettext.install('text_monitorwords', localedir=os.path.join(os.path.dirname(__file__), 'locale'))

plugins_mock = MagicMock()
fuzzywuzzy_mock = MagicMock()
sys.modules['plugins'] = plugins_mock
sys.modules['fuzzywuzzy'] = fuzzywuzzy_mock
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import possequote

class FakeBot:
    def coro_send_message(self,  fake_conv, message):
        yield message

class FakeUser:
    full_name=''

class FakeConv:
    id_ = ''
class FakeEvent:
    text = ''
    conv=''
    user = ''


fake_quotes="""
Quote one
Quote two
Quote three
"""
class MonitorWordsTestCase(unittest.TestCase):
    def setUp(self):
        self.fake_bot = FakeBot()
        self.fake_event = FakeEvent()
        self.fake_user = FakeUser()
        self.fake_event.user = self.fake_user
        self.message_found=False
        self.fake_conv = FakeConv()

    @patch("builtins.open", new_callable=mock_open, read_data="data")    
    def test_add_possequote(self, mock_open):
        possequote.sanitize_command = MagicMock(return_value='add')
        args=("add This is a test quote")
        self.fake_event.user.full_name='merklepants'
        expected_message="'This is a test quote' has been to the posse archive"

        for x in possequote.possequote(self.fake_bot, self.fake_event, args):
            if(x == expected_message):
                self.message_found=True
        self.assertTrue(self.message_found)
        
        
    @patch("builtins.open", new_callable=mock_open, read_data="data")    
    def test_get_possequote(self, mock_open):
        self.fake_conv.id_=1234
        self.fake_event.conv = self.fake_conv
        possequote.sanitize_command = MagicMock(return_value='')
        args=("add This is a test quote")
        self.fake_event.user.full_name='merklepants'
        expected_messages=['Quote one', 'Quote two', 'Quote three']
        mock_open.side_effect = [
            mock.mock_open(read_data=fake_quotes).return_value
        ]
        for x in possequote.possequote(self.fake_bot, self.fake_event, args):
            if(x in expected_messages):
                self.message_found=True
        self.assertTrue(self.message_found)
        
