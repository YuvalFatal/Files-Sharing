import asyncore
import socket


class Client(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def handle_read(self):
        print self.recv(1024)

    def handle_write(self, data="3"):
        self.send(data)

    def handle_close(self):
        self.close()


def main(server_ip, port):
    client = Client(server_ip, port)
    asyncore.loop()

if __name__ == '__main__':
    main('127.0.0.1', 8080)