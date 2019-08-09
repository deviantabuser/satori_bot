import requests
import datetime
from dateutil import relativedelta
import os
from pytz import timezone
import math

def update_textfile_with_dict(dictionary, path):
  file = open(path, 'w')
  for item in dictionary:
    file.write('%s:%s' % (item, dictionary[item]))
  file.close() #этот кусок ещё не чекал

def count_additional_points(exercise, value, exercises):
  return(int(math.floor((int(value)/int(exercises[exercise]))*100)))

def check_if_exercise_record(exercise, value, exercises):
  if value > exercises[exercise]:
    return True
  else:
    return False #этот кусок ещё не чекал

def check_if_todays_quest(exercise):
  return False

def create_week_from_string(string):
  words = string.split('/')
  date = datetime.datetime(int(words[2]), int(words[1]), int(words[0]))
  week = Week(date, int(words[6]))
  return week #этот кусок ещё не чекал

def get_dict_from_textfile(path):
    file = open(path,'r')
    text = file.read()
    strings = text.split('\n')
    words = []
    dictionary = {}
    for word in strings:
      words.append(word.split(':'))
    for word in words:
      dictionary[word[0]] = word[1]
    file.close()
    return dictionary

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

    Record_bonus_points = 100
    Quest_bonus_points = 100

    start_time = datetime.datetime.now()
    start_time_local = start_time.astimezone(timezone('Asia/Yekaterinburg'))
    last_week_in_data = create_week_from_string(weeks[str(len(weeks)-1)])
    if last_week_in_data.check_if_date_in(start_time_local):
      current_week = last_week_in_data
    else:
      current_week = Week(start_time_local, 0)
      weeks[len(weeks)] = current_week.write_into_string()
      print(weeks)
      update_textfile_with_dict(weeks, './weeks.txt') #этот кусок ещё не чекал


    while True:
        print('i have entered the loop')
        greet_bot.get_updates(new_offset)

        time = datetime.datetime.now()
        time_local = time.astimezone(timezone('Asia/Yekaterinburg'))

        last_update = greet_bot.get_last_update()
        if time_local.hour == 13 and  time_local.minute == 0 :
          greet_bot.send_message(258274093, 'Напоминание!')
        if time_local.hour == 0 and time_local.minute == 0 and time_local.weekday() == 0:
          greet_bot.send_message(258274093, 'Неделя подошла к концу!')
        if last_update is None: continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower()=='упражнения' :
          for exercise in exercises:
            greet_bot.send_message(last_chat_id, ' %s: %s' % (exercise, exercises[exercise]))

        elif last_chat_text.lower()=='время' :
          greet_bot.send_message(last_chat_id, 'Текущее время: %s:%s' % (time_local.hour, time_local.minute))

        elif last_chat_text.lower()=='дата' :
          greet_bot.send_message(last_chat_id, 'Сегодняшняя дата: %s.%s.%s' % (time_local.day, time_local.month, time_local.year))

        elif last_chat_text.lower() in greetings :
            greet_bot.send_message(last_chat_id, 'Привет, {}'.format(last_chat_name))

        else:
          words = last_chat_text.lower().split(' ')
          if len(words) > 1:
            if words[0] in exercises:
              try:
                int(words[1])
              except TypeError:
                continue
              additional_points = 0
              if check_if_exercise_record(words[0], words[1], exercises):
                additional_points += Record_bonus_points
              if check_if_todays_quest(words[0]):
                additional_points += Quest_bonus_points
              additional_points += count_additional_points(words[0], words[1], exercises)
              greet_bot.send_message(last_chat_id, 'Вы записали упражнение: %s, получив %s баллов!' % (words[0], additional_points))
              current_week.points += additional_points
              weeks[len(weeks)-1] = current_week.write_into_string
              update_textfile_with_dict(weeks, './weeks.txt')

        #этот кусок ещё не чекал
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(
)
