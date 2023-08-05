import unittest
from netcat.message import Message
from netcat.communicate_mode import CommunicateMode
import json


class CommunicateModeTest(unittest.TestCase):
    test_dict = {'host': '192.168.1.1', 'port': 1234, 'execute': 'test.txt', 'send': None}
    test_message = Message(title="mode", content=json.dumps(test_dict))

    def assertMessage(self, message1, message2):
        self.assertEqual(message1.get_title(), message2.get_title())
        self.assertEqual(message1.get_content(), message2.get_content())

    def test_set_mode(self):
        communicate_mode = CommunicateMode()
        _, message = communicate_mode.set_mode(self.test_dict)
        self.assertMessage(message, Message(b_mess=self.test_message.get_b_mess()))
        self.assertDictEqual(communicate_mode.get_args(), self.test_dict)

    def test_get_mode(self):
        communicate_mode = CommunicateMode()
        _ = communicate_mode.get_mode(self.test_message)
        self.assertDictEqual(communicate_mode.get_args(), self.test_dict)
