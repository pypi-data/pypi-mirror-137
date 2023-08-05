import socket 
from abc import ABC, abstractmethod
from .message import Message


class Socket:
    def __init__(self, host, port):
        self._host = host 
        self._port = port 
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @abstractmethod
    def run(self):
        raise NotImplementedError("You must implement run method if you inherit Socket class.") 

    def send(self, message, socket):
        socket.send(message.get_encoded_message())

    @abstractmethod
    def receive(self, socket):
        header_msg = socket.recv(Message.header_size)
        len_msg = int(header_msg)
        msg = socket.recv(len_msg)
        message = Message(b_mess=msg)
        return message
    
