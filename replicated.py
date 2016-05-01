from __future__ import print_function


class ReplicatedDictionary:

  def __init__(self):
    self.dict = {}

  def addPost(self, timeStamp, post, author):
    self.dict[len(self.dict)] = entry(post, author, timeStamp)

  def showPosts(self):
    for key, entry in self.dict.iteritems():
      print(entry.author, ": ", entry.post, sep="")


class ReplicatedLog:

  def __init__(self):
    self.log = {}


class entry:
  def __init__(self, post, author, timeStamp):
    self.post = post
    self.author = author
    self.timeStamp = timeStamp



