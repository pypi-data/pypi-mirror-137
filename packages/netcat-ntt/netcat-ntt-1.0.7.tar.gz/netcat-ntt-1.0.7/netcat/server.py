import sys
from .socket import Socket
from .message import Message
from threading import Thread
from .communicate_mode import CommunicateMode


class Server(Socket):
    def __init__(self, host, port):
        Socket.__init__(self, host, port) 
        
    def bind(self):
        self._socket.bind((self._host, self._port))
        self._socket.listen()

    def _printSysInfor(self, title='WARNING', content="Something's wrong here."):
        return f"[{title.upper()}] {content}"

    def _handle_client(self, socket):
        communicate_mode = CommunicateMode() 
        msg = self.receive(socket)
        func = communicate_mode.get_mode(msg)
        self.send(Message(title='confirm'), socket)
        msg = self.receive(socket)
        result = func(msg)
        self.send(Message(title='confirm', content=result), socket)
        msg = self.receive(socket)
        socket.close()

    def run(self):
        print(self._printSysInfor(title='start', content='sever is starting.'))
        self.bind()
        while True:
            socket, add = self._socket.accept()
            print(self._printSysInfor(title='connect', content=f'Connect to {add[0]}:{add[1]}'))
            thread = Thread(
                    target=self._handle_client, args=(socket, )
                    )
            thread.start()
            sys.exit(0)
