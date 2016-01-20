import asyncore
import socket
import msvcrt
import sys


class Client(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.message = ""

    def handle_read(self):
        data = self.read_data()
        print data

    def handle_write(self):
        if msvcrt.kbhit():
            key = msvcrt.getch()

            if key == "\r" and len(self.message) != 0:
                self.send_data(self.message)
                self.message = ""
                print "\r"

            else:
                if key == "\b":
                    self.message = self.message[:-1]
                    key = "\b \b"
                else:
                    self.message += key

                sys.stdout.write(key)

    def send_data(self, data):
        self.send(str(len(data)).zfill(8) + data)

    def read_data(self):
        len_data = int(self.recv(8))
        return self.recv(len_data)

    def handle_close(self):
        self.close()


def main(server_ip, port):
    Client(server_ip, port)
    asyncore.loop()

if __name__ == '__main__':
    main('127.0.0.1', 8080)