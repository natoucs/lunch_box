from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect)
import json
from pymysql import connect, cursors
from functools import partial


view = partial(jinja2_view, template_lookup=['templates'])


def user_loged_in():
    return ("somthig from cocies")


# setting the connection to the DB server
connection = connect(host='localhost',
                     user='root',
                     password='momo',
                     db='store',
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
    #check if user exists
    return ()


@get('/home')
@view('home.html')#not working!
def back_home():
        return ()


@get('/Sign_Up')
@view('login.html')
def Sign_Up():
        return ()


@post('/Sign_Up')
@view('login.html')
def prosses_Sign_Up():
        return ()


@get('/Offer')
@view('offer.html')
def login_route():
        return ()


@post('/Offer')
@view('offer.html')
def login_route():
        return ()


@get('/My_Acount')
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