if __name__ == '__main__':
    import sqlite3

    db_lp = sqlite3.connect('login_password.db')
    cursor_db = db_lp.cursor()
    sql_create = '''CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    nickname TEXT NOT NULL,
    password TEXT NOT NULL);'''

    db_lp.commit()

    cursor_db.close()
    db_lp.close()