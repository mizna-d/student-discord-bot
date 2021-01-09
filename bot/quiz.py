import csv
import re
import random
import sqlite3
from discord.ext import commands

from bot import helper

f = r'C:\Users\Mixna\PycharmProjects\student-discord-bot\Storage' \
    r'\question_bank.csv '

correct_feedback = ["That's right!", "Correct!", "That's correct!",
                    "You got it!", "Looks like you know your stuff!",
                    "Yup! That's the answer!", "Amazing as always!"]

incorrect_feedback = ["Oh no. Wrong answer.", "Ahh that's not correct.",
                      "Incorrect.", "Sorry, that's wrong.",
                      "Whoops! Wrong Answer.", "You might need more practice."]

level_dict = {0: 0, 1: 5, 2: 10, 3: 25, 4: 45, 5: 70, 6: 100, 7: 150, 8: 200,
              9: 350, 10: 500, 11: 1000000000000000}


class QuizCog(commands.Cog):
    """"
    This class is responsible for commands related to the flashcard and quiz
    aspects of this bot. This includes, adding and removing questions from the
    question bank. Users are able to practice questions from the question
    bank having unlimited tries to get the answer right. Users are also able to
    test themselves where the bot provides feedback in terms of a score.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(case_insensitive=True, aliases=['addquestion', 'aq'])
    async def add_question(self, ctx):
        """
        Allows the user to add a paired question and answer to the question bank
        :param ctx: the context of the command call
        :returns: messages in response to the user's decisions
        """

        def check(m):
            return m.content is not None and m.author == ctx.author

        # asks for question
        await ctx.send('Please input the question you would like to add to the '
                       'question bank')
        question = await self.client.wait_for('message', check=check)

        # asks for answer to aforementioned question
        await ctx.send('Please input the correct answer for the previously'
                       ' inputted question')
        answer = await self.client.wait_for('message', check=check)

        # adds info to csv file
        with open(f, mode='a', newline='') as question_bank:
            question_bank = csv.writer(question_bank, delimiter=',',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)
            question_bank.writerow([question.content, answer.content,
                                    question.channel])

        # success message
        await ctx.send(f"The question, '{question.content}' and its answer, "
                       f"'{answer.content}' was successfully added to the "
                       f"question "
                       f"bank")

    @commands.command(case_insensitive=True, aliases=['removequestion', 'rq'])
    async def remove_question(self, ctx):
        """ Allows the user to remove a previously added question from the
        question bank
        :param ctx: the context of the command call
        :returns: messages in response to to the user's decisions
        """
        # shows all the questions in the question bank with numbers

        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            recorder = []
            for row in csv_reader:
                await ctx.send(
                    f'{line_count + 1} \nQuestion:\t{row[0]} \nAnswer:  '
                    f'\t{row[1]}')
                recorder.append(row[0])
                line_count += 1

            if len(recorder) != 0:
                await ctx.send("Please enter the selection of the question you"
                               " would like to remove")

                def check(m):
                    return m.content is not None

                to_delete = await self.client.wait_for('message', check=check)

                if re.search("[0-9][0-9]*", to_delete.content):

                    # removes accordingly
                    line_count = 0
                    updated_bank = []
                    question = ""
                    answer = ""
                    csv_file.seek(0, 0)

                    for row in csv_reader:
                        if line_count != int(to_delete.content) - 1:
                            updated_bank.append(row)
                        else:
                            question = row[0]
                            answer = row[1]
                        line_count += 1

                    if helper.update_file(updated_bank):
                        await ctx.send(f"The question, '{question}' and its "
                                       f"answer, '{answer}' was successfully "
                                       f"removed from the question bank")
                    else:
                        await ctx.send("Your request could not be completed")
                else:
                    await ctx.send("Not a valid input")
            else:
                await ctx.send(
                    "There are no questions found in the question bank")

    @commands.command(case_insensitive=True,
                      aliases=["viewall", "viewallquestions",
                               "viewquestionbank", "vqb"])
    async def view_question_bank(self, ctx):
        """
        Allows the user to view all the questions and their answers found in the
        question bank
        :param ctx: the context of the command call
        :returns: messages in response to to the user's decisions
        """
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            recorder = []
            for row in csv_reader:
                await ctx.send(f'\nQuestion:\t{row[0]} \nAnswer:  \t{row[1]}\n')
                recorder.append(row[0])
                line_count += 1

            if len(recorder) == 0:
                await ctx.send(
                    "There are no questions found in the question bank")

    @commands.command(case_insensitive=True,
                      aliases=["askquestion", "askme", "ask",
                               'practice'])
    async def ask_question(self, ctx, num=1, timeout=30):
        """
        Allows the user to prompt the bot to help them practice questions from
        the question bank, giving them unlimited tries to answer correctly. The
        user can specify the number of questions they want to practice in
        one go as well as the time limit they have to answer each question. If
        they do not, the bot will assume the default values, 1 question per call
        and a 30 second time limit for each question.

        :param ctx: the context of the command call
        :param num: Optional parameter representing the number of questions to
        be asked from this call, default number is 1 question per call.
        :param timeout: Optional parameter representing the timeout time of each
        question. This creates a time limit for each question to be answered
        within, the default time is 30 seconds.
        :return: messages in response to to the user's decisions
        """
        question_bank = helper.get_question_bank()

        counter = 1
        marker = False
        while counter <= num:

            def check(m):
                return m.content is not None

            if len(question_bank) == 0:
                if marker:
                    await ctx.send("There are no more questions left to ask")
                else:
                    await ctx.send("There are no questions to ask")
                break

            else:
                marker = True
                chosen_row = random.choice(question_bank)
                question_bank.remove(chosen_row)
                await ctx.send(f'Question: {chosen_row[0]}')
                counter += 1
                answer = await self.client.wait_for('message', check=check,
                                                    timeout=timeout * 1000)
                if answer.content == chosen_row[1]:

                    await ctx.send(random.choice(correct_feedback))

                else:
                    incorrect = True
                    while incorrect:

                        await ctx.send(random.choice(incorrect_feedback) +
                                       " Try again.\nIf you would like "
                                       "to exit, type '.exit'")
                        answer = await self.client.wait_for(
                            'message', check=check, timeout=timeout * 1000)
                        if answer.content == chosen_row[1]:
                            incorrect = False

                            await ctx.send(random.choice(correct_feedback))
                        elif answer.content == '.exit':
                            incorrect = False
                            await ctx.send("You have exited the "
                                           "question bank")

    @commands.command(case_insensitive=True, aliases=["practiceall", 'askall',
                                                      "askallquestions"])
    async def ask_all_questions(self, ctx, timeout=30):
        """
        Allows the user to prompt the bot to help them practice through all the
        questions found in the question bank, with unlimited tries to answer
        each question correctly. The user can specify the time limit to answer
        each question (in seconds), otherwise will use the default limit of 30
        seconds.

        :param ctx: the context of the command call
        :param timeout: Optional parameter representing the timeout time of each
        question. This creates a time limit for each question to be answered
        within, the default time is 30 seconds
        :returns: messages in response to to the user's decisions
        """
        question_bank = helper.get_question_bank()
        counter = 1
        marker = False

        while True:
            def check(m):
                return m.content is not None

            if len(question_bank) == 0:
                if marker:
                    await ctx.send("There are no more questions left to ask")
                else:
                    await ctx.send("There are no questions to ask")
                break

            else:
                marker = True
                chosen_row = random.choice(question_bank)
                question_bank.remove(chosen_row)
                await ctx.send(f'Question: {chosen_row[0]}')
                counter += 1
                answer = await self.client.wait_for('message', check=check,
                                                    timeout=timeout * 1000)
                if answer.content == chosen_row[1]:

                    await ctx.send(random.choice(correct_feedback))

                else:
                    incorrect = True
                    while incorrect:

                        await ctx.send(random.choice(incorrect_feedback) +
                                       " Try again."
                                       "\nIf you would like "
                                       "to exit, type '.exit'")
                        answer = await \
                            self.client.wait_for('message', check=check,
                                                 timeout=timeout * 1000)
                        if answer.content == chosen_row[1]:
                            incorrect = False

                            await ctx.send(random.choice(correct_feedback))
                        elif answer.content == '.exit':
                            incorrect = False
                            await ctx.send("You have exited the "
                                           "question bank")

    @commands.command(case_insensitive=True,
                      aliases=["testquestions", "testme"])
    async def test_questions(self, ctx, num=5, timeout=30):
        """
        Allows the user to prompt the bot to help them test themselves using
        questions from the question bank, giving them only one try to answer
        each correctly, and keeping score. After the selected number of
        questions are answered, the user wil receive a score based on their
        performance.

        The user can specify the number of questions they want to
        practice in one go and the time limit they have to answer each question.
        If they decide not to, the bot will assume the default values, 1
        question per call and a 30 second time limit for each question.


        :param ctx: the context of the command call
        :param num: Optional parameter representing the number of questions to
        be tested from this call, default number is 5 questions per call.
        :param timeout: Optional parameter representing the timeout time of each
        question. This creates a time limit for each question to be answered
        within, the default time is 30 seconds
        :returns: messages in response to to the user's decisions and score
        based on how many questions asked were correctly answered
        """
        question_bank = helper.get_question_bank()

        correct = 0
        total = 0
        counter = 1
        marker = False
        while counter <= num:

            def check(m):
                return m.content is not None

            if len(question_bank) == 0:
                if marker:
                    await ctx.send(f"You completed the allotted questions! "
                                   f"\nYour score was {correct} out of {total},"
                                   f" {(correct / total) * 100}%.")
                else:
                    await ctx.send("There are no questions to ask")
                break

            else:
                marker = True
                chosen_row = random.choice(question_bank)
                question_bank.remove(chosen_row)
                await ctx.send(f'Question: {chosen_row[0]}')
                counter += 1

                answer = await self.client.wait_for('message', check=check,
                                                    timeout=timeout * 1000)
                total += 1
                if answer.content == chosen_row[1]:
                    correct += 1

                    await ctx.send(random.choice(correct_feedback))

                    db = sqlite3.connect('user_levels.sqlite')
                    cursor = db.cursor()
                    helper.add_points(db, cursor, answer)
                    cursor.execute(f"SELECT user_id, XP, level FROM "
                                   f"user_levels WHERE "
                                   f"user_id = {answer.author.id}")
                    user_stats = cursor.fetchone()
                    current_xp = int(user_stats[1])
                    current_level = int(user_stats[2])

                    to_exceed = level_dict[current_level + 1]

                    if current_xp >= to_exceed:
                        await ctx.send(f"Congrats! {answer.author.mention} "
                                       f"has leveled up "
                                       f"to level {current_level + 1}! "
                                       f"This means {answer.author.name} "
                                       f"has answered {current_xp} questions "
                                       f"correctly. Keep up the great work!")
                        cursor.execute(f"UPDATE user_levels SET "
                                       f"level = {current_level + 1} WHERE "
                                       f"user_id = {str(answer.author.id)}")
                        db.commit()
                        cursor.close()
                        db.close()

                elif answer.content == '.exit':
                    await ctx.send(f"You have exited the question bank. "
                                   f"\nYour score was {correct} out of "
                                   f"{total}, {(correct / total) * 100}%.")

                else:
                    await ctx.send(random.choice(incorrect_feedback))

    @commands.command(case_insensitive=True,
                      aliases=["testall", "testallquestions",
                               "testmeall"])
    async def test_all_questions(self, ctx, timeout=30):
        """
        Allows the user to prompt the bot to help them test themselves using all
        the questions from the question bank, giving them only one try to answer
        each correctly, and keeping score. After all the questions are answered,
        the user wil receive a score based on their performance.

        The user can specify the number of questions they want to
        practice in one go and the time limit they have to answer each question.
        If they decide not to, the bot will assume the default values, 1
        question per call and a 30 second time limit for each question.
        :param ctx: the context of the command call
        :param timeout: Optional parameter representing the timeout time of each
        question. This creates a time limit for each question to be answered
        within, the default time is 30 seconds
        :returns: messages in response to to the user's decisions and score
        based on how many questions asked were correctly answered
        """
        question_bank = helper.get_question_bank()
        marker = False
        correct = 0
        total = 0

        while True:
            def check(m):
                return m.content is not None

            if len(question_bank) == 0:
                if marker:
                    await ctx.send(f"You completed all the questions!."
                                   f"\n Your score was "
                                   f"{correct} out of {total}, "
                                   f"{(correct / total) * 100}%.")
                else:
                    await ctx.send("There are no questions to ask")
                break

            else:
                marker = True
                chosen_row = random.choice(question_bank)
                question_bank.remove(chosen_row)
                await ctx.send(f'Question: {chosen_row[0]}')
                answer = await self.client.wait_for('message', check=check,
                                                    timeout=timeout * 1000)
                total += 1

                if answer.content == chosen_row[1]:
                    correct += 1
                    await ctx.send(random.choice(correct_feedback))

                    db = sqlite3.connect('user_levels.sqlite')
                    cursor = db.cursor()
                    helper.add_points(db, cursor, answer)
                    cursor.execute(f"SELECT user_id, XP, level FROM "
                                   f"user_levels WHERE "
                                   f"user_id = {answer.guild.id}")
                    user_stats = cursor.fetchone()
                    current_xp = int(user_stats[1])
                    current_level = int(user_stats[2])

                    to_exceed = level_dict[current_level + 1]

                    if current_xp >= to_exceed:
                        await ctx.send(f"Congrats! {answer.author.mention}"
                                       f" has leveled up "
                                       f"to level {current_level + 1}! "
                                       f"This means {answer.author.nickname} "
                                       f"has answered {current_xp} questions "
                                       f"correctly. Keep up the great work!")
                        cursor.execute(f"UPDATE user_levels SET "
                                       f"level = {current_level + 1} WHERE "
                                       f"user_id = {str(answer.author.id)}")
                        db.commit()
                        cursor.close()
                        db.close()

                elif answer.content == '.exit':
                    await ctx.send(f"You have exited the question bank. "
                                   f"\nYour score was {correct} out of "
                                   f"{total}, {(correct / total) * 100}%.")
                    break

                else:
                    await ctx.send(random.choice(incorrect_feedback))


def setup(client):
    client.add_cog(QuizCog(client))
