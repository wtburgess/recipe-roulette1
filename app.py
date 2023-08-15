from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Sample ingredients table and recipes table
ingredients = {
    1: {'ingredient': "tomatoes", 'amount': "2"},
    2: {'ingredient': "onion", 'amount': "5"},
    3: {'ingredient': "garlic", 'amount': "3"},
    4: {'ingredient': "peanut butter", 'amount': "8"},
    5: {'ingredient': "chocolate", 'amount': "1"}
}


recipes_table = {
    1: ["tomato salad", ["tomatoes", "tomatoes"]],
    2: ["chicken tomatoes", ["chicken", "tomatoes"]],
    3: ["test recipe", ["garlic", "peanut butter", "ingredient4"]],
}

def find_matching_recipes(user_ingredients):
    matching_recipes = []

    for recipe_id, (_, recipe_ingredients) in recipes_table.items():
        if set(recipe_ingredients).issubset(set(user_ingredients)):
            matching_recipes.append(recipe_id)

    return matching_recipes

@app.route("/", methods=["GET"])
def index():
    selected_ingredients = session.get("selected_ingredients", [])
    matching_recipes = find_matching_recipes(selected_ingredients)

    return render_template("index.html", matching_recipes=matching_recipes)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_ingredients = parse_ingredients(request.form.get('recipe_ingredients'))
        recipe_is_core = request.form.get('recipe_is_core') == 'on'
        recipe_url = request.form.get('recipe_url')
        recipe_description = request.form.get('recipe_description')

        # Generate a unique recipe_id based on the length of the 'recipes' dictionary
        recipe_id = len(recipes) + 1

        recipes[recipe_id] = {
            'name': recipe_name,
            'ingredients': recipe_ingredients,
            'is_core': recipe_is_core,
            'url': recipe_url,
            'description': recipe_description
        }

        return redirect(url_for('recipes'))

    return render_template("recipes.html", recipes=recipes)



@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if recipe_id in recipes:
        print(f"Deleting recipe with ID: {recipe_id}")
        del recipes[recipe_id]
    else:
        print(f"Recipe with ID {recipe_id} not found.")

    return redirect(url_for('recipes'))


@app.route('/ingredient_overview', methods=['GET', 'POST'])
def ingredient_overview():
    if request.method == 'POST':
        ingredient_name = request.form.get('ingredient_name')
        ingredient_amount = request.form.get('ingredient_amount')

        # Generate a unique ingredient_id based on the length of the 'ingredients' dictionary
        ingredient_id = len(ingredients) + 1

        ingredients[ingredient_id] = {'ingredient': ingredient_name, 'amount': ingredient_amount}

        return redirect(url_for('ingredient_overview'))

    return render_template("ingredient_overview.html", ingredients=ingredients)

@app.route('/delete_ingredient/<int:ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    if ingredient_id in ingredients:
        print(f"Deleting ingredient with ID: {ingredient_id}")
        del ingredients[ingredient_id]
    else:
        print(f"Ingredient with ID {ingredient_id} not found.")

    return redirect(url_for('ingredient_overview'))







if __name__ == "__main__":
    app.run(debug=True)
