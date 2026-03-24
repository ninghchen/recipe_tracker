# 🍝 La Cucina Mia — Personal Italian Recipe Tracker

A beautiful Mediterranean-themed recipe tracker built with Flask and vanilla HTML/CSS/JS.

## Features
- 8 recipe categories: Pasta, Dessert, Sauces, Creami, Antipasti, Secondi, Zuppe, Pane
- Add ingredients one by one with name, amount, and unit
- Optional photo uploads per recipe
- Edit and delete recipes
- Responsive, Italian Mediterranean color palette

## Setup

### 1. Clone / Download
```bash
git clone <your-repo-url>
cd recipe-tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

## Project Structure
```
recipe-tracker/
├── app.py                  # Flask backend
├── recipes.json            # Recipe data (auto-created)
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/            # Uploaded images (auto-created)
└── templates/
    ├── base.html
    ├── index.html
    ├── category.html
    ├── recipe.html
    └── new_recipe.html
```

## Deploying to GitHub
```bash
git init
git add .
git commit -m "Initial commit: La Cucina Mia recipe tracker"
git remote add origin https://github.com/YOUR_USERNAME/recipe-tracker.git
git push -u origin main
```

> **Note:** Add `recipes.json` and `static/uploads/` to `.gitignore` if you don't want your personal recipes committed.

## .gitignore (recommended)
```
recipes.json
static/uploads/
__pycache__/
*.pyc
.env
```
