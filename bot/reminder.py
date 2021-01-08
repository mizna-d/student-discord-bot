import asyncio

from discord.ext import commands
import re

from bot import helper

file = r'C:\Users\Mixna\PycharmProjects\discordBotProject\Storage\reminders.csv'


class ReminderCog(commands.Cog):
    """

    """
    def __init__(self, client):
        self.client = client

    @commands.command(case_insensitive=True, aliases=["remind", "r"])
    async def reminder(self, ctx, *, reminder=None):
        """

        :param ctx:
        :param reminder:
        :return:
        """

        def check(m):
            return m.content is not None

        marker = True

        if reminder is None:
            while marker:
                await ctx.send("What would like to be reminded of?")
                reminding = await self.client.wait_for('message', check=check)
                if not re.search("[.]*[a-zA-z]+[.]*", reminding.content):
                    await ctx.send("You have not entered a valid reminder "
                                   "message")
                elif reminding.content == '.exit':
                    break
                else:
                    marker = False
                    marker_two = True
                    while marker_two:
                        await ctx.send("What time would you like to be "
                                       "reminded?")
                        timing = await self.client.wait_for('message',
                                                            check=check)
                        if not re.search(r"^(?=.*[hmd]$)\d*(?:d\s*)?\d*("
                                         r"?:h\s*)?\d*(?:m\s*)?$",
                                         timing.content):
                            await ctx.send("incorrect formatting")
                        elif timing.content == '.exit':
                            break
                        else:
                            marker_two = False

                            reminder_time = helper.reminder_time(timing.content)
                            counter = f"{reminder_time[1]} day(s), " \
                                      f"{reminder_time[2]} hour(s), " \
                                      f"{reminder_time[3]} minutes(s) "

                            if reminding == '':
                                await ctx.send(f"Your reminder, "
                                               f"'{reminder}' at "
                                               f"{reminder_time[0]} is set! "
                                               f"\n I'll make sure to remind "
                                               f"you in {counter}.")
                                await asyncio.sleep(reminder_time[-1])
                                await ctx.send(f"Hi "
                                               f"@{ctx.message.author.mention},"
                                               f" you asked me to remind you, '"
                                               f"{reminder}' {counter} ago.")
                            elif reminding != '':
                                await ctx.send(f"Your reminder, '"
                                               f"{reminding.content}' at "
                                               f"{reminder_time[0]} is set! "
                                               f"\n I'll make sure to remind "
                                               f"you in {counter}.")
                                await asyncio.sleep(reminder_time[-1])
                                await ctx.send(f"Hi "
                                               f"@{ctx.message.author.mention},"
                                               f" you asked me to remind you, '"
                                               f"{reminding.content}' {counter}"
                                               f" ago.")
                            else:
                                await ctx.send("Something went wrong with "
                                               "your request")

        else:
            if not re.search("[.]*[a-zA-z]+[.]*", reminder):
                await ctx.send("You have not entered a valid reminder message")
                while marker:
                    await ctx.send("What would like to be reminded of?")
                    reminding = await self.client.wait_for('message',
                                                           check=check)
                    if not re.search("[.]*[a-zA-z]+[.]*", reminding.content):
                        await ctx.send("You have not entered a valid reminder "
                                       "message")
                    elif reminding.content == '.exit':
                        break
                    else:
                        marker = False
                        marker_two = True
                        while marker_two:
                            await ctx.send("What time would you like to "
                                           "be reminded?")
                            timing = await self.client.wait_for('message',
                                                                check=check)
                            if not re.search(r"^(?=.*[hmd]$)\d+(?:d\s*)?\d*("
                                             r"?:h\s*)?\d*(?:m\s*)?$",
                                             timing.content):
                                await ctx.send("incorrect formatting")
                            elif timing.content == '.exit':
                                break
                            else:
                                marker_two = False

                                reminder_time = helper.reminder_time \
                                    (timing.content)
                                counter = f"{reminder_time[1]} day(s), " \
                                          f"{reminder_time[2]} hour(s), " \
                                          f"{reminder_time[3]} minutes(s)"

                                if reminding == '':
                                    await ctx.send(f"Your reminder, '"
                                                   f"{reminder}' at "
                                                   f"{reminder_time[0]} is set!"
                                                   f" \n I'll make sure to "
                                                   f"remind you in {counter}.")
                                    await asyncio.sleep(reminder_time[-1])
                                    await ctx. \
                                        send(f"Hi @{ctx.message.author.mention}"
                                             f", you asked me to remind you, '"
                                             f"{reminder}' {counter} ago.")
                                elif reminding != '':
                                    await ctx.send(f"Your reminder, '"
                                                   f"{reminding.content}' "
                                                   f"at {reminder_time[0]} "
                                                   f"is set! \n I'll make sure "
                                                   f"to remind you in {counter}"
                                                   f".")
                                    await asyncio.sleep(reminder_time[-1])
                                    await ctx.send(
                                        f"Hi {ctx.message.author.mention}, "
                                        f"you asked me to remind you, '"
                                        f"{reminding.content}' {counter} ago.")
                                else:
                                    await ctx.send("Something went wrong "
                                                   "with your request")


def setup(client):
    client.add_cog(ReminderCog(client))
