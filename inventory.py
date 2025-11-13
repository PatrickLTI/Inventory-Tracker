from app import app, db
from app.models import Ingredient, Dish, Sale

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ingredient': Ingredient, 'Dish': Dish, 'Sale': Sale}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
