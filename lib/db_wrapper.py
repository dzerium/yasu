import sqlite3


class db_wrapper: 

    def __init__(self, location):
        self.connection = sqlite3.connect(location)
        self.cursor = self.connection.cursor()
    #end __init__

    def deinit(self):
        self.connection.close()
    #end deinit

    def create_table(self, table):
        print("Creating table for: ", table)
        sql = """create table if not exists \"""" + table + """\" (
                id INTEGER,
                date text(10),
                open real,
                close real,
                high real,
                low real,
                volume INTEGER,
                CONSTRAINT NOW_PK PRIMARY KEY (id)
                ) """
        self.cursor.execute(sql)
    #end create_table

    def insert_row(self, table, rows):
        sql = "INSERT INTO \"{0}\" (\"date\", \"open\", \"close\", \"high\", \"low\", \"volume\") VALUES (?,?,?,?,?,?) ".format(table)
        self.cursor.executemany(sql, rows)
        self.connection.commit()
    #end db_wrapper