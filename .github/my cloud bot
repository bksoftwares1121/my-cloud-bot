import random
import time
import requests
from playwright.sync_api import sync_playwright

# YOUR LINK IS HERE
TARGET_URL = "https://www.profitableratecpmnetwork.com/xij3bnky?key=799b506ccb29959c50a39b9ab41b3065"

# 5 Different Browser Profiles (User Agents and Screen Sizes)
PROFILES = [
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "vp": {"width": 1920, "height": 1080}},
    {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15", "vp": {"width": 1680, "height": 1050}},
    {"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0", "vp": {"width": 1366, "height": 768}},
    {"ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "vp": {"width": 390, "height": 844}},
    {"ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36", "vp": {"width": 412, "height": 915}}
]

def get_proxies():
    print("Fetching free proxies...")
    try:
        res = requests.get('https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=json', timeout=10)
        data = res.json()
        proxies = [p['proxy'] for p in data['proxies'] if p['protocol'] in ['http', 'https']]
        print(f"Found {len(proxies)} proxies.")
        return proxies
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def run_bot():
    views_completed = 0
    TARGET_VIEWS = 100000  # 100k views

    while views_completed < TARGET_VIEWS:
        proxies = get_proxies()
        if len(proxies) < 5:
            print("Not enough proxies available. Waiting 10 seconds...")
            time.sleep(10)
            continue

        # Shuffle the profiles to randomize the browser order
        shuffled_profiles = random.sample(PROFILES, len(PROFILES))
        used_proxies = set()

        for profile in shuffled_profiles:
            if views_completed >= TARGET_VIEWS:
                break

            # Pick a random unused proxy
            proxy = None
            attempts = 0
            while (proxy is None or proxy in used_proxies) and attempts < 10:
                proxy = random.choice(proxies)
                attempts += 1
            used_proxies.add(proxy)

            print(f"Opening browser {views_completed+1} with proxy {proxy}...")

            try:
                with sync_playwright() as p:
                    # Launch browser
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(
                        user_agent=profile['ua'],
                        viewport=profile['vp'],
                        proxy={"server": f"http://{proxy}"}
                    )
                    page = context.new_page()
                    
                    # Open link
                    page.goto(TARGET_URL, timeout=30000, wait_until="domcontentloaded")
                    
                    # Wait 5 seconds
                    page.wait_for_timeout(5000)
                    
                    # Scroll a random amount
                    scroll_amount = random.randint(100, 800)
                    page.mouse.wheel(0, scroll_amount)
                    page.wait_for_timeout(2000) 

                    browser.close()
                    
                    views_completed += 1
                    print(f"SUCCESS: View {views_completed}/{TARGET_VIEWS} completed.")

            except Exception as e:
                print(f"Proxy {proxy} failed or link timed out. Skipping. Error: {str(e)[:100]}")
                if 'browser' in locals():
                    try: browser.close()
                    except: pass
                continue

if __name__ == "__main__":
    run_bot()
