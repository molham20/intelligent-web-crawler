from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json
import time

def scrape_recipe_card(url):
    driver = None
    try:
        print("🚀 Setting up browser...")
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')

        service = Service(EdgeChromiumDriverManager().install())
        service.creationflags = 0x08000000

        driver = webdriver.Edge(service=service, options=options)

        print(f"🌐 Loading: {url}")
        driver.get(url)
        time.sleep(3)  # Additional wait for JavaScript content

        # Wait for important elements
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        def safe_get(selector, default="غير متوفر"):
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                return el.text.strip()
            except:
                return default

        # Updated selectors with fallbacks
        ingredients = []
        ingredients_container = driver.find_elements(By.CSS_SELECTOR, ".recipe-ingredients__list li, .ingredients li, [data-testid='ingredient-item']")
        if ingredients_container:
            ingredients = [el.text.strip() for el in ingredients_container if el.text.strip()]
        else:
            # Fallback for different site structure
            ingredients = [el.text.strip() for el in driver.find_elements(By.XPATH, "//*[contains(text(), 'Ingredient')]/following-sibling::ul//li")]

        directions = []
        directions_container = driver.find_elements(By.CSS_SELECTOR, ".recipe-directions__list li, .instructions li, [data-testid='instruction-step']")
        if directions_container:
            directions = [el.text.strip() for el in directions_container if el.text.strip()]
        else:
            # Fallback for different site structure
            directions = [el.text.strip() for el in driver.find_elements(By.XPATH, "//*[contains(text(), 'Instruction')]/following-sibling::ol//li")]

        recipe_data = {
            "title": safe_get("h1", "Untitled Recipe"),
            "description": safe_get(".recipe-description, .recipe-summary, [data-testid='recipe-description']"),
            "prep_time": safe_get(".prep-time .time-amount, [data-testid='prep-time']"),
            "cook_time": safe_get(".cook-time .time-amount, [data-testid='cook-time']"),
            "ingredients": ingredients,
            "directions": directions,
        }

        with open("recipe_data.json", "w", encoding="utf-8") as f:
            json.dump(recipe_data, f, ensure_ascii=False, indent=4)

        print("✅ Recipe extracted successfully!")
        print(f"📋 Title: {recipe_data['title']}")
        print(f"🛒 Ingredients count: {len(recipe_data['ingredients'])}")
        print(f"👩‍🍳 Steps count: {len(recipe_data['directions'])}")
        return recipe_data

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()
            print("🧹 Browser closed")

if __name__ == "__main__":
    recipe_url = "https://www.tasteofhome.com/recipes/the-best-beef-stew/"
    result = scrape_recipe_card(recipe_url)

    if result:
        print("\n🎉 Success! Check recipe_data.json")