import wikipedia
import discord
from discord.ext import commands


def get_wiki_info(topic):
    """

    :param topic:
    :return:
    """
    return wikipedia.summary(topic, sentences=5)


class WikiCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(caseinsensitive=True, aliases=['wiki', 'wikipedia'])
    async def wikipedia_info(self, ctx):
        """

        :param ctx:
        :return:
        """

        # asks for the wikipedia topic
        await ctx.send('What would you like to learn about?')
        try:
            wiki_topic = await self.client.wait_for('message',
                                                    check=lambda message:
                                                    message.author == ctx.author)

            embed = discord.Embed(
                    description=get_wiki_info(wiki_topic.content),
                    colour=discord.Colour.purple()
            )
            embed.set_author(name=wiki_topic.content,
                             icon_url='https://cdn.discordapp.com/avatars/77577'
                                      '4976548405278/3a033aaeb4c112f7778fed109a'
                                      'f4c7a7.webp?size=128')
            await ctx.send(embed=embed)
        except:
            await ctx.send('Try being more specific with your topic!')


def setup(client):
    client.add_cog(WikiCog(client))

# self.client.run('Nzc1Nzc0OTc2NTQ4NDA1Mjc4.X6rOvw.IIMUROaQt26-ztNsZpPNM4gL2gA')


