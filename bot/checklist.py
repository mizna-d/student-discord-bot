
from discord.ext import commands

from bot import helper

checklist_file = r"C:\Users\Mixna\PycharmProjects\discordBotProject\Storage" \
                 r"\checklist.csv "


class CheckListCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.todo_list = helper.get_checklist(checklist_file)

    @commands.command(case_insensitive=True, aliases=['addtodo', 'todo'])
    async def add_todo(self, ctx, *, todo=None):

        def check(m):
            return m.content is not None

        if todo is None:
            await ctx.send("What would you like to add to your todo list?")
            todo_input = await self.client.wait_for('message', check=check)
            self.todo_list.append(todo_input.content)
            await ctx.send(f"Your todo, '{todo_input.content}' has been "
                           f"successfully added")

        else:
            self.todo_list.append(todo)
            await ctx.send("Your todo has been successfully added")

        helper.update_list(self.todo_list, checklist_file)

    @commands.command(case_insensitive=True, aliases=['removetodo', "rtodo"])
    async def remove_todo(self, ctx, *, todo=None):
        possible = []
        to_print = ''

        def check(m):
            return m.content is not None

        if todo is None:
            await ctx.send("What is the keyword for the todo you would like "
                           "to delete? \n or if you would like to see your "
                           "todo list please type 'VIEW TODO'")
            input_todo = await self.client.wait_for('message', check=check)

            if input_todo.content in ["VIEW TODO", "view todo", "View Todo",
                                      "View TODO", "view TODO", "VIEWTODO"]:
                for i in self.todo_list:
                    to_print += i + "\n"
                await ctx.send(to_print + "What is the keyword for the todo "
                                          "you would like to delete?")
                input_todo = await self.client.wait_for('message', check=check)
            if input_todo.content == ".exit":
                ctx.send("You have exited this command")
                return

            for i in self.todo_list:
                if input_todo.content in i:
                    possible.append(i)
                    print(possible)

        else:
            for i in self.todo_list:
                if todo in i:
                    possible.append(i)
                    print(possible)

        valid = True
        finished = False

        for i in possible:
            await ctx.send(f"Would you like to remove '{i}' from "
                           f"your todo list?")
            answer = await self.client.wait_for('message', check=check)
            while valid:
                if answer.content in ["y", "yes", "yeah", "yup", "Y", "YES"]:
                    self.todo_list.remove(i)
                    finished = True
                    valid = False
                    await ctx.send(f" The todo list element '{i}' has been "
                                   f"successfully removed.")
                elif answer.content in ["n", "no", "nope", "N", "NO"]:
                    valid = False
                elif answer.content == ".exit":
                    await ctx.send("You have exited this command")
                    break
                else:
                    await ctx.send("Sorry, I couldn't understand, please "
                                   "repeat.")

        if not finished:
            await ctx.send("There are no todo list elements that fit you "
                           "keyword. You can try again by calling the command "
                           "with a new keyword")
        helper.update_list(self.todo_list, checklist_file)

    @commands.command(case_insensitive=True, aliases=['viewtodo'])
    async def view_todo(self, ctx):
        to_print = ''
        for i in self.todo_list:
            to_print += i + "\n"
        await ctx.send("Your To-Do List: \n" + to_print)


def setup(client):
    client.add_cog(CheckListCog(client))
