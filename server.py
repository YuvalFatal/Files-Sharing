import asyncore
import socket
import time
import random
import threading


class Handler(asyncore.dispatcher_with_send):
    semaphore_thread = threading.Semaphore(10)

    def send_data_test(self, data):
        sleep = random.SystemRandom().randint(0, 10)
        time.sleep(sleep)
        self.send_data("Slept " + str(sleep) + " - " + data)

    def handle_read(self):
        data = self.read_data()
        print data

        Handler.semaphore_thread.acquire()
        threading.Thread(target=self.send_data_test, args=data).start()
        Handler.semaphore_thread.release()

    def handle_write(self):
        self.send_data("")

    def send_data(self, data):
        self.send(str(len(data)).zfill(8) + data)

    def read_data(self):
        len_data = int(self.recv(8))
        return self.recv(len_data)

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
    Server(my_ip, port)
    asyncore.loop()

if __name__ == "__main__":
    main('127.0.0.1', 8080)