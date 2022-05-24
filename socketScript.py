import socket

class NewSocket:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self, host):
        self.__socket.connect((host, 1051))
    
    def SocketSend(self, msg):
        sent = self.__socket.send(msg.encode("ASCII"))
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def SocketReceive(self):
        return self.__socket.recv(1024).decode("ASCII")
        '''
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.__socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
        '''
