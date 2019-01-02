import pymysql

conn_params = {"user": 'zivgos',
               "password": '6QP6N220YQU5X^l%',
               "host": 'db4free.net',
               "database": "lunchbox"}


def check_columns(columns):
    if not len(columns):
        raise ValueError("Must specify at least one column!")


def stringify_columns(columns):
    return '`, `'.join(columns)


def compose_insert(table, columns):
    check_columns(columns)
    columns_str = stringify_columns(columns)
    placeholders = ','.join(['%s'] * len(columns))
    insert_query = f"insert into `{table}` (`{columns_str}`) values ({placeholders});"
    return insert_query


def compose_select(columns, table):
    check_columns(columns)
    columns_str = stringify_columns(columns)
    return f"select `{columns_str}` from `{table}`;"


def insert(table, columns, values):
    query = compose_insert(table, columns)
    return execute_query(query, values)


def select(columns, table):
    query = compose_select(columns, table)
    return execute_query(query)


def execute_query(query, values=None):
    global conn_params

    with pymysql.connect(**conn_params) as cursor:
        if values:
            return cursor.execute(query, values)
        else:
            cursor.execute(query)
            return cursor.fetchall()
