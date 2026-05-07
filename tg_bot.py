import feedparser
import requests
import sqlite3
import os
from dotenv import load_dotenv

# For token inputting

# Load telegram environment variables
load_dotenv()

# Recupera i valori
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

urls_raw = os.getenv("CHOSEN_URLS") # if chosen_url is in csv format

if urls_raw: 
    RSS_URLs = urls_raw.split(',')
else:
    RSS_URLs = [ 
        # list your links
    ]

print(RSS_URLs)

for url in RSS_URLs:
    response = requests.get(url)
    print("STATUS:", response.status_code)
    print("CONTENT-TYPE:", response.headers.get("content-type"))
    print("FIRST 500 CARATTERI:\n", response.text[:500])


# Create database
conn = sqlite3.connect("sent_links.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sent_items (
    id TEXT PRIMARY KEY
)
""")
conn.commit()

# Telegram send
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# Chech feed rss
def check_feed():
    
    for url in RSS_URLs:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        feed = feedparser.parse(response.content)
        feed.href = url  
        print("Final URL:", url)
        print("Bozo:", feed.bozo)
        print("Entries Found:", len(feed.entries))
        for entry in feed.entries:
            article_id = f"{url}:{entry.get('id', entry.link)}"

            cursor.execute("SELECT 1 FROM sent_items WHERE id = ?", (article_id,))
            if cursor.fetchone():
                continue 

            message = f"<b>{entry.title}</b>\n{entry.link}" 
            send_message(message)

            cursor.execute("INSERT INTO sent_items (id) VALUES (?)", (article_id,))
            print(f"Entries trovate in {url}", len(feed.entries))
            conn.commit()

if __name__ == "__main__":
    check_feed()
    print("TOKEN:", TELEGRAM_TOKEN)
    print("CHAT_ID:", CHAT_ID)
    
    print("Controllo completato.")