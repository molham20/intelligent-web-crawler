import requests
from urllib.robotparser import RobotFileParser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def analyze_robots():
    try:
        url = "https://www.tasteofhome.com/robots.txt"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        rp = RobotFileParser()
        rp.parse(response.text.splitlines())
        
        print(f"Can crawl /recipes/: {rp.can_fetch('*', 'https://www.tasteofhome.com/recipes/')}")
        return rp
    except Exception as e:
        print(f"Failed to analyze robots.txt: {e}")
        return None

analyze_robots()