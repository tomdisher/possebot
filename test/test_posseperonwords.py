from unittest.mock import MagicMock,patch, mock_open
from unittest import mock
import sys, os
import unittest
import gettext

gettext.install('text_monitorwords', localedir=os.path.join(os.path.dirname(__file__), 'locale'))

plugins_mock = MagicMock()
sys.modules['plugins'] = plugins_mock
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import possepersonwords

miller_fake_yml="""
ferret:
  - Ferret message one
  - Ferret message two
keilbasa:
  - Kielbasa message one
  - Kielbasa message two
"""

joey_fake_yml="""
games:
  - Games message one
  - Games message two
sisterwife:
  - Sisterwife message one
  - Sisterwife message two
"""

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
        self.message_found=False
        
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_miller_returns_ferret(self, mock_open):
        args=("Does miller ferret often?")
        expected_messages=["Ferret message one","Ferret message two"]
        mock_open.side_effect = [
            mock.mock_open(read_data=miller_fake_yml).return_value
        ]
        for x in possepersonwords.miller(self.fake_bot, self.fake_event, args):
            if (x in expected_messages):
                self.message_found=True
        self.assertTrue(self.message_found)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_miller_returns_kielbasa(self, mock_open):
        args=("Does kielbasa often?")
        expected_messages=["Kielbasa message one","Kielbasa message two"]
        mock_open.side_effect = [
            mock.mock_open(read_data=miller_fake_yml).return_value
        ]
        for x in possepersonwords.miller(self.fake_bot, self.fake_event, args):
            if (x in expected_messages):
                self.message_found=True
        self.assertTrue(self.message_found)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_joey_returns_games(self, mock_open):
        args=("Does joey play games often?")
        expected_messages=["Games message one","Games message two"]
        mock_open.side_effect = [
            mock.mock_open(read_data=joey_fake_yml).return_value
        ]
        for x in possepersonwords.joey(self.fake_bot, self.fake_event, args):
            if (x in expected_messages):
                self.message_found=True
        self.assertTrue(self.message_found)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_joey_returns_sisterwife(self, mock_open):
        args=("Does joey have wife look like sister")
        expected_messages=["Sisterwife message one","Sisterwife message two"]
        mock_open.side_effect = [
            mock.mock_open(read_data=joey_fake_yml).return_value
        ]
        for x in possepersonwords.joey(self.fake_bot, self.fake_event, args):
            if (x in expected_messages):
                self.message_found=True
        self.assertTrue(self.message_found)

        
