from unittest.mock import MagicMock,patch, mock_open
from unittest import mock
import sys, os
import unittest
import gettext

gettext.install('text_monitorwords', localedir=os.path.join(os.path.dirname(__file__), 'locale'))
fuzzywuzzy_mock = MagicMock()
plugins_mock = MagicMock()
sys.modules['plugins'] = plugins_mock
sys.modules['fuzzywuzzy'] = fuzzywuzzy_mock
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import possepersonpicture

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

    def get_config_option(self ,url):
        return 'http://test.com'

    def call_shared(self, image_data, filename):
        return "called with {} and {}".format(image_data, filename)

    def coro_send_message(self, id_, legacy_segments):
        return "called with {} and {}".format(id_, legacy_segments)
    
class FakeUser:
    full_name=''

class FakeEvent:
    text = ''
    conv=''
    user = ''

class FakeConv:
    id_ = ''

class FakeData:
    def decode(self, string):
        return "<a href='http://test.com'>test link</a>"
    def read(self):
        return  FakeData()
    
class MonitorWordsTestCase(unittest.TestCase):
    def setUp(self):
        self.fake_bot = FakeBot()
        self.fake_event = FakeEvent()
        self.fake_user = FakeUser()
        self.fake_event.user = self.fake_user
        self.fake_conv = FakeConv()
        self.message_found=False

    @patch('urllib.request.urlopen')
    def test_get_image_list(self, mock_urlopen):
        mock_urlopen.return_value = FakeData()
        result = possepersonpicture.get_image_list('http://test.com')
        self.assertEqual('http://test.com', (result[0]['href']))

    @patch('possepersonpicture.sanitize_possemember')
    def test_dirty_member_url(self, mock_sanitize):
        fake_bot = MagicMock()
        test_site='http://meekle.com/images/'
        fake_bot.get_config_option.return_value=test_site
        mock_sanitize.return_value='merklemeister'
        mock_bot = MagicMock()
        possepersonpicture.bot = mock_bot
        mock_bot.get_config_option.return_value = test_site
        result = possepersonpicture.get_member_url(fake_bot,'merklemeister')
        self.assertEqual(test_site+'merklemeister'+'/', result)
    
    def test_sanitize_posse_member_finds_member(self):
        possepersonpicture.process.extractOne.return_value=['miller']
        result = possepersonpicture.sanitize_possemember('millller')
        self.assertEqual('miller', result)
     
    def test_sanitize_posse_member_finds_random_member(self):
        result = possepersonpicture.sanitize_possemember('')
        self.assertTrue(len(result)>1)
        
