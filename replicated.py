from __future__ import print_function


class ReplicatedDictionary:
    def __init__(self):
        self.dict = {}

    def add_post(self, entry):
        self.dict[len(self.dict)] = entry

    def show_posts(self):
        for key, entry in self.dict.iteritems():
            entry.print_entry()


class ReplicatedLog:
    def __init__(self):
        self.log = []

    def add_entry(self, entry):
        self.log.append(entry)

    def remove_entry(self, entry):
        self.log.remove(entry)

    def show_log(self):
        for entry in self.log:
            entry.print_entry()

class Entry:
    def __init__(self, post, author, time_stamp, parent_server_id):
        self.post = post
        self.author = author

        # Identifiers of entry
        self.time_stamp = time_stamp
        self.parent_server_id = parent_server_id

    def get_parent_server(self):
        return self.parent_server_id

    def get_time_stamp(self):
        return self.time_stamp

    def print_entry(self):
        print(self.author, ": ", self.post, sep="")

