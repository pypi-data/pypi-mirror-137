import json


class Message:
    header_size = 10

    def __init__(self, content=None, title=None, b_mess=None):
        self._dic = {}
        self._b_mess = b''

        if content is not None or title is not None:
            self._dic["content"] = content if content is not None else ""
            self._dic["title"] = title if title is not None else ""
            self._encode()
        else:
            self._decode(b_mess)

    def _create_header_msg(self):
        dumped_dict = json.dumps(self._dic) 
        len_msg = len(dumped_dict)
        header_msg = f"{len_msg}"

        while len(header_msg) < self.header_size:
            header_msg += " "
        return header_msg.encode('utf-8')

    def _encode(self):
        dumped_dict = json.dumps(self._dic) 
        self._b_mess = dumped_dict.encode("utf-8")

    def _decode(self, b_mess):
        self._dic = json.loads(b_mess.decode("utf-8"))
        self._b_mess = b_mess

    def get_b_mess(self):
        return self._b_mess

    def get_content(self):
        return self._dic["content"] 

    def get_title(self):
        return self._dic["title"]

    def get_dict(self):
        return self._dic

    def get_encoded_message(self):
        header_msg = self._create_header_msg()
        return header_msg + self._b_mess
