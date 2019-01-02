from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect, response)
import json
from pymysql import connect, cursors
from functools import partial
from lunch_box.db_utils import (select, insert)


view = partial(jinja2_view, template_lookup=['templates'])


def user_loged_in(user):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE first_name = '{}'".format(user)#need to change to user_name
        cursor.execute(sql)
        result = cursor.fetchall()
        for res in result:
            if res['first_name'] == user:
                #response.set_cookie("session_id",)
                response.set_cookie("user_name", user)
    return ("somthig from cocies")


# setting the connection to the DB server
connection = connect(host='localhost',
                     user='root',
                     password='momo',
                     db='lunch_box',
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
@view('login.html')
def login():
    user_name = request.forms.get("user_name")
    user_loged_in(user_name)
    return json.dumps({"user_name": user_name})


@get('/home')
@view('home.html')#not working!
def back_home():
    username = request.get_cookie("user_name")
    print(username)
    return (username)


@get('/signup')
@view('login.html')
def Sign_Up():
        return ()


@post('/signup')
@view('login.html')
def prosses_Sign_Up():
        return ()


# Potentially not necessary as already done through the dishes page. See with Hila later.
# Front wants to get information on the offers
@get('/pffer')
@view('offer.html')
def login_route():
        return ()

# Front-end wants to insert in the database an offer from a cook
@post('/offer')
@view('offer.html')
def login_route():
    date = request.forms.get("date")
    description = request.forms.get("description")
    number = request.forms.get("number")

    # will use later
    name = request.forms.get("name")
    kosher = request.forms.get("kosher")
    vegetarian = request.forms.get("vegetarian")
    vegan = request.forms.get("vegan")
    meat = request.forms.get("meat")
    fish = request.forms.get("fish")
    hot = request.forms.get("hot")
    cold = request.forms.get("cold")
    image = request.forms.get("image")

    try:
        insert('meals',
               ['description', 'total_servings', 'delivery_date'],
                [description, number, date])
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
def login():
        return ()


@post('/dishes')
@view('dishes.html')
def login():
        return ()


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()