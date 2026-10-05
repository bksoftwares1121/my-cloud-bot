import random, time, requests
from playwright.sync_api import sync_playwright

# CHANGE THIS LINK TO YOUR TARGET LINK
TARGET_URL = "https://example.com" 

PROFILES = [
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "vp": {"width": 1920, "height": 1080}},
    {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15", "vp": {"width": 1680, "height": 1050}},
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0", "vp": {"width": 1366, "height": 768}},
    {"ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "vp": {"width": 390, "height": 844}},
    {"ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", "vp": {"width": 412, "height": 915}}
]

def get_proxies():
    try:
        res = requests.get('https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=json')
        return [p['proxy'] for p in res.json()['proxies'] if p['protocol'] in ['http', 'https']]
    except: return []

views = 0
while views < 1000:
    proxies = get_proxies()
    if len(proxies) < 5: 
        time.sleep(10)
        continue
    
    for profile in random.sample(PROFILES, len(PROFILES)):
        proxy = random.choice(proxies)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                ctx = browser.new_context(user_agent=profile['ua'], viewport=profile['vp'], proxy={"server": f"http://{proxy}"})
                page = ctx.new_page()
                page.goto(TARGET_URL, timeout=30000)
                page.wait_for_timeout(5000)
                page.mouse.wheel(0, random.randint(100, 800))
                browser.close()
                views += 1
                print(f"View {views}/1000")
        except Exception as e:
            print(f"Proxy failed, skipping.")
print("1000 views done.")
