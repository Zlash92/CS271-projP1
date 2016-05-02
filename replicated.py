from __future__ import print_function


class ReplicatedDictionary:
    def __init__(self):
        self.dict = {}

    def add_post(self, entry):
        self.dict[len(self.dict)] = entry

    def show_posts(self):
        for key, entry in self.dict.iteritems():
            print(entry.author, ": ", entry.post, sep="")


class ReplicatedLog:
    def __init__(self):
        self.log = []

    def add_entry(self, entry):
        self.log.append(entry)

    def remove_entry(self):
        pass

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
        return self.ge

