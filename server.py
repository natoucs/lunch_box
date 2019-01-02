from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect, response, HTTPError)
import json
from pymysql import connect, cursors
from functools import partial
from db_utils import (select, insert, is_user_exist, execute_query, add_meal, add_tags)
from uuid import uuid4


view = partial(jinja2_view, template_lookup=['templates'])

# setting the connection to the DB server
connection = connect(host='db4free.net',
                     user='zivgos',
                     password='6QP6N220YQU5X^l%',
                     db='lunchbox',
                     charset='utf8',
                     cursorclass=cursors.DictCursor)


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
        if is_user_exist(user_name):
            user_id = select('id', 'users', f"user_name='{user_name}'")[0][0]
            response.set_cookie("user_id", str(user_id))
            sessionid = str(uuid4().hex)[:8]
            response.set_cookie("sessionid", sessionid)
            redirect('/dishes')
        else:
            status = "ERROR"
    except Exception as e:
        print(e)
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
        'total_servings': request.forms.get("number"),
        'delivery_date': request.forms.get("date"),
        'name': request.forms.get("name"),
        'image': None
    }

    dict_tags = {
        'kosher': 1 if request.forms.get("kosher") == 'true' else 0,
        'vegetarian': 1 if request.forms.get("vegetarian") == "true" else 0,
        'vegan': 1 if request.forms.get("vegan") == 'true' else 0,
        'meat': 1 if request.forms.get("meat") == 'true' else 0,
        'fish': 1 if request.forms.get("fish") == 'true' else 0,
        'dairy': 1 if request.forms.get("dairy") == 'true' else 0,
        'hot': 1 if request.forms.get("hot") == 'true' else 0,
        'cold': 1 if request.forms.get("cold") == 'true' else 0
    }

    try:
        meal_id = add_meal(dict_meal)  # inserts new meal into database and returns its ID
        add_tags(meal_id, dict_tags)  # uses the previous meal ID to add the tags of the meal
        status = 'SUCCESS'
    except:
        status = 'ERROR'

    return json.dumps({'status': status})



@get('/myaccount')
@view('login.html')
def login_route():
        return ()


@get('/dishes')
@view('dishes.html')
def dishes():
    try:
        conn = connection
        c = conn.cursor()
        c.execute(
            "SELECT meals.id, meals.name ,meals.image, CAST(meals.delivery_date AS char(10)) as date,CONCAT(users.first_name , ' ', users.last_name) as full_name , tags.vegan,"
            " tags.vegetarian, tags.meat, tags.fish, tags.kosher, tags.dairy, tags.hot, tags.cold, meals.description"
            " FROM meals"
            " JOIN users ON users.id = meals.chef_id "
            " JOIN tags ON tags.id = meals.id "
            "ORDER BY delivery_date")
        result = c.fetchall()
        print(result)
        final = []

        for dict_ in result:
            dict_['tags'] = [key for key, value in dict_.items() if value == 1]
        for dict_ in result:
            key_to_remove = ["vegan", "vegetarian", "meat", "fish", "kosher", "cold", "dairy", "hot"]
            for element in key_to_remove:
                if element in dict_.keys():
                    del dict_[element]
            final.append(dict_)
        print(final)
    except:
        status = 'ERROR'
        return json.dumps({'status': status})
    return {"dishes": final}



@post('/dish/<meal_id>')
def dish(meal_id):
    # fetch the data from the front
    try:
        user_id = request.get_cookie('user_id')
        result = execute_query("SELECT customer_id, meal_id FROM transactions JOIN "
                               "users on users.id = transactions.customer_id where users.id = %s" % user_id)
        customer_id, meal_id = result[0]
        insert('transactions', ['customer_id', 'meal_id'], [customer_id, meal_id])
        status = 'SUCCESS'
    except Exception as e:
        print(e)
        status = 'ERROR'
    return json.dumps({'status': status})



def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()


