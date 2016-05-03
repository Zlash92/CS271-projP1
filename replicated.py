from __future__ import print_function


class ReplicatedDictionary:
    def __init__(self):
        self.dict = {}

    def add_post(self, entry):
        self.dict[len(self.dict)] = entry

    def show_posts(self):
        for key, entry in self.dict.iteritems():
            entry.print_entry()

    # Return True if not in dictionary
    def is_not_in(self, entry):
        # if entry in self.dict.values():
        #     return False
        # else:
        #     return True
        boolean = True
        for dictEntry in self.dict.values():
            if entry.time_stamp == dictEntry.time_stamp and entry.parent_server_id == dictEntry.parent_server_id:
                boolean = False

        return boolean


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

    def get_log(self):
        return self.log


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


# rd = ReplicatedDictionary()
# entry1 = Entry("Hello", 1, 0, 0)
# entry2 = Entry("World", 1, 2, 0)
#
#
# rl = ReplicatedLog()
# rl.add_entry(entry1)
# rl.add_entry(entry2)
#
# rd.add_post(entry1)
# rd.add_post(entry2)
# rd.show_posts()
# print(rd.is_not_in(entry2))
# print(rd.is_not_in(entry1))
