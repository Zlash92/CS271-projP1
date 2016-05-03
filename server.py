from __future__ import print_function
import socket
import replicated
from time_table import TimeTable
import sys
import threading
import pickle
import signal

server_addresses = ['128.111.84.159', # Server0
                    '128.111.84.210', # Server1
                    '128.111.84.221'] # Server2

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
            # close = raw_input("Close server? y/n")
            # if close == "y":
            #     break
            c, addr = self.socket.accept()
            print("Connected to", addr)
            c.send("Connection to server was successful")
            client = ClientHandler(c, addr, self)
            client.start()
            self.threads.append(client)


        self.socket.close()
        for client in self.threads:
            client.join()

    def send_message(self, msg, ip):
        data = pickle.dumps(msg)
        address = (ip, 80)
        self.socket.sendto(data, address)

    def post(self, msg, author):
        self.increment_time()
        entry = replicated.Entry(msg, author, self.time_table.get_self_clock(), self.server_id)
        self.data.add_post(entry)
        self.log.add_entry(entry)
        print("Post has been submitted at local time", self.time_table.get_self_clock())

    def lookup(self, c):
        package = pickle.dumps(self.data)
        c.send(package)

    def sync(self, sync_server):
        address = (server_addresses[sync_server], 80)
        sock = socket.socket()
        sock.connect(address)
        r = sock.recv(1024)

        sock.send("update_contents_on_my_server")
        print("Waiting for receive")
        recv = sock.recv(1024)
        data = pickle.loads(recv)
        # TODO: Fix timetable etc...pickle
        sock.close()

        other_time_table = None
        other_log = None
        for e in other_log:
            if self.data.is_in(e):
                self.data.add_post(e)
                self.log.add_entry(e)

        self.time_table.sync_tables(other_time_table)
        self.garbage_collect_log()

    def received_sync(self, client):
        print("Received sync msg")
        client.send("Here you go")
        print("Msg sent")

    # Compiles log to send when another server wants to sync with this server
    def compile_log(self):
        subLog = []
        # TODO: server_id of recipient
        other_server_id = None
        for e in self.log:
            # The id of server where entry was first posted
            entry_server_id = e.get_parent_server()

            if self.time_table[other_server_id][entry_server_id] < e.get_time_stamp():
                subLog.append(e)

        return subLog

    def garbage_collect_log(self):
        # Entry i is the clock time at server i, to which point this server knows that all other servers know about events at server i
        max_common_clocks = column_min_vals(self.time_table)

        for e in self.log:
            if e.get_time_stamp() <= max_common_clocks[e.get_parent_server()]:
                self.log.remove_entry(e)

    def increment_time(self):
        self.time_table.increment_self()


class ClientHandler(threading.Thread):
    def __init__(self, client, address, parent_server):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.parent_server = parent_server


    def close_connection(self):
        self.socket.close()

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
            elif inp[0] == 'sync' and len(inp)>1:
                sync_server = int(inp[1])
                self.parent_server.sync(sync_server)
            elif recv == "update_contents_on_my_server":
                self.parent_server.received_sync(self.client)
            elif len(recv)>0:
                print("Received message:", recv)

# Returns a list of minimum values for each column in a 2D list
def column_min_vals(table):
    result = []
    print(result)

    for i in range(len(table)):
        minval = min([row[i] for row in table])
        result.append(minval)

    return result

def handler(signum, frame):
   try:
      print('Ctrl+Z pressed')
   finally:
      server.close_connection()


server = Server(port=80)
signal.signal(signal.SIGTSTP, handler)
