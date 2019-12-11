import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ticketsDB:
    def __init__(self):
        self.connection = sqlite3.connect("tickets_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def insertEntry(self, entrant_name, entrant_age, guest_name, random_token):
        data = [entrant_name, entrant_age, guest_name, random_token]
        self.cursor.execute(
            "INSERT INTO entries (entrant_name, entrant_age, guest_name, random_token) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def getEntries(self):
        self.cursor.execute("SELECT * FROM entries")
        result = self.cursor.fetchall()
        return result

    def goldenTicket(self, winner):
        data = [winner]
        self.cursor.execute(
            "SELECT random_token FROM entries WHERE id = ?", data)
        result = self.cursor.fetchone()
        return result
