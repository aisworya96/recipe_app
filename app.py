from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from extensions import db, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0951e543-441d-41e9-9890-224eee7440a2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/MyDatabase'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = app.config['SECRET_KEY']

from models import User, Recipe, Comment


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes, session=session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('login/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))
        session['user_id'] = user.id

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('login/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, author=current_user)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('recipe/create_recipe.html')


@app.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author != current_user:
        flash("You don't have permission to edit this recipe.", 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    return render_template('recipe/edit_recipe.html', recipe=recipe)


@app.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author != current_user:
        flash("You don't have permission to delete this recipe.", 'danger')
        return redirect(url_for('index'))

    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/favorite/<int:recipe_id>', methods=['POST'])
@login_required
def favorite_recipe(recipe_id):
    if 'user_id' in session:
        user_id = session['user_id']

        user = User.query.get(user_id)

        recipe = Recipe.query.get(recipe_id)

        user.favorites.append(recipe)
        db.session.commit()

        return redirect('/view-recipe/' + str(recipe_id))
    else:
        return redirect('/login')


@app.route('/comment/<int:recipe_id>', methods=['POST'])
@login_required
def add_comment(recipe_id):
    if 'user_id' in session:
        user_id = session['user_id']
        comment_text = request.form['comment']
        recipe = Recipe.query.get(recipe_id)
        comment = Comment(text=comment_text, user_id=user_id)
        recipe.comments.append(comment)
        db.session.commit()
        return redirect('/view-recipe/' + str(recipe_id))
    else:
        return redirect('/login')

@app.route('/favorite/remove/<int:recipe_id>', methods=['POST'])
@login_required
def remove_favorite_recipe(recipe_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        recipe = Recipe.query.get(recipe_id)
        user.favorites.remove(recipe)
        db.session.commit()
        return redirect('/view-recipe/' + str(recipe_id))
    else:
        return redirect('/login')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        recipes = Recipe.query.filter(or_(Recipe.title.ilike(f'%{query}%'),
                                          Recipe.ingredients.ilike(f'%{query}%'),
                                          Recipe.instructions.ilike(f'%{query}%'))).all()
        return render_template('search/search_results.html', query=query, recipes=recipes)
    return render_template('search/search.html')

@app.route('/view-recipe/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe/view_recipe.html', recipe=recipe)


def populate_database():
    # Create a predefined user
    username = 'admin'
    password = 'password'
    hashed_password = generate_password_hash(password)
    admin_user = User(username=username, password=hashed_password)
    db.session.add(admin_user)
    db.session.commit()

    # Create a predefined recipe
    title = 'Chocolate Cake'
    instructions = '1. Preheat the oven...\n2. In a mixing bowl...\n3. Bake for 30 minutes...'
    ingredients = '1.water'
    admin_user_id = admin_user.id
    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, author_id=admin_user_id)
    db.session.add(recipe)
    db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_database()
    app.run(debug=True)
