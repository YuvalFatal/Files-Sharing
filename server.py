import asyncore
import socket


class Handler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(1024)
        print data
        self.send(data)

    def handle_write(self, data="ERROR"):
        self.send(data)

    def handle_close(self):
        self.close()


class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        sock, addr = self.accept()
        Handler(sock)

def main(my_ip, port):
    server = Server(my_ip, port)
    asyncore.loop()

if __name__ == "__main__":
    main('127.0.0.1', 8080)