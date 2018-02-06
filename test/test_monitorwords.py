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
        self.message_found=False
        
    def test_tom_bomb_found(self):

        bomb_message='Gary actually made the tom bomb. 💩💩💩💩💩💩💩💩💩💩💩💩💩💩💩'
        self.fake_event.text = 'tom bomb'
        for x in  monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            print(x)
            if(bomb_message == x):
                self.message_found=True
        self.assertTrue(self.message_found)

    def test_merkle_found(self):
        self.fake_event.text='merkle'
        self.fake_event.user.full_name='merklepants'
        merkle_message="YOU SAID THE SECRET WORDDDDDD {}!!!".format(self.fake_event.user.full_name)
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(merkle_message == x):
               self.message_found=True
        self.assertTrue(self.message_found)

    def test_when_palooza_found(self):
        self.fake_event.text='when palooza'
        expected_message='Feb 9-11'
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(expected_message == x):
               self.message_found=True
        self.assertTrue(self.message_found)

    def test_where_palooza_found(self):
        self.fake_event.text='where palooza'
        expected_message="I believe it is Miller's turn to pick"
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(expected_message == x):
               self.message_found=True
        self.assertTrue(self.message_found)

    def test_where_miller_keilbasa_found(self):
        self.fake_event.text='where miller kielbasa'
        expected_message="Oh, its somewhere you don't wanna know.... :-;"
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(expected_message == x):
               self.message_found=True
        self.assertTrue(self.message_found)

    def test_how_many_socks_found(self):
        self.fake_event.text='how many socks'
        expected_message="Meekle uses"
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(expected_message in x):
               self.message_found=True
        self.assertTrue(self.message_found)

    def test_how_many_kielbasa_found(self):
        self.fake_event.text='how many kielbasa'
        expected_message="Miller scarfs down"
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(expected_message in x):
               self.message_found=True
        self.assertTrue(self.message_found)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_joeyboy_found(self, mock_open):
        self.fake_event.text='!joeyboy'
        expected_messages=["Joeyboy loves things!","Joeyboy eats veggies!"]
        mock_open.side_effect = [
            mock.mock_open(read_data="Joeyboy eats veggies!").return_value,
            mock.mock_open(read_data="Joeyboy loves things!").return_value
        ]
        for x in monitorwords._got_a_message(self.fake_bot, self.fake_event, 'nocommand'):
            if(x in expected_messages):
               self.message_found=True
        self.assertTrue(self.message_found)
    
        
