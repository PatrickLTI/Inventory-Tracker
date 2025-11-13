
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
    page.fill("input[name='threshold']", "500")
    page.click("input[value='Add Ingredient']")

    # Add a dish
    page.fill("input[name='dish_name']", "Bread")
    page.click("input[value='Add Dish']")

    # Navigate to the dish page
    page.click("a:text('Manage')")

    # Add the ingredient to the dish
    page.select_option("select[name='ingredient']", label="Flour")
    page.fill("input[name='quantity']", "600")
    page.click("input[value='Add/Update Ingredient']")

    # Go back to the index page
    page.goto("http://127.0.0.1:5000/")

    # Record a sale
    page.select_option("select[name='dish']", label="Bread")
    page.fill("input[name='sale_quantity']", "1")
    page.click("input[value='Record Sale']")

    # Go to the shopping list page
    page.click("a:text('Shopping List')")

    # Take a screenshot to verify
    page.screenshot(path="verification.png")

    # Verify that the ingredient is in the shopping list
    shopping_list_content = page.inner_text('table')
    assert "Flour" in shopping_list_content
    assert "400" in shopping_list_content
    assert "500" in shopping_list_content

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
