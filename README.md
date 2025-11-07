# Telegram Keyword Bot

A Telegram bot that monitors specified public channels and sends messages containing specific keywords.

## 1. Features

* Searches for keywords in channel posts.
* Forwards text and photos from posts containing keywords.
* Asynchronous checking at regular intervals.
* Sends only new posts, avoiding duplicates.

## 2. Technologies Used

* Python 3.12.10
* aiogram
* aiohttp
* BeautifulSoup

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/ledokol11/telegram-keyword-bot.git
   cd telegram-keyword-bot
   ```
2. Navigate to the project folder:

   ```bash
   cd telegram-keyword-bot
   ```
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```
4. In `bot.py`, add your bot token and Telegram ID.
5. Run the bot:

   ```bash
   python bot.py
   ```


