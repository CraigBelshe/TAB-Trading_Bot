import sqlite3

import constants

connection = sqlite3.connect(constants.database)
cursor = connection.cursor()

ticker_init = '''
    CREATE TABLE ticker (
    pair CHAR(6),
    date TIMESTAMP,
    value FLOAT,
    volume FLOAT,
    vwap FLOAT);'''

create_trigger = '''
    CREATE TRIGGER queue AFTER INSERT ON ticker BEGIN
    DELETE FROM ticker WHERE
        date =(SELECT min(date) FROM ticker) 
        AND (SELECT count(*) FROM ticker) > 1000001; 
    END;'''

order_book_init = '''
    CREATE TABLE order_book (
    type TINYTEXT,
    price FLOAT,
    amount FLOAT);'''

cursor.execute(' SELECT count(name) FROM sqlite_master WHERE type="table" AND name="ticker"')
if cursor.fetchone()[0] != 1:
    cursor.execute(ticker_init)

cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="order_book"')
if cursor.fetchone()[0] != 1:
    cursor.execute(order_book_init)

cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="trigger" AND name="queue"')
if cursor.fetchone()[0] != 1:
    cursor.execute(create_trigger)

connection.commit()
connection.close()
