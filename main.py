import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import datetime
from datetime import time
import pytz
import random
import asyncio
import os
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is alive!")

async def run_webserver():
    app = web.Application()
    app.add_routes([web.get("/", handle)])

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))  # Render provides PORT
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Webserver running on port {port}")


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
channel_id = int(os.getenv('CHANNEL_ID'))
timezone = pytz.timezone(os.getenv('TIMEZONE'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class BirthdayBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(run_webserver())

bot = BirthdayBot(command_prefix="!", intents=intents)

birthdays = {
    'Angel': {
        "date": (12, 5),
        "year": 2001,
        "id": 748267581659545631,
        "older": True
    },
    'Anthony': {
        "date": (10, 26),
        "year": 2002,
        "id": 245914395534819328,
        "older": False
    },
    'Human Bio-Diversity Bot': {
        "date": (7, 27),
        "year": 2025,
        "id": 1399037133867581491,
        "older": False
    },
    'Eric': {
        "date": (5, 3),
        "year": 2002,
        "id": 197099924947468288,
        "older": True
    },
    'Erik': {
        "date": (3, 12),
        "year": 2000,
        "id": 400165422810267660,
        "older": True
    },
    'Felix': {
        "date": (1, 20),
        "year": 2004,
        "id": 293026730250076162,
        "older": False
    },
    'Jacob': {
        "date": (8, 15),
        "year": 2002,
        "id": 272961486031421441,
        "older": True
    },
    'Joey': {
        "date": (1, 15),
        "year": 2002,
        "id": 209663987233587200,
        "older": True
    },
    'Nick': {
        "date": (5, 5),
        "year": 2001,
        "id": 277939122214010880,
        "older": True
    },
    'Other Max': {
        "date": (8, 15),
        "year": 1999,
        "id": 273278542253391872,
        "older": True
    },
    'Rahm': {
        "date": (1, 6),
        "year": 2004,
        "id": 314190486409576448,
        "older": False
    },
    'Tyler': {
        "date": (7, 21),
        "year": 2002,
        "id": 226030330706919424,
        "older": True
    },
}

greeted_today = set()


def ordinal(n):
    match n % 10:
        case 1:
            return f"{n}st"
        case 2:
            return f"{n}nd"
        case 3:
            return f"{n}rd"
        case _:
            return f"{n}th"


@bot.event        
async def on_ready():
    message = f'{bot.user.name} has started running!'
    print(message)

    if not scheduled_message_loop.is_running():
        scheduled_message_loop.start()


@bot.command()
async def info(ctx):
    await ctx.send(f"HBD! I Am {bot.user.name}!")
    await ctx.send("I give information about people's birthdays!")


@bot.command()
async def mentionroulette(ctx):
    random_person = random.choice(list(birthdays.values()))
    await ctx.send(f"<@{random_person['id']}>")


@tasks.loop(time=[
    time(hour=0, minute=0, tzinfo=timezone),
    time(hour=6, minute=0, tzinfo=timezone),
    time(hour=12, minute=0, tzinfo=timezone),
    time(hour=18, minute=0, tzinfo=timezone)
])
async def scheduled_message_loop():
    now = datetime.datetime.now(timezone)
    print(f'{bot.user.name} starting search process at {now}!')
    if now.hour == 0:
        greeted_today.clear()

    today = (now.month, now.day)
    channel = bot.get_channel(channel_id)
    if not channel:
        print('Channel not found')
        return

    for name, info in birthdays.items():
        if info['date'] == today and name not in greeted_today:
            user_mention = f"<@{info['id']}>"
            age = now.year - info['year']

            if name == 'Angel' or name == 'Nick':
                await channel.send(f'{user_mention} ¡Feliz Cumpleaños {name}!')
            elif name == 'Rahm':
                await channel.send(f'{user_mention} Happy {ordinal(age)} Birthday!')
            else:
                await channel.send(f'{user_mention} Happy {ordinal(age)} Birthday {name}!')

            greeted_today.add(name)

    print(f'{bot.user.name} finished searching for session {now}!')


bot.run(token)
