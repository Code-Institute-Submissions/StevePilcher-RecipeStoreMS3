import os
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from flask import Flask, render_template
redirect, request, session, url_for, flash, redirect
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

# Home route that checks for a logged in user


@app.route('/')
def index():
    if 'userid' in session:
        return redirect(url_for('my_recipes', user=['userid']))
    return render_template('login.html', title='Home')


# Login user verification with flash message for failed login

@app.route('/login', methods=['POST', 'GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password']
                         .encode('utf-8'),
                         login_user['password']) == login_user['password']:
            session['userid'] = str(login_user['_id'])
            return redirect(url_for('index'))

    return render_template(
        'login.html', message=flash(
            'The username {} does not exist!'.format(
                request.form["username"], title='Home')))

# Logout route to pop user from session


@app.route("/logout")
def logout():
    session.pop('userid', None)
    return render_template('login.html', title='Home')


# Signup route with check for existing username

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'),
                bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            user_id = session['userid']
            return redirect(url_for('create_recipe'))

        return render_template(
            'signup.html', message=flash(
                'The username {} already exists!'.format(
                    request.form["username"])))

    return render_template('signup.html')


# Create route for input form

@app.route('/create_recipe')
def create_recipe():
    user_id = session['userid']
    if 'userid' in session:
        return render_template(
            'createrecipe.html',
            title='Create Recipe',
            user_id=user_id,
            categories=mongo.db.categories.find())
    return render_template('login.html')

# Insert recipe and assign logged in user to that recipe


@app.route('/insert_recipe', methods=['POST', 'GET'])
def insert_recipe():
    recipes = mongo.db.recipes
    user_id = session['userid']
    group_recipe = request.form.to_dict()
    group_recipe['userid'] = user_id
    group_recipe = recipes.insert_one(group_recipe)
    return redirect(url_for('my_recipes'))

# Delete recipe function from Mongo


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('my_recipes'))

# Find all recipes associated with that user and display


@app.route('/my_recipes')
def my_recipes():
    user_id = session['userid']
    if 'userid' in session is None:
        return render_template('login.html')

    user_recipes = mongo.db.recipes.find({'userid': user_id})
    if user_recipes is None:
        return render_template('createrecipe.html')

    return render_template(
        'myrecipes.html',
        user_recipes=user_recipes,
        user_id=user_id,
        title='My Recipes')

# Edit route, retrieve and display the specific recipe


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    user_id = session['userid']
    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    categories = mongo.db.categories.find()
    return render_template(
        'editrecipe.html',
        recipe=the_recipe,
        categories=categories,
        user_id=user_id)


# Update the edited recipe back to Mongo

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    user_id = session['userid']
    recipes.update({'_id': ObjectId(recipe_id)},
                   {'category_name': request.form.get('category_name'),
                    'recipe_name': request.form.get('recipe_name'),
                    'ingredients': request.form.get('ingredients'),
                    'preparation_instructions': request.form.get
                    ('preparation_instructions'),
                    'cooking_instructions': request.form.get
                    ('cooking_instructions'),
                    'prep_time': request.form.get('prep_time'),
                    'cook_time': request.form.get('cook_time'),
                    'userid': user_id,
                    })
    return redirect(url_for('my_recipes'))

# Display page of categories to search


@app.route('/categories')
def categories():
    user_id = session['userid']
    return render_template('search.html', user_id=user_id)

# Search particular category of recipes owned by that user.


@app.route('/search')
def search():
    user_id = session['userid']
    category_name = request.values.get('submit_button')
    user_recipes = mongo.db.recipes.find(
        {'userid': user_id, 'category_name': category_name})
    return render_template(
        'search.html',
        user_recipes=user_recipes,
        user_id=user_id,
        title=category_name)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
