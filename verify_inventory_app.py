
import os
import subprocess
from playwright.sync_api import sync_playwright

# Define the path to the database file
db_path = os.path.join('instance', 'inventory.db')

# Delete the database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Run database migrations
subprocess.run(['flask', 'db', 'upgrade'])

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Go to the app
    page.goto("http://127.0.0.1:5000/")

    # Add an ingredient
    page.fill("input[name='ingredient_name']", "Flour")
    page.fill("input[name='quantity']", "1000")
    page.fill("input[name='unit']", "grams")
    page.click("input[value='Add Ingredient']")

    # Add a dish
    page.fill("input[name='dish_name']", "Bread")
    page.click("input[value='Add Dish']")

    # Navigate to the dish page
    page.click("a:text('Bread')")

    # Add the ingredient to the dish
    page.select_option("select[name='ingredient']", label="Flour")
    page.fill("input[name='quantity']", "200")
    page.click("input[value='Add Ingredient']")

    # Take a screenshot to verify
    page.screenshot(path="/home/jules/verification/verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
