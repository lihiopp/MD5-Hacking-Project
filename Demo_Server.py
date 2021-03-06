import socket

class Server:

    def __init__(self,ip,port):
        self.socket = socket.socket()
        self.socket.bind((ip,port))
        self.socket.listen(1)
        self.clientSoc, self.addr = self.socket.accept()
        print("good")

    def recv(self):
        msg = self.clientSoc.recv(1024).decode()
        if(msg!="Howdy"):
            self.clientSoc.close() #wrong code word, close connection
        
        else:
            self.clientSoc.send("1".encode()) #sends id
            self.clientSoc.close() #closes main port, connects to the unique one
        
        self.socket.close()
        self.socket = socket.socket()
        self.socket.bind(("127.0.0.1",13370))
        port_addr = self.addr[1]+1
        self.socket.connect(("127.0.0.1",port_addr))

    def unique_connection(self):
        start="aaaaaaaa"
        stop="cccccccc"
        self.md5 = "c9e1a482c67069fc92cea8ca55327c01"
        self.socket.send((start + "," + stop + "," + self.md5).encode())
        
    def get_answer(self):
        answer = self.socket.recv(1024).decode()
        print(answer)
        found=answer.split(",")[1]
        if(found=="True"):
            self.socket.send(("finish," + self.md5).encode()) #sends finish


def main():
    server = Server("127.0.0.1",13370)
    server.recv()
    server.unique_connection()
    while(True):
        server.get_answer()

main()
