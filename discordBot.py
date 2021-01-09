from discord.ext import commands

from bot.checklist import CheckListCog
from bot.levelup import LevelUpCog
from bot.quiz import QuizCog
from bot.wiki import WikiCog
from bot.reminder import ReminderCog
from bot.dictionary import DictionaryCog
from secret import secret
import sqlite3

# from bot.translation import TranslationCog

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    db = sqlite3.connect('user_levels.sqlite')
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_levels(
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        XP TEXT,
        level TEXT)
        """)
    client.add_cog(QuizCog(client))
    client.add_cog(WikiCog(client))
    client.add_cog(ReminderCog(client))
    client.add_cog(DictionaryCog(client))
    client.add_cog(CheckListCog(client))
    client.add_cog(LevelUpCog(client))
    # client.add_cog(TranslationCog(client))
    print('Bot is online')


@client.command()
async def logout(ctx):
    await ctx.send("Shutting down the bot")
    return await client.logout()  # this just shuts down the bot.


client.run(secret.DISCORD_BOT_TOKEN)
