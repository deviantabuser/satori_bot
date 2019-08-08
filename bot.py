import requests
import datetime
from dateutil import relativedelta
import os
from pytz import timezone

def createWeeksFile():
  return 'hz'

def get_dict_from_textfile(path):
    file = open(path,'r')
    text = file.read()
    strings = text.split('\n')
    words = []
    dictt = {}
    for word in strings:
      words.append(word.split(':'))
    for word in words:
      dictt[word[0]] = word[1]
    file.close()
    return dictt

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
now = datetime.datetime.now()

def main():
    new_offset = None
    weeks = get_dict_from_textfile('./weeks.txt')

    while True:
        print('i have entered the loop')
        greet_bot.get_updates(new_offset)

        time = datetime.datetime.now()
        time_local = time.astimezone(timezone('Asia/Yekaterinburg'))

        last_update = greet_bot.get_last_update()
        if time_local.hour == 0 and  time_local.minute == 13 :
          greet_bot.send_message(258274093, 'Напоминание!')
        if last_update is None: continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower()=='время' :
          greet_bot.send_message(last_chat_id, 'Текущее время: %s:%s' % (time_local.hour, time_local.minute))

        if last_chat_text.lower()=='дата' :
          greet_bot.send_message(last_chat_id, 'Сегодняшняя дата: %s.%s.%s' % (time_local.day, time_local.month, time_local.year))

        if last_chat_text.lower() in greetings :
            greet_bot.send_message(last_chat_id, 'Привет, {}'.format(last_chat_name))

        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()




#def
