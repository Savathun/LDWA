import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch(self, table):
        self.cur.execute("SELECT * FROM " + table)
        return self.cur.fetchall()
