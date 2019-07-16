import sqlite3

import constants

def sql_exec(statement):
    connection = sqlite3.connect(constants.database)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    connection.close()


def sql_fetch(statement):
    connection = sqlite3.connect(constants.database)
    cursor = connection.cursor()
    cursor.execute(statement)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data
