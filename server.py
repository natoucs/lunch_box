from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect, response)
import json
from pymysql import connect, cursors
from functools import partial
from db_utils import (select, insert, is_user_exist, execute_query, add_meal, add_tags)


view = partial(jinja2_view, template_lookup=['templates'])


def set_user_cookie(user):
    with connection.cursor() as cursor:
        sql = "SELECT user_name FROM users WHERE user_name = '{}'".format(user)#need to change to user_name
        cursor.execute(sql)
        result = cursor.fetchall()
        for res in result:
            if res['user_name'] == user:
                sessionid = str(uuid4().hex)[:8]
                response.set_cookie("user_name", user)
                response.set_cookie("sessionid", sessionid)
                print(sessionid)
    return (sessionid)



# static Routes
@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/images")


# serving templates
@get('/')
@view('home.html')
def home():
    return {}


@get('/login')
@view('login.html')
def login():
    return {}


@post('/login')
def login():
    try:
        user_name = request.forms.get("user_name")
        is_user_exist(user_name)
        status = "SUCCESS"
    except:
        status = "ERROR"
    return json.dumps({"status": status})


@get('/signup')
@view('login.html')
def signup():
        return {}
def Sign_Up():
    user_name = request.POST.get('user_name')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    sessionid = request.get_cookie("sessionid")
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (`user_name`,`first_name`, `last_name`,`email`,`password`) VALUES('{}','{}','{}','{}')".format(
                user_name, first_name, last_name, email, password)
            cursor.execute(sql)
            connection.commit()
            redirect(sessionid)
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "error in the values adding"})



@post('/signup')
@view('login.html')
def prosses_Sign_Up():
        return ()


# Displays the page where you fill the form ('offer.html')
@get('/offer')
@view('offer.html')
def login_route():
        return {}


# Front-end wants to insert in the database an offer from a cook
@post('/offer')
def login_route():
    dict_meal = {  # keys NEED to be the column name in the database
        'chef_id': request.get_cookie('user_id'),  # fake until it works (fetch cookie/session_id)
        'description': request.forms.get("description"),
        'number': request.forms.get("number"),
        'date': request.forms.get("date"),
        'name': request.forms.get("name"),
    }

    dict_tags = {
        'kosher': request.forms.get("kosher"),
        'vegetarian': request.forms.get("vegetarian"),
        'vegan': request.forms.get("vegan"),
        'meat': request.forms.get("meat"),
        'fish': request.forms.get("fish"),
        'dairy': request.forms.get("dairy"),
        'hot': request.forms.get("hot"),
        'cold': request.forms.get("cold")
    }

    # to do later
    image = request.forms.get("image")

    try:
        meal_id = add_meal(dict_meal)  # inserts new meal into database and returns its ID
        add_tags(meal_id, dict_tags)  # uses the previous meal ID to add the tags of the meal
        status = 'SUCCESS'
    except Exception as error:
        print(error)
        status = 'ERROR'

    return json.dumps({'status': status})


@get('/myaccount')
@view('login.html')
def login_route():
        return ()


@get('/dishes')
def dishes():
    try:
        conn = connection
        c = conn.cursor()
        c.execute(
            "SELECT meals.id, meals.name, meals.delivery_date,users.first_name +''+users.last_name , tags.vegan,"
            " tags.vegetarian, tags.meat, tags.fish, tags.kosher, tags.dairy, tags.hot, tags.cold, meals.description"
            " FROM meals"
            " JOIN users ON users.id = meals.chef_id "
            " JOIN tags ON tags.id = meals.id "
            "ORDER BY delivery_date")
        result = c.fetchall()
        print(result)
        status = 'SUCCESS'
    except:
        status = 'ERROR'
    return json.dumps([result, {"status": status}])


@post('/dish/<meal_id>')
@view('dishes.html')  # store a click into the transaction table
def login():
    # fetch the data from the front
    try:
        user_name = request.get_cookie('user_name')
        # conn = connection
        # c = conn.cursor()
        result = execute_query(
            "SELECT customer_id, meal_id FROM transactions JOIN users on users.id = transactions.customer_id "
            "where users.user_name = %s" % (
                user_name,))
        customer_id, meal_id = result[0]
        insert('transactions', ['customer_id', 'meal_id'], [customer_id, meal_id])
        status = 'SUCCESS'
    except:
        status = 'ERROR'
    return json.dumps('status', status)


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
