from bottle import (get, post, request, route, run,template, static_file, jinja2_view, redirect, response, HTTPError, HTTPResponse)
import json
from pymysql import connect, cursors
from functools import partial
from db_utils import (select, insert, is_user_exist, execute_query, add_meal, add_tags)
from uuid import uuid4


view = partial(jinja2_view, template_lookup=['templates'])

# setting the connection to the DB server
connection = connect(host='localhost',
                     user='root',
                     password='hilla',
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
            status = "SUCCESS"
            # redirect('/welcome?username={}'.format(user_name))
        else:
            status = "ERROR"
    except HTTPResponse as e:
        print(e)
        status = "ERROR"
    return json.dumps({"status": status, "username": user_name})


@get('/welcome')
@view('welcome.html')
def welcome():
    user_name = request.query.username
    return {"username":user_name}


# @get('/signup')
# @view('login.html')
# def signup():
#         return {}
# def Sign_Up():
#     user_name = request.POST.get('user_name')
#     first_name = request.POST.get('first_name')
#     last_name = request.POST.get('last_name')
#     email = request.POST.get('email')
#     password = request.POST.get('password')
#     sessionid = request.get_cookie("sessionid")
#     try:
#         with connection.cursor() as cursor:
#             sql = "INSERT INTO users (`user_name`,`first_name`, `last_name`,`email`,`password`) VALUES('{}','{}','{}','{}')".format(
#                 user_name, first_name, last_name, email, password)
#             cursor.execute(sql)
#             connection.commit()
#             redirect(sessionid)
#     except:
#         return json.dumps({'STATUS': 'ERROR', 'MSG': "error in the values adding"})


#
# @post('/signup')
# @view('login.html')
# def prosses_Sign_Up():
#         return ()


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



# @get('/myaccount')
# @view('login.html')
# def login_route():
#         return ()


@get('/dishes')
@view('dishes.html')
def dishes():
    try:
        conn = connection
        c = conn.cursor()
        c.execute(
            "SELECT meals.id, meals.name ,meals.image, CAST(meals.delivery_date AS char(10)) as date,CONCAT(users.first_name , ' ', users.last_name) as chef , tags.vegan,"
            " tags.vegetarian, tags.meat, tags.fish, tags.kosher, tags.dairy, tags.hot, tags.cold, meals.description"
            " FROM meals"
            " JOIN users ON users.id = meals.chef_id "
            " JOIN tags ON tags.id = meals.id "
            "ORDER BY delivery_date")
        result = c.fetchall()
        final = []
        for dict_ in result:
            dict_['tags'] = [key for key, value in dict_.items() if value == 1]
            #TO REMOVE:
            # dict_["image"] = 'https://images.unsplash.com/photo-1473093226795-af9932fe5856?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=985&q=80'
        for dict_ in result:
            key_to_remove = ["vegan", "vegetarian", "meat", "fish", "kosher", "cold", "dairy", "hot"]
            for element in key_to_remove:
                if element in dict_.keys():
                    del dict_[element]
            final.append(dict_)
    except:
        status = 'ERROR'
        return json.dumps({'status': status})
    return {"dishes": final}



@post('/dish')
def dish():
    try:
        meal_id = request.params.mealid
        user_id = request.get_cookie('user_id')
        #the insert function doesn't work
        insert('transactions', ['customer_id', 'meal_id'], [user_id, meal_id])
        status = 'SUCCESS'
    except Exception as e:
        print(e)
        status = 'ERROR'
    return json.dumps({'status': status})


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()


