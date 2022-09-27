import sqlite3

FILE_DB = 'db.sqlite3'


def create_bd():
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS subdivision(
        id INTEGER PRIMARY KEY,
        subdivision_name CHAR,
        subdivision_address TEXT
    );

    CREATE TABLE IF NOT EXISTS networks(
        id INTEGER PRIMARY KEY,
        department_id INTEGER NOT NULL,
        name_pc CHAR,
        cabinet CHAR,
        ip_address CHAR,
        owner CHAR,
        FOREIGN KEY(department_id) REFERENCES department(id)
    );

    ''')
    con.commit()
    con.close()


if __name__ == '__main__':
    pass
