import requests as rq
from bs4 import BeautifulSoup
import streamlit as st

# Streamlit UI
st.title("Create Telegram Bot For Tracking Trendyol Products")

# Information text in English
st.markdown("""
## How to Create a Telegram Bot

1. **Open Telegram**: Open your Telegram app or use the [web version](https://web.telegram.org/).

2. **Contact BotFather**: Search for and open **@BotFather** on Telegram. BotFather is the official Telegram bot that helps you create and manage new bots.

3. **Create a New Bot**: 
   - Send the command ` /newbot`.
   - Enter a name for your bot (e.g., "My Trendyol Tracker").
   - Enter a username for your bot (e.g., "my_trendyol_tracker_bot"). The username must end with "bot".

4. **Get Your Token**: BotFather will send you a message containing your bot's API token. Copy this token and use it in your application later.

5. **Find Your Chat ID**:
   - Search for your bot on Telegram and send a message.
   - Paste the following URL into your browser, replacing `YOUR_TOKEN` with your bot's token:
     ```
     https://api.telegram.org/botYOUR_TOKEN/getUpdates
     ```
   - Look for the JSON response containing your sent message. Note the `chat_id` value.

6. **Using the Bot**: Enter the token and chat ID in the fields above, then add the Trendyol product URL. Click the "Check Price and Send Telegram Message" button to send a message to your bot.
""")

# Input fields for bot token, chat ID, and product URL
bot_token = st.text_input("Enter your Telegram bot token", type="password")
chat_id = st.text_input("Enter your Telegram chat ID")
product_url = st.text_input("Enter the Trendyol product URL")

# Function to scrape the product title and latest price
def get_product_details(url):
    try:
        page = rq.get(url)
        html_page = BeautifulSoup(page.content, "html.parser")
        title = html_page.find("h1", class_="pr-new-br").getText()
        latest_price = html_page.find("span", class_="prc-dsc").getText()
        return title, latest_price
    except Exception as e:
        st.error(f"Error fetching product details: {e}")
        return None, None

# Function to send message to Telegram
def send_telegram_message(token, chat_id, message):
    api = f"https://api.telegram.org/bot{token}/sendMessage"
    response = rq.post(url=api, data={"chat_id": chat_id, "text": message})
    return response.json()

# Button to check the product price and send the message
if st.button("Check Price and Send Telegram Message"):
    if bot_token and chat_id and product_url:
        title, latest_price = get_product_details(product_url)
        if title and latest_price:
            # Prepare the message to be sent
            message = f"Product: {title}\nLatest Price: {latest_price}"
            # Send message to Telegram
            send_telegram_message(bot_token, chat_id, message)
            st.success("Message sent to Telegram successfully!")
        else:
            st.error("Could not fetch product details.")
    else:
        st.error("Please provide all inputs.")
