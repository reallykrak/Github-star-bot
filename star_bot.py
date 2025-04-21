import requests
import time
import random
import json
from config import GITHUB_TOKEN, PROXIES, CAPTCHA_API_KEY, REPO_URL

# GitHub API Header
headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Proxy ile istek atma
def get_proxy():
    return random.choice(PROXIES)

# 2Captcha ile captcha çözme
def solve_captcha(api_key, page_url):
    url = "http://2captcha.com/in.php"
    payload = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": "YOUR_GOOGLE_RECAPTCHA_SITE_KEY",
        "pageurl": page_url
    }
    
    response = requests.post(url, data=payload)
    captcha_id = response.text.split('|')[1]
    
    solution_url = f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}'
    solution = requests.get(solution_url).text
    return solution

# Star atma işlemi
def star_repo():
    # Proxy ayarı
    proxy = get_proxy()
    proxies = {"http": proxy, "https": proxy}
    
    response = requests.put(f"{REPO_URL}/stargazers", headers=headers, proxies=proxies)
    
    if response.status_code == 204:
        print("Star başarıyla atıldı!")
    else:
        print(f"Star atılamadı, durum kodu: {response.status_code}")
        # Eğer captcha varsa çözme işlemi
        if "captcha" in response.text.lower():
            print("Captcha tespit edildi, çözülüyor...")
            captcha_solution = solve_captcha(CAPTCHA_API_KEY, REPO_URL)
            print(f"Captcha çözüldü: {captcha_solution}")
            # Captcha'yı geçtikten sonra tekrar deneyebilirsiniz.
            star_repo()

# Rastgele bir bekleme süresi ile işlemi yap
def wait_before_star():
    wait_time = random.randint(10, 30)
    time.sleep(wait_time)

# Botu başlat
def start_bot():
    while True:
        star_repo()
        wait_before_star()  # Her yıldız atma işleminden sonra rastgele bekleme süresi
        print(f"{time.ctime()} - Yeni bir yıldız atıldı.")

if __name__ == "__main__":
    start_bot()
