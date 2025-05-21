from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json

def scrape_recipe_card(url):
    driver = None
    try:
        print("🚀 جارِ إعداد المتصفح...")
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')

        service = Service(EdgeChromiumDriverManager().install())
        service.creationflags = 0x08000000

        driver = webdriver.Edge(service=service, options=options)

        print(f"🌐 جارِ تحميل: {url}")
        driver.get(url)

        # تأكد من وجود العنوان
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        def safe_get(selector):
            try:
                el = driver.find_element(By.CSS_SELECTOR, selector)
                return el.text.strip()
            except:
                return "غير متوفر"

        # ✅ تحديث الـ Selectors للمكونات والخطوات
        ingredients = driver.find_elements(By.CSS_SELECTOR, ".recipe-ingredients__list li")
        directions = driver.find_elements(By.CSS_SELECTOR, ".recipe-directions__list li")

        recipe_data = {
            "title": safe_get("h1"),
            "description": safe_get(".recipe-description"),
            "prep_time": safe_get(".prep-time .time-amount"),
            "cook_time": safe_get(".cook-time .time-amount"),
            "ingredients": [el.text.strip() for el in ingredients if el.text.strip()],
            "directions": [el.text.strip() for el in directions if el.text.strip()],
        }

        with open("recipe_data.json", "w", encoding="utf-8") as f:
            json.dump(recipe_data, f, ensure_ascii=False, indent=4)

        print("✅ تم استخراج الوصفة بنجاح!")
        print(f"📋 العنوان: {recipe_data['title']}")
        print(f"🛒 عدد المكونات: {len(recipe_data['ingredients'])}")
        print(f"👩‍🍳 عدد الخطوات: {len(recipe_data['directions'])}")
        return recipe_data

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()
            print("🧹 تم إغلاق المتصفح")

if __name__ == "__main__":
    recipe_url = "https://www.tasteofhome.com/recipes/the-best-beef-stew/"
    result = scrape_recipe_card(recipe_url)

    if result:
        print("\n🎉 تم الانتهاء بنجاح! يمكنك فحص ملف recipe_data.json")
