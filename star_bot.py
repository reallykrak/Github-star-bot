import requests
import time
from datetime import datetime, timedelta
from collections import defaultdict
from config import repo_owner, repo_name, tokens

# Geçici bloklama için
block_until = None
star_logs = defaultdict(list)

# GitHub API URL'si
api_url = f"https://api.github.com/user/starred/{repo_owner}/{repo_name}"

# Yıldızları takip etme fonksiyonu
def track_stars():
    global block_until
    now = datetime.utcnow()

    # Eğer bloklama aktifse
    if block_until and now < block_until:
        print(f"[+] Bot saldırısı algılandı! Repo 1 saat boyunca bloklandı.")
        return

    for token in tokens:
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Yıldız verme isteği
        response = requests.put(api_url, headers=headers)
        
        if response.status_code == 204:
            print(f"[+] Star atıldı: {token[:10]}...")
            star_logs[now.minute].append(token)
        else:
            print(f"[-] Başarısız ({response.status_code}): {token[:10]}...")

    # Son 1 dakika içindeki yıldızları kontrol et
    recent_stars = [t for t in star_logs if (now - datetime(now.year, now.month, now.day, now.hour, t)).total_seconds() <= 60]
    total_stars = sum(len(star_logs[t]) for t in recent_stars)

    # 10'dan fazla yıldız gelirse, repo'yu blokla
    if total_stars >= 10:
        print("!! BOT ALGILANDI. Repo geçici olarak 1 saatlik süreyle bloklandı.")
        block_until = now + timedelta(hours=1)

    # Bir saniye bekleyerek rate limit problemi yaşamamak için
    time.sleep(1)

# Test süreci: Sürekli yıldız atma işlemi yapmak
while True:
    track_stars()
