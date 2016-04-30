from __future__ import print_function
import socket
import replicated


class Server:


  def __init__(self, port=80):
    self.socket = socket.socket()
    self.host = socket.gethostname()
    self.socket.bind((self.host, port))
    self.data = replicated.ReplicatedDictionary()
    self.time = 0
    self.timeTable = None

    self.initConnection()


  def initConnection(self):
    self.socket.listen(5)
    print("Server is running and listening for incoming connections")

    while True:
      c, addr = self.socket.accept()
      print("Connected to", addr)
      c.send("Connection to server was successful")

      while True:
        recv = c.recv(1024)
        inp = recv.split(' ', 1)
        if recv == 'close':
          print("Closing client connection")
          c.close()
          break
        elif inp[0] == 'post':
          self.post(inp[1], addr)
        elif inp[0] == 'lookup':
          self.lookup(c)
        elif inp[0] == 'sync':
          self.sync()
        else:
          print("Received message:", recv)

      break

  def post(self, msg, author):
    self.incrementTime()
    self.data.addPost(self.time, msg, author)
    print("Post has been submitted at local time", self.time)

  def lookup(self, c):
    c.send(self.data)

  def sync(self, other):
    pass

  def incrementTime(self):
    self.time += 1

server = Server(port=18861)
# Server()
