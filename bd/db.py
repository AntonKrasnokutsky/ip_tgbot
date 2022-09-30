import sqlite3

FILE_DB = 'db.sqlite3'


def create_bd():
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS subdivision(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        network TEXT,
        prefix TEXT,
        gateway TEXT,
        dns TEXT
    );

    CREATE TABLE IF NOT EXISTS networks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_id INTEGER NOT NULL,
        name_pc TEXT,
        cabinet TEXT,
        ip_address TEXT,
        owner TEXT,
        FOREIGN KEY(department_id) REFERENCES department(id)
    );

    ''')
    con.commit()
    con.close()


def create_tvsp(tvsp_name):
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute(
        '''
        INSERT INTO subdivision(
            name
        )
        VALUES (?);
        ''',
        (tvsp_name,)
    )
    con.commit()
    con.close()


def update_address_tvsp(tvsp_id, address):
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute(
        '''
        UPDATE subdivision
        SET address = ?
        WHERE id = ?
        ''',
        (address, tvsp_id)
    )
    con.commit()
    con.close()


def update_net_tvsp(tvsp_id, net):
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute(
        '''
        UPDATE subdivision
        SET network = ?
        WHERE id = ?
        ''',
        (net, tvsp_id)
    )
    con.commit()
    con.close()


def select_all_tvsp():
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute('SELECT * FROM subdivision;')
    return cur


def select_tvsp(tvsp_id):
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute('SELECT * FROM subdivision WHERE id = ?;', (tvsp_id,))
    return cur


if __name__ == '__main__':
    pass
