from products import PRODUCTS_TO_MONITOR
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
import requests
import random
import time
import re
import undetected_chromedriver as uc
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID_FILE = os.getenv("CHAT_ID_FILE")


def get_registered_chat_ids():
    try:
        with open(CHAT_ID_FILE, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    registered_chat_ids = get_registered_chat_ids()

    if chat_id not in registered_chat_ids:
        with open(CHAT_ID_FILE, "a") as file:
            file.write(chat_id + "\n")
        await update.message.reply_text("✅ Sei stato registrato! Riceverai notifiche sugli sconti.")
    else:
        await update.message.reply_text("ℹ️ Sei già registrato per ricevere notifiche.")


async def launch_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Avvio del monitoraggio dei prezzi...")
    main()


def start_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", register_user))
    application.add_handler(CommandHandler("launch", launch_script))

    application.run_polling()


def get_price(url):
    service = Service(ChromeDriverManager().install())
    driver = uc.Chrome()

    try:
        driver.get(url)

        actions = ActionChains(driver)
        actions.move_by_offset(10, 10).perform()

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0"
        ]

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        price_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-qa="productpage-product-price"]'))
        )

        price_text = price_element.text.strip()
        price_text = re.sub(r"[^\d,]", "", price_text)
        price_text = price_text.replace(",", ".")
        price = float(price_text)

        print(f"Prezzo trovato per {url}: €{price}")
        return price

    except Exception as e:
        print(f"Errore nel web scraping per {url}:", e)
        return None

    finally:
        driver.quit()

def send_telegram_message(message):
    chat_ids = get_registered_chat_ids()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for chat_id in chat_ids:
        payload = {"chat_id": chat_id, "text": message}
        requests.post(url, json=payload)


def main():
    for product_name, product_data in PRODUCTS_TO_MONITOR.items():
        url = product_data["url"]
        target_price = product_data["target_price"]

        print(f"Controllando prezzo per: {product_name}")
        price = get_price(url)

        if price is None:
            print(f"Impossibile ottenere il prezzo per {product_name}")
        elif price < target_price:
            message = f"💰 {product_name} in offerta! Ora costa €{price}\nLink: {url}"
            send_telegram_message(message)
            print(f"Notifica inviata su Telegram per {product_name}!")
        else:
            message = f"💰 {product_name} non è variato. Prezzo €{price}\nLink: {url}"
            send_telegram_message(message)
            print(f"Il prezzo di {product_name} è ancora alto: €{price}")

        time.sleep(random.randint(10, 15))


if __name__ == "__main__":
    start_bot()
