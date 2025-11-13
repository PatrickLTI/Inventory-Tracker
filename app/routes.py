from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Ingredient, Dish, Sale, dish_ingredients

@app.route('/')
def index():
    ingredients = Ingredient.query.all()
    dishes = Dish.query.all()
    sales = Sale.query.all()
    return render_template('index.html', title='Home', ingredients=ingredients, dishes=dishes, sales=sales)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    name = request.form['ingredient_name']
    quantity = request.form['quantity']
    unit = request.form['unit']
    ingredient = Ingredient(name=name, quantity=quantity, unit=unit)
    db.session.add(ingredient)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_dish', methods=['POST'])
def add_dish():
    name = request.form['dish_name']
    dish = Dish(name=name)
    db.session.add(dish)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/dish/<int:dish_id>')
def dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    ingredients = Ingredient.query.all()

    dish_ingredient_associations = db.session.query(dish_ingredients).filter_by(dish_id=dish.id).all()
    ingredient_quantities = {assoc.ingredient_id: assoc.quantity for assoc in dish_ingredient_associations}

    return render_template('dish.html', dish=dish, ingredients=ingredients, ingredient_quantities=ingredient_quantities)

@app.route('/dish/<int:dish_id>/add_ingredient', methods=['POST'])
def add_ingredient_to_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    ingredient_id = int(request.form['ingredient'])
    quantity = int(request.form['quantity'])

    # Check if the association already exists
    association = db.session.query(dish_ingredients).filter_by(dish_id=dish_id, ingredient_id=ingredient_id).first()

    if association:
        # Update the quantity if the association exists
        stmt = db.update(dish_ingredients).where(
            db.and_(dish_ingredients.c.dish_id == dish_id, dish_ingredients.c.ingredient_id == ingredient_id)
        ).values(quantity=quantity)
        db.session.execute(stmt)
    else:
        # Create a new association if it does not exist
        stmt = db.insert(dish_ingredients).values(dish_id=dish_id, ingredient_id=ingredient_id, quantity=quantity)
        db.session.execute(stmt)

    db.session.commit()

    return redirect(url_for('dish', dish_id=dish_id))

@app.route('/record_sale', methods=['POST'])
def record_sale():
    dish_id = request.form['dish']
    quantity = int(request.form['sale_quantity'])

    sale = Sale(dish_id=dish_id, quantity=quantity)
    db.session.add(sale)

    dish = Dish.query.get(dish_id)

    # Get all the ingredient associations for this dish
    dish_ingredient_associations = db.session.query(dish_ingredients).filter_by(dish_id=dish.id).all()

    for association in dish_ingredient_associations:
        ingredient = Ingredient.query.get(association.ingredient_id)
        ingredient.quantity -= association.quantity * quantity

    db.session.commit()

    return redirect(url_for('index'))
