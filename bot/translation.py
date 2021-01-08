import discord
from discord.ext import commands
# from googletrans import Translator
# translator = Translator()
from google_trans_new import google_translator

translator = google_translator()


# def get_french_translation(word):
#     french_translation = translator.translate(word, src='en', dest='fr')
#     print(french_translation.text)


def get_french_translation(word):
    french_translation = translator.translate(word, lang_src='en', lang_dest='fr')
    print(french_translation.text)


# def get_spanish_translation(word):
#     spanish_translation = translator.translate(word, src='en', dest='es')
#     print(spanish_translation.text)

def get_spanish_translation(word):
    spanish_translation = translator.translate(word, lang_src='en', lang_dest='es')
    print(spanish_translation.text)


get_french_translation("what are you doing")


class TranslationCog(commands.Cog):
    """

    """
    def __init__(self, client):
        self.client = client

    @commands.command(caseinsensitive=True, aliases=['translate', 'tr'])
    async def word_translation(self, ctx):
        """

        :param ctx:
        :return:
        """
        await ctx.send('What word would you like the translation of?')

        get_word_to_translate = await self.client.wait_for('message',
                                                           check=lambda message:
                                                           message.author == ctx.author)

        await ctx.send('What language would you like to translate it to?')

        get_language = await self.client.wait_for('message',
                                                  check=lambda message:
                                                  message.author == ctx.author)

        if get_language.content == 'French' or 'french' or 'fr':
            embed = discord.Embed(
                description='Translation:' + get_french_translation(get_word_to_translate.content),
                colour=discord.Colour.blue()
            )
            embed.set_author(name=get_word_to_translate.content,
                             icon_url='https://cdn.discordapp.com/avatars/77577'
                                      '4976548405278/3a033aaeb4c112f7778fed109a'
                                      'f4c7a7.webp?size=128')
            await ctx.send(embed=embed)

        if get_language.content == 'Spanish' or 'spanish' or 'es':
            embed = discord.Embed(
                description='Translation:' + get_spanish_translation(get_word_to_translate.content),
                colour=discord.Colour.blue()
            )
            embed.set_author(name=get_word_to_translate.content,
                             icon_url='https://cdn.discordapp.com/avatars/77577'
                                      '4976548405278/3a033aaeb4c112f7778fed109a'
                                      'f4c7a7.webp?size=128')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TranslationCog(client))
