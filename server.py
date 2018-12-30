from bottle import (get, post, request, route, run, static_file, jinja2_view)
import json
from pymysql import connect, cursors
from functools import partial


view = partial(jinja2_view, template_lookup=['templates'])


# setting the connection to the DB server
connection = connect(host='localhost',
                     user='root',
                     password='hilla',
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


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()