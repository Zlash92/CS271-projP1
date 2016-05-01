from __future__ import print_function
import socket
import replicated
from time_table import TimeTable
import sys
import threading
import pickle


class Server:
    def __init__(self, serverId=sys.argv[1], port=80):
        self.socket = socket.socket()
        self.host = socket.gethostname()
        self.socket.bind((self.host, port))
        self.data = replicated.ReplicatedDictionary()
        self.serverId = serverId
        self.timeTable = TimeTable(self.serverId, 3)
        self.threads = []

        self.initConnection()

    def initConnection(self):
        self.socket.listen(5)
        print("Server with id=", self.serverId, " is running and listening for incoming connections", sep="")

        while True:
            c, addr = self.socket.accept()
            print("Connected to", addr)
            c.send("Connection to server was successful")
            client = ClientHandler(c, addr, self)
            client.start()
            self.threads.append(client)

        self.socket.close()
        for client in self.threads:
            client.join()

    def post(self, msg, author):
        self.incrementTime()
        self.data.addPost(self.timeTable.get_self_clock(), msg, author)
        print("Post has been submitted at local time", self.timeTable.get_self_clock())

    def lookup(self, c):
        package = pickle.dumps(self.data)
        c.send(package)

    def sync(self, other):
        pass

    def incrementTime(self):
        self.timeTable.increment_self()

    def listen(self):
        self.socket.listen(5)
        print("Server with id=", self.serverId, " is running and listening for incoming connections", sep="")



class ClientHandler(threading.Thread):
    def __init__(self, client, address, parentServer):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.parentServer = parentServer

    def run(self):
        while True:
            recv = self.client.recv(1024)
            inp = recv.split(' ', 1)
            if recv == 'close':
                print("Closing client connection")
                self.client.close()
                break
            elif inp[0] == 'post':
                self.parentServer.post(inp[1], self.address)
            elif inp[0] == 'lookup':
                self.parentServer.lookup(self.client)
            elif inp[0] == 'sync':
                self.parentServer.sync()
            else:
                print("Received message:", recv)


server = Server(serverId=0, port=18869)
# Server()
