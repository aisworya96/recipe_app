# Flask Recipe App

This Flask application allows users to create, edit, and delete recipes. Users can register, log in, and add comments to recipes. The application uses SQLAlchemy for database management and Flask-Login for user authentication.

## Endpoints

- `GET /`
    - Renders the homepage, displaying all recipes.
    - Requires the user to be logged in.
- `GET /register`
    - Renders the registration page.
    - Allows users to create a new account.
- `POST /register`
    - Handles the registration form submission.
    - Creates a new user in the database.
- `GET /login`
    - Renders the login page.
    - Allows users to log in to their accounts.
- `POST /login`
    - Handles the login form submission.
    - Validates user credentials and logs the user in.
- `GET /logout`
    - Logs out the currently logged-in user.
- `GET /create-recipe`
    - Renders the recipe creation page.
    - Allows logged-in users to create a new recipe.
- `POST /create-recipe`
    - Handles the recipe creation form submission.
    - Adds a new recipe to the database.
- `GET /edit-recipe/<int:recipe_id>`
    - Renders the recipe editing page for the specified recipe ID.
    - Allows the author of the recipe to edit it.
- `POST /edit-recipe/<int:recipe_id>`
    - Handles the recipe editing form submission.
    - Updates the recipe in the database.
- `POST /delete-recipe/<int:recipe_id>`
    - Handles the recipe deletion form submission.
    - Deletes the specified recipe from the database.
- `POST /favorite/<int:recipe_id>`
    - Handles the favorite recipe form submission.
    - Adds the specified recipe to the user's favorites list.
- `POST /comment/<int:recipe_id>`
    - Handles the comment submission form for the specified recipe ID.
    - Adds a new comment to the recipe.
- `POST /favorite/remove/<int:recipe_id>`
    - Handles the removal of a recipe from the user's favorites list.
- `GET /search`
    - Renders the search page.
    - Allows users to search for recipes based on keywords.
- `POST /search`
    - Handles the search form submission.
    - Retrieves recipes matching the search query.
- `GET /view-recipe/<int:recipe_id>`
    - Renders the page displaying the details of the specified recipe ID.
    - Requires the user to be logged in.

## Setup and Usage

1. Install the required dependencies by running:

2. Configure the database connection in the Flask application:
- Update the `app.config['SQLALCHEMY_DATABASE_URI']` value in `app.py` with the appropriate database URI.

3. Create the database tables by running the following command:

```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(500) NOT NULL
);

CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE favorites (
    user_id INT,
    recipe_id INT,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)
);

CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (id)
);

INSERT INTO user (username, password) VALUES ('admin', 'password');
INSERT INTO recipe (title, ingredients, instructions, created_at, author_id)
VALUES ('Chocolate Chip Cookies', 'Flour, sugar, chocolate chips', '1. Preheat oven to 350°F. 2. Mix ingredients...', NOW(), 1);
```
4. Before running below command check the flask version using command ``falsk --version``
```agsl
Python 3.10.0
Flask 2.1.3
Werkzeug 2.0.1
```
Commands to run the application:
    ``flask run``

5. Access the application by visiting `http://localhost:5000` in your web browser.

