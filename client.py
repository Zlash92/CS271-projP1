from __future__ import print_function
import socket
import replicated
import pickle

class Client:

    def __init__(self, host, port=80):
        print("Setting up client")
        self.s = socket.socket()
        self.connect_to_server(host, port)

    def connect_to_server(self, host, port):
        connection = False
        print("Connecting to server")

        try:
            self.s.connect((host, port))
            connection = True

        except:
            print('Unable to connect to server')
            self.s.close()

        if connection:
            # Receive no more than 1024 bytes
            print(self.s.recv(1024))

            while True:
                msg = raw_input('Enter message: ')
                if msg == 'close':
                    self.s.send(msg)
                    break

                elif msg == 'lookup':
                    self.s.send(msg)
                    recv = s.recv(1024)
                    blog = pickle.loads(recv)
                    blog.show_posts()
                self.s.send(msg)
        self.s.close()


# c = Client(host='128.111.43.37', port=12353)
c = Client(host=socket.gethostname(), port=18874)