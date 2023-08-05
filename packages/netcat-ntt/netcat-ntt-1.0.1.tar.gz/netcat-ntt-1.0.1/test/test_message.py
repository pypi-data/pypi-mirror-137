from netcat.message import Message
import unittest
import json


standard = "utf-8"


class MessageTest(unittest.TestCase):
    expected_msg = "Hello, Bro"
    expected_title = "greedy"
    expected_bin_str_10 = ("44        " + json.dumps({"content": expected_msg, "title": expected_title})).encode(standard)
    expected_bin_str_10_no = (json.dumps({"content": expected_msg, "title": expected_title})).encode(standard)
    expected_bin_str_8 = ("44      " + json.dumps({"content": expected_msg, "title": expected_title})).encode(standard) 
    expected_bin_str_8_no = (json.dumps({"content": expected_msg, "title": expected_title})).encode(standard) 

    def test_get_content(self):
        # exact initial form
        test_message = Message(title=self.expected_title, content=self.expected_msg)
        self.assertEqual(self.expected_msg, test_message.get_content())

        # missing msg property
        test_message = Message(title=self.expected_title)
        self.assertEqual("", test_message.get_content())

        test_message = Message(title=self.expected_title, b_mess=self.expected_bin_str_10_no)
        self.assertEqual("", test_message.get_content())

        # using all properties
        test_message = Message(title=self.expected_title, content=self.expected_msg, b_mess=self.expected_bin_str_10_no)
        self.assertEqual(self.expected_msg, test_message.get_content())

        # using only b_mess
        test_message = Message(b_mess=self.expected_bin_str_10_no)
        self.assertEqual(self.expected_msg, test_message.get_content())

        Message.header_size = 8
        test_message = Message(b_mess=self.expected_bin_str_8_no)
        self.assertEqual(self.expected_msg, test_message.get_content())

    def test_get_title(self):
        # exact initial form
        test_message = Message(title=self.expected_title, content=self.expected_msg)
        self.assertEqual(self.expected_title, test_message.get_title())

        # missing msg_type property 
        test_message = Message(content=self.expected_msg)
        self.assertEqual("", test_message.get_title())

        test_message = Message(content=self.expected_msg, b_mess=self.expected_bin_str_10_no)
        self.assertEqual("", test_message.get_title())

        # using all properties
        test_message = Message(title=self.expected_title, content=self.expected_msg, b_mess=self.expected_bin_str_10_no)
        self.assertEqual(self.expected_title, test_message.get_title())

        # using only b_mess
        test_message = Message(b_mess=self.expected_bin_str_10_no)
        self.assertEqual(self.expected_title, test_message.get_title())

        Message.header_size = 8
        test_message = Message(b_mess=self.expected_bin_str_8_no)
        self.assertEqual(self.expected_title, test_message.get_title())

    def test_get_encoded_message(self):
        # exact initial form
        Message.header_size = 10
        test_message = Message(title=self.expected_title, content=self.expected_msg)
        self.assertEqual(self.expected_bin_str_10, test_message.get_encoded_message())

        # using only b_mess
        test_message = Message(b_mess=self.expected_bin_str_10_no)
        self.assertEqual(self.expected_bin_str_10, test_message.get_encoded_message())

        Message.header_size = 8
        test_message = Message(b_mess=self.expected_bin_str_8_no)
        self.assertEqual(self.expected_bin_str_8, test_message.get_encoded_message())
