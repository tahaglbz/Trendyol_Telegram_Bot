import requests as rq
from bs4 import BeautifulSoup
import streamlit as st
import time

# Streamlit UI
st.title("Create Telegram Bot For Tracking Trendyol Products")

# Input fields for bot token, chat ID, and product URL
bot_token = st.text_input("Enter your Telegram bot token", type="password")
chat_id = st.text_input("Enter your Telegram chat ID")
product_url = st.text_input("Enter the Trendyol product URL")

# Function to scrape the product title and latest price
def get_product_details(url):
    page = rq.get(url)
    html_page = BeautifulSoup(page.content, "html.parser")
    title = html_page.find("h1", class_="pr-new-br").getText()
    latest_price = html_page.find("span", class_="prc-dsc").getText()
    return title, latest_price

# Function to send message to Telegram
def send_telegram_message(token, chat_id, message):
    api = f"https://api.telegram.org/bot{token}/sendMessage"
    rq.post(url=api, data={"chat_id": chat_id, "text": message}).json()

# Button to start tracking
if st.button("Start Tracking"):
    if bot_token and chat_id and product_url:
        while True:
            title, latest_price = get_product_details(product_url)
            st.write(f"Product: {title}")
            st.write(f"Latest Price: {latest_price}")
            
            message = f"{title}\nLatest Price: {latest_price}"
            send_telegram_message(bot_token, chat_id, message)
            
            # Wait 24 hours before next update
            time.sleep(86400)
    else:
        st.error("Please provide all inputs")
