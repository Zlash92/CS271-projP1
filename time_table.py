class TimeTable(object):

    def __init__(self, server_id, size):

        self.size = size
        self.table = [[0 for _ in range(size)] for _ in range(size)]
        self.server_id = server_id

    def sync_tables(self, table2):

        # Max of all elements
        for j in range(self.size):
            for k in range(self.size):
                self.table[j][k] = max(self.table[j][k], table2.table[j][k])

        # Max of local i'th row and remote k'th row
        for i in range(self.size):
            self.table[self.server_id][i] = max(self.table[self.server_id][i], table2.table[table2.server_id][i])


    def update(self, server, count):
        self.table[server][server] = count

    def increment_self(self):
        self.table[self.server_id][self.server_id] += 1

    def get_table_entry(self, i, j):
        return self.table[i][j]

    def get_self_clock(self):
        return self.table[self.server_id][self.server_id]

# t1 = TimeTable(2, 3)
# t2 = TimeTable(1, 3)
#
# table1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# table2 = [[3, 0, 0], [3, 1, 0], [0, 0, 0]]
#
# t1.table = table1
# t2.table = table2
#
# print t1.table
# print t2.table
#
# t1.sync_tables(t2)
#
# print t1.table