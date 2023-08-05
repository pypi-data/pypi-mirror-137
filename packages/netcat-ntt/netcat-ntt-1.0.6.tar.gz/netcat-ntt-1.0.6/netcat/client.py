from .message import Message
from .communicate_mode import CommunicateMode
from .socket import Socket


class Client(Socket):
    def __init__(self, host, port, args):
        Socket.__init__(self, host, port)
        self._mode = CommunicateMode()
        self._args = args

    def connect(self):
        self._socket.connect((self._host, self._port))

    def run(self):
        func, mode_mess = self._mode.set_mode(self._args)
        self.connect()
        self.send(mode_mess, self._socket)
        confirm_mess = self.receive(self._socket)

        assert confirm_mess.get_title() == "confirm"

        self.send(func(self._args), self._socket)
        msg = self.receive(self._socket)
        if self._args['result']:
            print(msg.get_content())

        self.send(Message(title='quit'), self._socket)
