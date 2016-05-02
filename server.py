from __future__ import print_function
import socket
import replicated
from time_table import TimeTable
import sys
import threading
import pickle
import atexit


class Server:
    def __init__(self, server_id=sys.argv[1], port=80):
        self.socket = socket.socket()
        self.host = socket.gethostname()
        self.socket.bind((self.host, port))
        self.data = replicated.ReplicatedDictionary()
        self.log = replicated.ReplicatedLog()
        self.server_id = server_id
        self.time_table = TimeTable(self.server_id, 3)
        self.threads = []
        self.run = True

        self.init_connection()

    def init_connection(self):
        self.socket.listen(5)
        print("Server with id=", self.server_id, " is running and listening for incoming connections", sep="")

        while self.run:
            close = raw_input("Close server? y/n")
            if close == "y":
                break
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
        self.increment_time()
        entry = replicated.Entry(msg, author, self.time_table.get_self_clock())
        self.data.add_post(entry)
        self.log.addEntry(entry)
        print("Post has been submitted at local time", self.time_table.get_self_clock())

    def lookup(self, c):
        package = pickle.dumps(self.data)
        c.send(package)

    def sync(self, other):
        # TODO: Receive time table and log from other server
        other_time_table = None
        other_log = None

        for e in other_log:
            if e not in self.data:
                self.data.add_post(e)
                self.log.addEntry(e)

        self.time_table.sync_tables(other_time_table)

    # Compiles log to send when receiving sync message
    def compile_log(self):
        subLog = []
        # TODO: server_id of recipient
        other_server_id = None
        for e in self.log:
            # The id of server where entry was first posted
            entry_server_id = e.get_parent_server()



    def increment_time(self):
        self.time_table.increment_self()

    # Ask server for input and close
    def query_close(self):
        close = raw_input("Close server? y/n")
        if close == "y":
            self.run = False


class ClientHandler(threading.Thread):
    def __init__(self, client, address, parent_server):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.parent_server = parent_server

    def run(self):
        while True:
            recv = self.client.recv(1024)
            inp = recv.split(' ', 1)
            if recv == 'close':
                print("Closing client connection")
                self.client.close()
                # self.parent_server.query_close()
                break
            elif inp[0] == 'post':
                self.parent_server.post(inp[1], self.address)
            elif inp[0] == 'lookup':
                self.parent_server.lookup(self.client)
            elif inp[0] == 'sync':
                self.parent_server.sync()
            else:
                print("Received message:", recv)

def close_socket():
    server.socket.close()

server = Server(server_id=0, port=18874)
atexit.register(close_socket)
# Server()
