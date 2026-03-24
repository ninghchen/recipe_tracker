from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'mediterranean-kitchen-secret'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
DATA_FILE = 'recipes.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

CATEGORIES = [
    {"id": "smoothies", "name": "Smoothies", "icon": "🥤"},
    {"id": "ninja-creami", "name": "Ninja Creami", "icon": "🍨"},
    {"id": "pasta", "name": "Pasta", "icon": "🍝"},
    {"id": "chicken", "name": "Chicken", "icon": "🍗"},
    {"id": "beef", "name": "Beef", "icon": "🥩"},
    {"id": "seafood", "name": "Seafood", "icon": "🦐"},
    {"id": "soups", "name": "Soups & Stews", "icon": "🍲"},
    {"id": "salads", "name": "Salads", "icon": "🥗"},
    {"id": "sauces", "name": "Sauces & Dips", "icon": "🫙"},
    {"id": "breakfast", "name": "Breakfast", "icon": "🍳"},
    {"id": "dessert", "name": "Dessert", "icon": "🍮"},
    {"id": "snacks", "name": "Snacks & Sides", "icon": "🥨"},
    {"id": "vegetarian", "name": "Vegetarian", "icon": "🥦"},
    {"id": "drinks", "name": "Drinks", "icon": "🍹"},
    {"id": "bread", "name": "Bread & Baking", "icon": "🍞"},
    {"id": "other", "name": "Other", "icon": "🍴"},
]

def load_recipes():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_recipes(recipes):
    with open(DATA_FILE, 'w') as f:
        json.dump(recipes, f, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    recipes = load_recipes()
    category_counts = {}
    for cat in CATEGORIES:
        category_counts[cat['id']] = sum(1 for r in recipes.values() if r.get('category') == cat['id'])
    return render_template('index.html', categories=CATEGORIES, recipes=recipes, category_counts=category_counts)

@app.route('/category/<cat_id>')
def category(cat_id):
    recipes = load_recipes()
    cat_recipes = {k: v for k, v in recipes.items() if v.get('category') == cat_id}
    cat_info = next((c for c in CATEGORIES if c['id'] == cat_id), None)
    return render_template('category.html', recipes=cat_recipes, category=cat_info, categories=CATEGORIES)

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipes = load_recipes()
    r = recipes.get(recipe_id)
    if not r:
        return redirect(url_for('index'))
    cat_info = next((c for c in CATEGORIES if c['id'] == r.get('category')), None)
    return render_template('recipe.html', recipe=r, recipe_id=recipe_id, category=cat_info, categories=CATEGORIES)

@app.route('/new', methods=['GET', 'POST'])
def new_recipe():
    if request.method == 'POST':
        recipes = load_recipes()
        recipe_id = str(uuid.uuid4())[:8]

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{recipe_id}_{file.filename}")
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"uploads/{filename}"

        # Parse ingredients
        ing_names = request.form.getlist('ing_name[]')
        ing_amounts = request.form.getlist('ing_amount[]')
        ing_units = request.form.getlist('ing_unit[]')
        ingredients = []
        for name, amount, unit in zip(ing_names, ing_amounts, ing_units):
            if name.strip():
                ingredients.append({"name": name.strip(), "amount": amount.strip(), "unit": unit.strip()})

        # Parse steps
        step_titles = request.form.getlist('step_title[]')
        step_descs = request.form.getlist('step_desc[]')
        steps = []
        for title, desc in zip(step_titles, step_descs):
            if title.strip() or desc.strip():
                steps.append({"title": title.strip(), "desc": desc.strip()})

        recipes[recipe_id] = {
            "title": request.form.get('title', '').strip(),
            "category": request.form.get('category', ''),
            "description": request.form.get('description', '').strip(),
            "servings": request.form.get('servings', '').strip(),
            "protein_per_serving": request.form.get('protein_per_serving', '').strip(),
            "cook_time": request.form.get('cook_time', '').strip(),
            "ingredients": ingredients,
            "steps": steps,
            "notes": request.form.get('notes', '').strip(),
            "image": image_path,
            "created": datetime.now().isoformat(),
        }
        save_recipes(recipes)
        return redirect(url_for('recipe', recipe_id=recipe_id))

    return render_template('new_recipe.html', categories=CATEGORIES)

@app.route('/edit/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipes = load_recipes()
    r = recipes.get(recipe_id)
    if not r:
        return redirect(url_for('index'))

    if request.method == 'POST':
        image_path = r.get('image')
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{recipe_id}_{file.filename}")
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"uploads/{filename}"

        ing_names = request.form.getlist('ing_name[]')
        ing_amounts = request.form.getlist('ing_amount[]')
        ing_units = request.form.getlist('ing_unit[]')
        ingredients = []
        for name, amount, unit in zip(ing_names, ing_amounts, ing_units):
            if name.strip():
                ingredients.append({"name": name.strip(), "amount": amount.strip(), "unit": unit.strip()})

        step_titles = request.form.getlist('step_title[]')
        step_descs = request.form.getlist('step_desc[]')
        steps = []
        for title, desc in zip(step_titles, step_descs):
            if title.strip() or desc.strip():
                steps.append({"title": title.strip(), "desc": desc.strip()})

        recipes[recipe_id].update({
            "title": request.form.get('title', '').strip(),
            "category": request.form.get('category', ''),
            "description": request.form.get('description', '').strip(),
            "servings": request.form.get('servings', '').strip(),
            "prep_time": request.form.get('prep_time', '').strip(),
            "cook_time": request.form.get('cook_time', '').strip(),
            "ingredients": ingredients,
            "steps": steps,
            "notes": request.form.get('notes', '').strip(),
            "image": image_path,
            "updated": datetime.now().isoformat(),
        })
        save_recipes(recipes)
        return redirect(url_for('recipe', recipe_id=recipe_id))

    return render_template('new_recipe.html', categories=CATEGORIES, recipe=r, recipe_id=recipe_id, editing=True)

@app.route('/delete/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipes = load_recipes()
    if recipe_id in recipes:
        del recipes[recipe_id]
        save_recipes(recipes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
