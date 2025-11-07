from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import aiohttp
from bs4 import BeautifulSoup

API_TOKEN = "YOUR_TOKEN_HERE"
YOUR_TELEGRAM_ID = 123456789  # replace with your numeric Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔍 Keywords to search for
KEYWORDS = ["coffee", "sunset", "travel", "books", "music", "python", "art", "fitness"]

# 📡 List of channels (replace with actual public channels if needed)
CHANNELS = [
    # Add channel links here, e.g. "https://t.me/channel_name"
]

# File to store already sent posts
SENT_FILE = "sent_posts.txt"

# Load already sent posts
try:
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        sent_posts = set(f.read().splitlines())
except FileNotFoundError:
    sent_posts = set()

async def check_channels():
    async with aiohttp.ClientSession() as session:
        for channel in CHANNELS:
            channel_name = channel.split("/")[-1]
            try:
                async with session.get(f"https://t.me/s/{channel_name}") as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    posts = soup.find_all("div", class_="tgme_widget_message_wrap")
                    for post in posts:
                        post_url_tag = post.find("a", class_="tgme_widget_message_date")
                        if not post_url_tag:
                            continue
                        post_url = post_url_tag["href"]
                        if post_url in sent_posts:
                            continue

                        post_text_tag = post.find("div", class_="tgme_widget_message_text")
                        post_text = post_text_tag.get_text(strip=True) if post_text_tag else ""

                        # Check for keywords
                        if any(word.lower() in post_text.lower() for word in KEYWORDS):
                            # Find photos
                            photo_tags = post.find_all("a", class_="tgme_widget_message_photo_wrap")
                            photos = [tag["href"] for tag in photo_tags if tag.get("href")]

                            # Send message
                            try:
                                if photos:
                                    media = [types.InputMediaPhoto(media=url) for url in photos]
                                    await bot.send_media_group(YOUR_TELEGRAM_ID, media)
                                    if post_text:
                                        await bot.send_message(YOUR_TELEGRAM_ID, f"📩 {post_text}\n{post_url}")
                                else:
                                    await bot.send_message(YOUR_TELEGRAM_ID, f"📩 {post_text}\n{post_url}")
                                sent_posts.add(post_url)
                                # Save post URL to file
                                with open(SENT_FILE, "a", encoding="utf-8") as f:
                                    f.write(post_url + "\n")
                            except Exception as e:
                                print(f"⚠️ Error sending post {post_url}: {e}")

            except Exception as e:
                print(f"⚠️ Error processing {channel_name}: {e}")

async def scheduler():
    while True:
        await check_channels()
        await asyncio.sleep(3600)  # check every hour

# /start command
@dp.message(Command(commands=["start"]))
async def start_cmd(msg: types.Message):
    await msg.answer("👋 Bot started! I will search for keywords in the specified channels.")

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
