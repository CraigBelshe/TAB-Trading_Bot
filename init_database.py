import sqlite3

import settings

connection = sqlite3.connect(settings.DATABASE)
cursor = connection.cursor()

ticker_init = '''
    CREATE TABLE ticker (
    id  INTEGER PRIMARY KEY,
    pair CHAR(6),
    date TIMESTAMP,
    value FLOAT,
    volume FLOAT,
    vwap FLOAT);'''

create_ticker_trigger = '''
    CREATE TRIGGER queue AFTER INSERT ON ticker BEGIN
    DELETE FROM ticker WHERE
        id =(SELECT min(id) FROM ticker) 
        AND (SELECT count(*) FROM ticker) > 1000001; 
    END;'''

create_order_trigger = '''
    CREATE TRIGGER queue2 AFTER INSERT ON order_book BEGIN
    DELETE FROM order_book WHERE
        id =(SELECT min(id) FROM order_book)
        AND (SELECT count(*) FROM order_book) > 1000001;
    END;'''

order_book_init = '''
    CREATE TABLE order_book (
    id INTEGER PRIMARY KEY,
    type TINYTEXT,
    pair CHAR(6),
    price FLOAT,
    amount FLOAT);'''

cursor.execute(' SELECT count(name) FROM sqlite_master WHERE type="table" AND name="ticker"')

if 0 in cursor.fetchone():
    cursor.execute(ticker_init)

cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="order_book"')
if 0 in cursor.fetchone():
    cursor.execute(order_book_init)

cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="trigger" AND name="queue"')
if 0 in cursor.fetchone():
    cursor.execute(create_ticker_trigger)

cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="trigger" AND name="queue2"')
if 0 in cursor.fetchone():
    cursor.execute(create_order_trigger)

connection.commit()
connection.close()
