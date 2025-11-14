from app import app, db
from app import models

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ingredient': models.Ingredient, 'Dish': models.Dish, 'Sale': models.Sale}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
