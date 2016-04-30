class TimeTable(object):

    def __init__(self, size):

        self.size = size
        self.table = [[0 for _ in range(size)] for _ in range(size)]

    def sync_tables(self, table2, self_id, table2_id):

        for i in range(self.size):
            self.table[self_id][i] == table2[table2_id][i]

        for j in range(self.size):
            for k in range(self.size):
                self.table[j][k] == max(self.table[j][k], table2[j][k])

    def update(self, server, count):
        self.table[server][server] = count

    def get_table_entry(self, i, j):
        return self.table[i][j]