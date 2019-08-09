import requests
import datetime
from dateutil import relativedelta
import os
from pytz import timezone
import math
from time import sleep
import random

def set_dayly_quest(exercises):
    exercises_list = []
    list = []
    for exercise in exercises:
        exercises_list.append(exercise)
    for i in range (3):
        rand = math.floor(random.random() * len(exercises_list))
        challenge = Quest(exercises_list[rand])
        del exercises_list[rand]
        list.append(challenge)
    return list

def update_textfile_with_dict(dictionary, path):
  os.remove(path)
  file = open(path, 'w')
  for item in dictionary:
    file.write('%s:%s\n' % (item, dictionary[item]))
  file.close()

def count_additional_points(exercise, value, exercises):
  return(int(math.floor((int(value)/int(exercises[exercise]))*100)))

def check_if_exercise_record(exercise, value, exercises):
  if int(value) > int(exercises[exercise]):
    return True
  else:
    return False

def check_if_todays_quest(exercise):
  return False

def create_week_from_string(string):
  words = string.split('/')
  date = datetime.datetime(int(words[2]), int(words[1]), int(words[0]))
  week = Week(date, int(words[6]))
  return week

def get_dict_from_textfile(path):
    file = open(path,'r')
    text = file.read()
    strings = text.split('\n')
    words = []
    words_in_string = []
    dictionary = {}
    for string in strings:
      if string == '':
        continue
      words_in_string = string.split(':')
      for word in words_in_string:
        words.append(word)
      words_in_string = []
    for number in range(0, len(words), 2):
        if words[number] != '':
            dictionary[words[number]] = words[number+1]
    file.close()
    print(dictionary)
    return dictionary

class Quest:

    def __init__(self, exercise):
        self.exercise = exercise
        self.done = False

class Week:

    def __init__(self, date, points):
      while date.weekday() != 0:
        date = date - relativedelta.relativedelta(days=1)
      self.first_day = date
      self.last_day = date + relativedelta.relativedelta(days=6)
      self.points = points

    def write_into_string(self):
      string = "%s/%s/%s/%s/%s/%s/%s" % (self.first_day.day, self.first_day.month, self.first_day.year, self.last_day.day, self.last_day.month, self.last_day.year, self.points)
      return string

    def check_if_date_in(self,date):
      if date.date()<=self.last_day.date() and date.date() >= self.first_day.date():
        return True
      else:
        return False


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=20):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

greet_bot = BotHandler('882404980:AAH37wn5mDwcZUHYzDPCypqwPf7sSQra4zI')
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
weeks = get_dict_from_textfile('./weeks.txt')
exercises = get_dict_from_textfile('./exercises.txt')

