import pymysql
from bottle import response
from uuid import uuid4

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


def compose_select(columns, table, where, order_by=None):
    columns_str = stringify_columns(columns)

    where = 'where ' + stringify_where(where) if where else ''
    order_by_str = 'order by ' + stringify_order_by(order_by) if order_by else ''
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
    """
    :table str
    :columns list/tuple
    :values list/tuple
    :returns id of last int
    """

    check_columns(columns)
    values = [values] if hasattr(values, 'lower') else values
    query = compose_insert(table, columns)
    return execute_query(query, values)


def insert_dict(table, dictionary):
    """
    :table str
    :dictionary dict
    :returns id of last inserted row int
    """
    return insert(table, list(dictionary.keys()), list(dictionary.values()))


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
            cursor.execute(query, values)
            print(cursor.lastrowid)
            return cursor.lastrowid
        else:
            cursor.execute(query)
            return cursor.fetchall()


def delete_record(table, where):
    where = stringify_where(where)
    return execute_query(f'update `{table}` set `deleted_at` = current_timestamp() where {where};')


def is_user_exist(user):
    if select('user_name', 'users', f"user_name='{user}'")[0][0]:
        response.set_cookie("user_name", user)
        sessionid = str(uuid4().hex)[:8]
        response.set_cookie("sessionid", sessionid)
        return True
    else:
        return False


# adding entities
def add_user(data):
    """
    :data dict
    :returns id of last inserted row int
    """
    return insert('users', list(data.keys()), list(data.values()))


def add_meal(data):
    """
    :param data: dictionary
    :return: id of last added row
    """
    return insert_dict('meals', data)


def add_tags(meal_id, data):
    """ requires the id returned by add_meal"""
    data['meal_id'] = meal_id
    return insert_dict('tags', data)


# delete entities - no need for users and tags
def delete_meal(table, id):
    delete_record(table, id)


def delete_transaction(id):
    """ deletes a meal and subtract one serving from that meal's current servings """
    meal_id = select('meal_id', 'transactions', f"id={id}")[0][0]
    delete_record("transactions", "id={}")
    add_serving(meal_id)


# servings
def fetch_available_servings(meal_id):
    result = select(['total_servings', 'current_servings'], 'meals', f'id={meal_id};')[0]
    return result[0] - result[1]


def update_servings(meal_id, value):
    execute_query(f"update meals set current_servings = current_servings {value} where meal_id = {meal_id};")


def add_serving(meal_id):
    update_servings(meal_id, '+ 1')


def subtract_serving(meal_id):
    update_servings(meal_id, '- 1')
