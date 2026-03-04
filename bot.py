import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
import pytz

# ========= CONFIG =========
CHANNEL_ID = 1478775197116137666  # <-- REPLACE with your channel ID
PING_ROLE_ID = None  # Set to role ID or keep None for @everyone
TIMEZONE = pytz.timezone("Asia/Kolkata")  # IST

# Base reminder times (IST)
BASE_TIMES = [
    time(5, 30),   # 5:30 AM
    time(13, 30),  # 1:30 PM
    time(21, 30),  # 9:30 PM
]
# ==========================

TOKEN = os.getenv("MTQ3ODc3MDU0MzE3NTEzOTU1MA.G5yiqK.xVtQ4mF-6DYiTjyrdZxWFZjUjwXqHmsPYHtwpI")  # Token comes from Railway env var

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    reminder_loop.start()

@tasks.loop(minutes=1)
async def reminder_loop():
    now = datetime.now(TIMEZONE)
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        return

    for base_time in BASE_TIMES:
        reminder_dt = datetime.combine(now.date(), base_time, tzinfo=TIMEZONE) - timedelta(minutes=30)

        # Handle reminders that fall on the previous day
        if reminder_dt > datetime.combine(now.date(), base_time, tzinfo=TIMEZONE):
            reminder_dt -= timedelta(days=1)

        if now.hour == reminder_dt.hour and now.minute == reminder_dt.minute:
            ping = f"<@&{PING_ROLE_ID}>" if PING_ROLE_ID else "@everyone"
            await channel.send(f"{ping} ⏰ Reminder: event in 30 minutes!")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set")

bot.run(TOKEN)