def main():
    new_offset = None

    Record_bonus_points = 5
    Quest_bonus_points = 100

    weekFlag = True

    dayly_quest = set_dayly_quest(exercises)
    daily_quest_set = True
    greet_bot.send_message(258274093, 'Сегодняшние задания:')
    for quest in dayly_quest:
        greet_bot.send_message(258274093, '%s' % (quest.exercise))

    start_time = datetime.datetime.now()
    start_time_local = start_time.astimezone(timezone('Asia/Yekaterinburg'))
    last_week_in_data = create_week_from_string(weeks[str(len(weeks)-1)])
    if last_week_in_data.check_if_date_in(start_time_local):
      current_week = last_week_in_data
      print('the bot will continue with last week in data')
    else:
      current_week = Week(start_time_local, 0)
      weeks[len(weeks)] = current_week.write_into_string()
      update_textfile_with_dict(weeks, './weeks.txt')
      print('new week has been created')

    while True:
        print('i have entered the loop')
        greet_bot.get_updates(new_offset)

        time = datetime.datetime.now()
        time_local = time.astimezone(timezone('Asia/Yekaterinburg'))
        time_local = time_local + relativedelta.relativedelta(days=3)

        last_update = greet_bot.get_last_update()

        if time_local.hour == 0 and time_local.minute == 0 :
            set_dayly_quest == False
        if time_local.hour == 8 and time_local.minute == 0 :
          greet_bot.send_message(258274093, 'Хозяин, пора вставать!')
          if set_dayly_quest == False:
              dayly_quest = set_dayly_quest(exercises)
              greet_bot.send_message(258274093, 'Сегодняшние задания:')
              for quest in dayly_quest:
                  greet_bot.send_message(258274093, '%s' % (quest.exercise))
              daily_quest_set = True
        if time_local.hour == 12 and  time_local.minute == 0 :
          greet_bot.send_message(258274093, 'Война войной, а обед по расписанию!')
        if time_local.hour == 15 and  time_local.minute == 0 :
          greet_bot.send_message(258274093, 'Перекусите. Хотя бы с пол кулака.')
        if time_local.hour == 19 and  time_local.minute == 0 :
          greet_bot.send_message(258274093, 'После ужина самое время заняться аэробными упражнениями! Надеюсь, вы не объелись?')
        if time_local.hour == 23 and  time_local.minute == 0 :
          greet_bot.send_message(258274093, 'Спокойной ночи, Хозяин! Надеюсь вы помните, что заснув после полуночи, крайне тяжело выспаться?')
        if time_local.hour == 20 and time_local.minute == 44 and time_local.weekday() == 0:
          greet_bot.send_message(258274093, 'Неделя подошла к концу!')
          if weekFlag == True:
              current_week = Week(time_local, 0)
              weeks[len(weeks)] = current_week.write_into_string()
              update_textfile_with_dict(weeks, './weeks.txt')
              weekFlag = False
        if time_local.hour == 0 and time_local.minute == 1 and time_local.weekday() == 0:
          weekFlag = True
        if last_update is None: continue

        last_update_id = last_update['update_id']
        last_chat_id = last_update['message']['chat']['id']
        if 'text' in last_update['message']:
            last_chat_text = last_update['message']['text']
        else:
            greet_bot.send_message(last_chat_id, 'Ошибка! Я умею работать только с текстовыми сообщениями.')
            sleep(20)
            continue
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower()=='упражнения' :
          for exercise in exercises:
            greet_bot.send_message(last_chat_id, ' %s: %s' % (exercise, exercises[exercise]))

        elif last_chat_text.lower()=='квест' :
            if len(dayly_quest) > 0:
                greet_bot.send_message(last_chat_id, 'Сегодняшние задания:')
                for quest in dayly_quest:
                    greet_bot.send_message(last_chat_id, '%s' % (quest.exercise))
            else: greet_bot.send_message(last_chat_id, 'Вы выполнили все задания на сегодня! Так держать!')

        elif last_chat_text.lower()=='баллы' :
            greet_bot.send_message(last_chat_id, 'Баллы за текущую неделю: %s' % (current_week.points))

        elif last_chat_text.lower()=='время' :
          greet_bot.send_message(last_chat_id, 'Текущее время: %s:%s' % (time_local.hour, time_local.minute))

        elif last_chat_text.lower()=='дата' :
          greet_bot.send_message(last_chat_id, 'Сегодняшняя дата: %s.%s.%s' % (time_local.day, time_local.month, time_local.year))

        elif last_chat_text.lower() in greetings :
            greet_bot.send_message(last_chat_id, 'Привет, {}'.format(last_chat_name))

        else:
          words = last_chat_text.lower().split(' ')
          if len(words) > 1:
            if words[0] in exercises: #залить упражнение
                try:
                    int(words[1])
                except ValueError:
                    greet_bot.send_message(last_chat_id, 'Ошибка!')
                    sleep(20)
                    continue
                additional_points = 0
                if check_if_exercise_record(words[0], words[1], exercises):
                    greet_bot.send_message(last_chat_id, 'Вы поставили новый рекорд!')
                    additional_points += Record_bonus_points
                    exercises[words[0]] = words[1]
                    print(exercises)
                    update_textfile_with_dict(exercises, './exercises.txt')

                if len(dayly_quest)>0:
                    dayly_quest_copy = dayly_quest
                    to_kill = -1
                    print(range(len(dayly_quest_copy)))
                    for i in range(len(dayly_quest_copy)):
                        print(i)
                        print(words[0])
                        if dayly_quest_copy[i].exercise == words[0]:
                            to_kill = i
                    del dayly_quest[to_kill]
                    if len(dayly_quest) == 0:
                        greet_bot.send_message(last_chat_id, 'Вы выполнили квест и получили 100 бонусных баллов!')
                        additional_points += Quest_bonus_points

                additional_points += count_additional_points(words[0], words[1], exercises)
                greet_bot.send_message(last_chat_id, 'Вы записали упражнение: %s, получив %s баллов!' % (words[0], additional_points))
                current_week.points += additional_points
                weeks[str(len(weeks)-1)] = current_week.write_into_string()
                update_textfile_with_dict(weeks, './weeks.txt')

            elif words[0] == 'добавить':
                if len(words) > 2:
                    try:
                        int(words[2])
                    except ValueError:
                        greet_bot.send_message(last_chat_id, 'Ошибка!')
                        sleep(20)
                        continue
                    exercises[words[1]] = words[2]
                    greet_bot.send_message(last_chat_id, 'Добавлено упражнение: %s с рекордом %s' % (words[1], words[2]))
                    update_textfile_with_dict(exercises, './exercises.txt')

            elif words[0] == 'вычесть':
                if len(words) > 1:
                    try:
                        int(words[1])
                    except ValueError:
                      greet_bot.send_message(last_chat_id, 'Ошибка!')
                      sleep(20)
                      continue
                    current_week.points -= int(words[1])
                    weeks[str(len(weeks)-1)] = current_week.write_into_string()
                    update_textfile_with_dict(weeks, './weeks.txt')

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(
)
