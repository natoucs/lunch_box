import pymysql

conn_params = {"user": 'zivgos',
               "password": '6QP6N220YQU5X^l%',
               "host": 'db4free.net',
               "database": "lunchbox"}


def check_columns(columns):
    if not len(columns):
        raise ValueError("Must specify at least one column!")


def stringify_columns(columns):
    columns = [columns] if hasattr(columns, 'lower') else columns
    return '`, `'.join(columns)


def stringify_where(where):
    where = [where] if hasattr(where, 'lower') else where
    return ' and '.join(where)


def stringify_update(data):
    return ','.join(f"`{key}`='{value}'" for key, value in data.items())


def stringify_order_by(order_by):
    return '`, `'.join(order_by)


def compose_insert(table, columns):
    columns_str = stringify_columns(columns)
    placeholders = ','.join(['%s'] * len(columns))
    insert_query = f"insert into `{table}` (`{columns_str}`) values ({placeholders});"
    return insert_query


def compose_select(columns, table, where, order_by):
    columns_str = stringify_columns(columns)

    where = 'where ' + stringify_where(where) if where else ''
    order_by_str = 'order by ' + stringify_order_by(order_by)
    return f"select `{columns_str}` from `{table}` {where} {order_by_str};"


def compose_update(table, data, where=None):
    """ data is a dictionary """
    data_str = stringify_update(data)
    where = 'where ' + stringify_where(where) if where else ''
    return f"update {table} set {data_str} {where};"


# only use this
# table: string
# columns: list
# values: list
# values and column elements must be ordered
def insert(table, columns, values):
    check_columns(columns)
    values = [values] if hasattr(values, 'lower') else values
    query = compose_insert(table, columns)
    return execute_query(query, values)


# only use this
def select(columns, table, where=None):
    check_columns(columns)
    query = compose_select(columns, table, where)
    return execute_query(query)


def update(table, data, where=None):
    check_columns(data)
    query = compose_update(table, data, where=where)
    return execute_query(query)


# delete participant
def execute_query(query, values=None):
    global conn_params

    with pymysql.connect(**conn_params) as cursor:
        if values:
            return cursor.execute(query, values)
        else:
            cursor.execute(query)
            return cursor.fetchall()


def delete_record(table, where):
    where = stringify_where(where)
    return execute_query(f'update `{table}` set `deleted_at` = current_timestamp() where {where};')

