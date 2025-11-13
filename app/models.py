from app import db

dish_ingredients = db.Table('dish_ingredients',
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    quantity = db.Column(db.Integer, index=True)
    unit = db.Column(db.String(64), index=True)
    threshold = db.Column(db.Integer, index=True, default=0)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    ingredients = db.relationship(
        'Ingredient', secondary=dish_ingredients,
        backref=db.backref('dishes', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Dish {self.name}>'

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'))
    quantity = db.Column(db.Integer)
    dish = db.relationship('Dish', backref='sales')

    def __repr__(self):
        return f'<Sale {self.dish.name} - {self.quantity}>'
