class TimeTable(object):

    def __init__(self, server_id, size):

        self.size = size
        self.table = [[0 for _ in range(size)] for _ in range(size)]
        self.server_id = server_id

    def sync_tables(self, table2):

        for i in range(self.size):
            self.table[self.server_id][i] = max(self.table[self.server_id][i], table2[table2.server_id][i])

        for j in range(self.size):
            for k in range(self.size):
                self.table[j][k] == max(self.table[j][k], table2[j][k])

    def update(self, server, count):
        self.table[server][server] = count

    def increment_self(self):
        self.table[self.server_id][self.server_id] += 1

    def get_table_entry(self, i, j):
        return self.table[i][j]

    def get_self_clock(self):
        return self.table[self.server_id][self.server_id]
