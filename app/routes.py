from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Ingredient, Dish, Sale, DishIngredient

@app.route('/')
def index():
    ingredients = Ingredient.query.all()
    dishes = Dish.query.all()
    sales = Sale.query.all()
    return render_template('index.html', ingredients=ingredients, dishes=dishes, sales=sales)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    name = request.form['ingredient_name']
    quantity = request.form['quantity']
    unit = request.form['unit']
    new_ingredient = Ingredient(name=name, quantity=quantity, unit=unit)
    db.session.add(new_ingredient)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_dish', methods=['POST'])
def add_dish():
    name = request.form['dish_name']
    new_dish = Dish(name=name)
    db.session.add(new_dish)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/dish/<int:dish_id>')
def dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    ingredients = Ingredient.query.all()
    return render_template('dish.html', dish=dish, ingredients=ingredients)

@app.route('/dish/<int:dish_id>/add_ingredient', methods=['POST'])
def add_ingredient_to_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    ingredient_id = request.form['ingredient']
    quantity = request.form['quantity']
    dish_ingredient = DishIngredient(dish_id=dish.id, ingredient_id=ingredient_id, quantity=quantity)
    db.session.add(dish_ingredient)
    db.session.commit()
    return redirect(url_for('dish', dish_id=dish_id))

@app.route('/record_sale', methods=['POST'])
def record_sale():
    dish_id = request.form['dish']
    quantity = int(request.form['quantity'])
    dish = Dish.query.get(dish_id)

    for item in dish.ingredients:
        item.ingredient.quantity -= item.quantity * quantity

    sale = Sale(dish_id=dish_id, quantity=quantity)
    db.session.add(sale)
    db.session.commit()
    return redirect(url_for('index'))
