import csv
import datetime
from discord.ext import commands
import sqlite3

question_bank_file = r'C:\Users\Mixna\PycharmProjects\student-discord-bot' \
                     r'\Storage\question_bank.csv '


def get_question_bank():
    """

    :return:
    """
    with open(question_bank_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        question_bank = []
        for row in csv_reader:
            question_bank.append(row)
    return question_bank


def get_checklist(checklist_file):
    with open(checklist_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        checklist = []
        for row in csv_reader:
            for i in row:
                checklist.append(i)
    return checklist


def update_list(updated_list, file_name):
    """

    :param file_name:
    :param updated_list:
    :return:
    """
    if updated_list is not None and len(updated_list) != 0:
        with open(file_name, "w", newline='') as file_to_update:
            file_to_update.truncate()
            csv.writer(file_to_update).writerow(updated_list)
            return True
    else:
        return False


def update_file(updated_content):
    """

    :param updated_content:
    :return:
    """
    if updated_content is not None:
        with open(question_bank_file, "w", newline='') as file_to_update:
            file_to_update.truncate()
            writer = csv.writer(file_to_update)
            for i in updated_content:
                writer.writerow(i)
            return True
    else:
        return False


def reminder_time(timing_content):
    """

    :param timing_content:
    :return:
    """
    rn = datetime.datetime.now()

    # checking days
    days = ''
    if 'd' in timing_content:
        num = 1
        while timing_content[timing_content.find('d') - num].isdigit():
            days += timing_content[timing_content.find('d') - num]
            num += 1

        days = days[::-1]

    # checking hours
    hours = ''
    if 'h' in timing_content:
        num = 1
        while timing_content[timing_content.find('h') - num].isdigit():
            hours += timing_content[timing_content.find('h') - num]
            num += 1

        hours = hours[::-1]

    # checking minutes
    minutes = ''
    if 'm' in timing_content:
        num = 1
        while timing_content[timing_content.find('m') - num].isdigit():
            minutes += timing_content[timing_content.find('m') - num]
            num += 1

        minutes = minutes[::-1]

    if days != '':
        if hours != '':
            if minutes != '':
                final_time = rn + datetime.timedelta(days=int(days),
                                                     hours=int(hours),
                                                     minutes=int(minutes))
                days = int(days)
                hours = int(hours)
                minutes = int(minutes)
            else:
                final_time = rn + datetime.timedelta(days=int(days),
                                                     hours=int(hours))
                days = int(days)
                hours = int(hours)
                minutes = 0
        else:
            if minutes != '':
                final_time = rn + datetime.timedelta(days=int(days),
                                                     minutes=int(minutes))
                days = int(days)
                hours = 0
                minutes = int(minutes)
            else:
                final_time = rn + datetime.timedelta(days=int(days))
                days = int(days)
                hours = 0
                minutes = 0
    elif hours != '':
        if minutes != '':
            final_time = rn + datetime.timedelta(hours=int(hours),
                                                 minutes=int(minutes))
            days = 0
            hours = int(hours)
            minutes = int(minutes)
        else:
            final_time = rn + datetime.timedelta(hours=int(hours))
            days = 0
            hours = int(hours)
            minutes = 0
    elif minutes != '':
        final_time = rn + datetime.timedelta(minutes=int(minutes))
        days = 0
        hours = 0
        minutes = int(minutes)
    else:
        final_time = 0

    total = days*24*60*60 + hours*60*60 + minutes*60
    return final_time.ctime(), days, hours, minutes, total


def add_points(db, cursor, msg):

    cursor.execute(f"SELECT user_id FROM user_levels WHERE "
                   f"user_id = '{msg.author.id}'")
    exists = cursor.fetchone()
    if exists is None:
        cursor.execute(f"INSERT INTO user_levels(user_id, XP, level) "
                       f"VALUES({msg.author.id}, 1, 0)")
        db.commit()
    else:
        cursor.execute(f"SELECT user_id, XP, level FROM user_levels WHERE "
                       f"user_id = {msg.author.id}")
        result = cursor.fetchone()
        xp = int(result[1])
        cursor.execute(f"UPDATE user_levels SET XP = {xp + 1} WHERE "
                       f"user_id = {str(msg.author.id)}")
        db.commit()
