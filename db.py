import sqlite3


class Db:
    def __init__(self):
        self.conn = sqlite3.connect('main.db')
        self.cursor = self.conn.cursor()


    def insert(self, args):
        self.args = args
        try:
            self.cursor.execute(
                ("INSERT INTO Songs VALUES (?, ?, ?, ?, 1)"), (self.args[0], self.args[1], self.args[2], self.args[3]))
            self.conn.commit()
        except sqlite3.DatabaseError as err:
            pass
        else:
            self.conn.commit()

    def insert_empty_page(self, page, link, is_del):
        try:
            self.cursor.execute(
                ("INSERT INTO Empty_links VALUES (?, ?, ?)"), (page, link, is_del))
            self.conn.commit()
        except sqlite3.DatabaseError as err:
            pass
        else:
            self.conn.commit()

    def select_last_id(self):
        self.cursor.execute("SELECT id FROM Songs ORDER BY id DESC LIMIT 1")
        temp = self.cursor.fetchall()
        if temp:
            return temp[0][0]
        else:
            return 0


    def get_path(self):
        self.cursor.execute('SELECT path FROM Save_folder')
        return self.cursor.fetchone()[0]

    def update_path(self, path):
        self.cursor.execute(('UPDATE Save_folder SET path = ?'), (path,))
        self.conn.commit()


    def close_conection(self):
        return self.conn.close()

