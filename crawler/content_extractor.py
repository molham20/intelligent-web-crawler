import requests
from bs4 import BeautifulSoup

def scrape_recipe(url):
    try:
        # إضافة headers لتجنب الحظر
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # التحقق من عدم وجود أخطاء HTTP
        
        soup = BeautifulSoup(response.text, 'lxml')  # استخدام lxml parser الأسرع
        
        # البحث بطريقة أكثر مرونة مع التعامل مع حالات العناصر غير الموجودة
        title_elem = soup.find("h1")
        title = title_elem.text.strip() if title_elem else "No title found"
        
        # استخراج المكونات باستخدام CSS Selector محدث
        ingredients = []
        ingredients_container = soup.select_one(".recipe-ingredients__list")
        if ingredients_container:
            ingredients = [li.get_text(strip=True) for li in ingredients_container.find_all("li")]
        
        # استخراج الخطوات
        instructions = []
        instructions_container = soup.select_one(".recipe-directions__list")
        if instructions_container:
            instructions = [step.get_text(strip=True) for step in instructions_container.find_all("li")]
        
        return {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "url": url
        }
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

# مثال محدث للاستخدام:
recipe_url = "https://www.tasteofhome.com/recipes/classic-beef-stew/"
result = scrape_recipe(recipe_url)
print(result)