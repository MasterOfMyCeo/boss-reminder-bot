import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
import pytz

# ===== CONFIG =====
TOKEN = "MTQ3ODc3MDU0MzE3NTEzOTU1MA.Gb6kJR.rU48tsU4I9-6GDNFwFItQL23EPAgaCnllnLH64"
CHANNEL_ID = 1478775197116137666  # replace with your channel ID
PING_ROLE_ID = None  # set role ID to ping a role, or leave None to @everyone
TIMEZONE = pytz.timezone("Asia/Kolkata")  # IST

# Base times in IST
BASE_TIMES = [
    time(5, 30),   # 5:30 AM
    time(13, 30),  # 1:30 PM
    time(21, 30),  # 9:30 PM
]
# ==================

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

    for base_time in BASE_TIMES:
        reminder_dt = datetime.combine(now.date(), base_time, tzinfo=TIMEZONE) - timedelta(minutes=30)

        # handle reminders that fall on previous day
        if reminder_dt.hour > base_time.hour:
            reminder_dt -= timedelta(days=1)

        if now.hour == reminder_dt.hour and now.minute == reminder_dt.minute:
            if PING_ROLE_ID:
                ping = f"<@&{PING_ROLE_ID}>"
            else:
                ping = "@everyone"

            await channel.send(f"{ping} ⏰ Reminder: event in 30 minutes!")

bot.run(TOKEN)
