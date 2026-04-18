import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env
load_dotenv()

# Bot Intents definieren (erforderlich für discord.py 2.0+)
intents = discord.Intents.default()
intents.message_content = True

# Bot mit Präfix erstellen
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot ist bereit
@bot.event
async def on_ready():
    print(f'{bot.user} ist verbunden mit Discord!')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="!help für Befehle"))

# Event: Neue Nachricht
@bot.event
async def on_message(message):
    # Ignoriere Nachrichten vom Bot selbst
    if message.author == bot.user:
        return

    # Verarbeite Befehle
    await bot.process_commands(message)

# Command: ping
@bot.command(name='ping', help='Zeigt die Bot-Latenz')
async def ping(ctx):
    latency = bot.latency * 1000  # in Millisekunden
    await ctx.send(f'🏓 Pong! Latenz: {latency:.2f}ms')

# Command: hello
@bot.command(name='hello', help='Der Bot grüßt dich')
async def hello(ctx):
    await ctx.send(f'Hallo {ctx.author.mention}! 👋')

# Command: info
@bot.command(name='info', help='Zeigt Bot-Informationen')
async def info(ctx):
    embed = discord.Embed(
        title="Bot Information",
        description="Ein einfacher Discord Bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="Bot Name", value=bot.user, inline=False)
    embed.add_field(name="Guild Count", value=len(bot.guilds), inline=False)
    embed.add_field(name="User Count", value=sum(g.member_count for g in bot.guilds), inline=False)
    await ctx.send(embed=embed)

# Starte den Bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Fehler: DISCORD_TOKEN nicht in .env gefunden!")
    else:
        bot.run(token)
