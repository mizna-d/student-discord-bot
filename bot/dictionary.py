import discord
from discord.ext import commands
from PyDictionary import PyDictionary

dictionary = PyDictionary()


def get_definition(word):
    """

    :param word:
    :return:
    """
    word_meaning = PyDictionary(word)
    word_definitions = word_meaning.meaning(word)
    definition_list = []
    if 'Noun' in word_definitions:
        word_is_noun = "Noun:" + " " + word_definitions['Noun'][0]
        definition_list.append(word_is_noun)
    if 'Adjective' in word_definitions:
        word_is_adjective = "Adjective:" + " " + word_definitions['Adjective'][0]
        definition_list.append(word_is_adjective)
    if 'Verb' in word_definitions:
        word_is_verb = "Verb:" + " " + word_definitions['Verb'][0]
        definition_list.append(word_is_verb)
    return definition_list

def display_definition(definition_list):
    final_definitions = ""
    for i in definition_list:
        final_definitions += i + "\n" + "\n"
    return final_definitions


class DictionaryCog(commands.Cog):
    """

    """
    def __init__(self, client):
        self.client = client

    @commands.command(caseinsensitive=True, aliases=['define', 'definition'])
    async def word_definition(self, ctx):
        """

        :param ctx:
        :return:
        """
        await ctx.send('What word would you like the definition for?')

        get_word = await self.client.wait_for('message',
                                              check=lambda message:
                                              message.author == ctx.author)

        embed = discord.Embed(
            description=display_definition(get_definition(get_word.content)),
            colour=discord.Colour.blue()
        )
        embed.set_author(name=get_word.content,
                         icon_url='https://cdn.discordapp.com/avatars/77577'
                                  '4976548405278/3a033aaeb4c112f7778fed109a'
                                  'f4c7a7.webp?size=128')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(DictionaryCog(client))
