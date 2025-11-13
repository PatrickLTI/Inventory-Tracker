
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

    # Update the ingredient quantity directly
    flour_row = page.locator('tr:has-text("Flour")')
    flour_row.locator('input[name="new_quantity"]').fill("1500")
    flour_row.locator('input[type="submit"]').click()

    # Verify that the quantity has been updated on the page
    ingredients_table_content_after_update = page.inner_text('h2:has-text("Ingredients") + table')
    assert "1500" in ingredients_table_content_after_update

    # Add a dish
    page.fill("input[name='dish_name']", "Bread")
    page.click("input[value='Add Dish']")

    # Navigate to the dish page
    page.click("a:text('Manage')")

    # Add the ingredient to the dish
    page.select_option("select[name='ingredient']", label="Flour")
    page.fill("input[name='quantity']", "200")
    page.click("input[value='Add/Update Ingredient']")

    # Go back to the index page
    page.goto("http://127.0.0.1:5000/")

    # Record a sale
    page.select_option("select[name='dish']", label="Bread")
    page.fill("input[name='sale_quantity']", "2")
    page.click("input[value='Record Sale']")

    # Take a screenshot to verify
    page.screenshot(path="verification.png")

    # Verify that the ingredient quantity has been updated
    # Get the text content of the ingredients table
    ingredients_table_content = page.inner_text('h2:has-text("Ingredients") + table')
    assert "Flour" in ingredients_table_content
    assert "1100" in ingredients_table_content
    assert "grams" in ingredients_table_content

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
