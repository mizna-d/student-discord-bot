import discord
from discord.ext import commands
from PyDictionary import PyDictionary

dictionary = PyDictionary()


def get_definition(word):
    """
    Gets possible definitions of the word requested by the user and stores in a list
    :param word: the word which was sent by the user
    :returns: a list of possible definitions
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
    """
    Displays all possible definitions for the word which was requested
    :param definition_list: a list of possible definitions
    :return: a formatted string of the definitions
    """
    final_definitions = ""
    for i in definition_list:
        final_definitions += i + "\n" + "\n"
    return final_definitions


class DictionaryCog(commands.Cog):
    """
    This class is responsible for commands related to the finding the definitions
    of words aspect of the bot. This includes, recieving words and outputting the
    definition of the word. Users are able to acquire definitions for unknown words
    while studying.
    """
    def __init__(self, client):
        self.client = client

    @commands.command(caseinsensitive=True, aliases=['define', 'definition'])
    async def word_definition(self, ctx):
        """
        Allows the user to send a word to be defined and recieve a definition
        :param ctx: the context of the command call
        :returns: messages in response to to the user's decisions
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
