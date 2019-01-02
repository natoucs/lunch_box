from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect, response)
import json
from pymysql import connect, cursors
from functools import partial
from db_utils import (select, insert, is_user_exist)


view = partial(jinja2_view, template_lookup=['templates'])


# setting the connection to the DB server
# connection = connect(host='localhost',
#                      user='ITC',
#                      #password='nathan',
#                      #db='store',
#                      charset='utf8',
#                      cursorclass=cursors.DictCursor)


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


@post('/signup')
@view('login.html')
def prosses_Sign_Up():
        return ()


@get('/offer')
@view('offer.html')
def login_route():
        return {}

# Front-end wants to insert in the database an offer from a cook
@post('/offer')
def login_route():
    user_id = 1 # fake until it works
    description = request.forms.get("description")
    number = request.forms.get("number")
    date = request.forms.get("date")
    name = request.forms.get("name")

    # later
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
               ['chef_id', 'description', 'total_servings', 'delivery_date', 'name'],
               [user_id, description, number, date, name])
        status = 'SUCCESS'
    except Exception as e:
        print(e)
        status = 'ERROR'

    return json.dumps({'status': status})



@get('/myaccount')
@view('login.html')
def login_route():
        return ()


@get('/dishes')
@view('dishes.html')
def login():
        return {}


@post('/dishes')
@view('dishes.html')
def login():
        return ()


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()