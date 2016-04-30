

#
# class ReplicatedDictionary:
#
#   def __init__(self):
#     self.dict = {}
#
#   def addPost(self, key, post):
#     self.dict[key] = post
#

class ReplicatedLog:

  def __init__(self):
    self.log = {}

  def addPost(self, timeStamp, post):
    self.dict[timeStamp] = post

  def showPosts(self):
    for time, value in self.log:
      print



