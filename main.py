import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.members = True
intents.bans = True
intents.emojis = True
intents.integrations = True
intents.webhooks = True
intents.invites = True
intents.voice_states = True
intents.messages = True
intents.message_content = True
intents.guild_scheduled_events = True
intents.auto_moderation = True  # enables both config and execution

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready and online!")

@bot.command(name='start')
async def start_wager(ctx, wager_name: str, opponent: discord.Member):
    author = ctx.author
    amount = 10  # You forgot to define 'amount', so define it here or make it dynamic

    # Notify public channel once
    await ctx.send(f"New wager `{wager_name}` started between {author.mention} and {opponent.mention}!\n"
                   f"DMs have been sent with payment instructions.")

    # Dummy PayPal.Me links (replace 'yourlink' with your actual PayPal.Me username)
    author_paypal_link = f"https://paypal.me/Level20Discord/10"
    opponent_paypal_link = f"https://paypal.me/Level20Discord/10"

    # Try DMing both users
    try:
        await author.send(f"🧾 Please complete your wager payment: {author_paypal_link}")
    except discord.Forbidden:
        await ctx.send(f"❌ Couldn't DM {author.mention}. Please enable DMs from server members.")

    try:
        await opponent.send(f"🧾 Please complete your wager payment: {opponent_paypal_link}")
    except discord.Forbidden:
        await ctx.send(f"❌ Couldn't DM {opponent.mention}. Please enable DMs from server members.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
