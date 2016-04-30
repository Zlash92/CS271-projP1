from __future__ import print_function
import socket
import replicated


class Client:

  def __init__(self, host, port=80):
    self.s = socket.socket()
    self.connectToServer(self.s, host, port)

  def connectToServer(self, s, host, port):
    connection = False
    try:
      s.connect((host, port))
      connection = True
    except:
      print('Unable to connect to server')
      s.close()

    if connection:
      # Receive no more than 1024 bytes
      print(self.s.recv(1024))

      while True:
        msg = raw_input('Enter message: ')
        if msg == 'close':
          self.s.send(msg)
          break
        if msg == 'lookup':
          self.s.send(msg)
          recv = s.recv(1024)
          
        self.s.send(msg)
      self.s.close()


# c = Client(host='128.111.84.221')
c = Client(host=socket.gethostname(), port=18861)