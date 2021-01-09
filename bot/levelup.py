from discord.ext import commands
import sqlite3


class LevelUpCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def my_stats(self, ctx):
        db = sqlite3.connect('user_levels.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, XP, level FROM user_levels WHERE "
                       f"user_id = {str(ctx.message.author.id)}")
        exists = cursor.fetchone()
        if exists is None:
            await ctx.send("You have not yet answered any questions correctly")
        else:
            await ctx.send(f"{str(ctx.message.author.name)} is "
                           f"currently at level {str(exists[2])} "
                           f"and has answered {str(exists[1])} "
                           f"questions correctly.")
        cursor.close()
        db.close()


def setup(client):
    client.add_cog(LevelUpCog(client))
