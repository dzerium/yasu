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
                date text(10),
                open real,
                close real,
                high real,
                low real,
                volume INTEGER,
                CONSTRAINT NOW_PK PRIMARY KEY (date)
                ) """
        self.cursor.execute(sql)
    #end create_table

    def insert_row(self, table, rows, date):
        sql = "INSERT OR REPLACE INTO \"{0}\" (\"date\", \"open\", \"close\", \"high\", \"low\", \"volume\") VALUES (?,?,?,?,?,?) ".format(table)
        self.cursor.executemany(sql, rows)
        self.connection.commit()
        sql = "INSERT OR REPLACE INTO \"monitor\" (\"symbol\", \"synch_date\") VALUES (\"{0}\", \"{1}\") ".format(table, date)
        self.cursor.execute(sql)
        self.connection.commit()
    #end db_wrapper

    def get_monitor_status(self):
        sql = "SELECT * FROM monitor"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #end get_monitor_status
