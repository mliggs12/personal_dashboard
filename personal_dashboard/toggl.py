import requests
from .personal_info import TOGGL_API_TOKEN
import base64
import decimal
import time
import datetime as DT


#The Toggl class is meant to get the pomodoro sessions using the get_pomodoros method
class Toggl():
    def __init__(self):
        headers = {
                "Authorization": "",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "User-Agent": "python/urllib",
            }
        authHeader = TOGGL_API_TOKEN + ":" + "api_token"
        authHeader = "Basic " + str(base64.b64encode(authHeader.encode()))[2:]
        authHeader = authHeader.replace('\'', "")
        headers['Authorization'] = authHeader
        url = 'https://www.toggl.com/api/v8/time_entries?api_token=fab0834862bcf57035b57bb39f0ae13f'
        self.json = requests.get(url, headers=headers).json()


    def get_pomodoros(self, dates):
        pomodoroDict = {}
        for index, time_entry in enumerate(self.json):
            end_time = time_entry['start'].split('T')[0]
            if end_time in dates:
                time_in_hours = decimal.Decimal(time_entry['duration']/60/60)
                description = time_entry['description']
                if time_in_hours < 0:
                    epoch_time = int(time.time())
                    time_in_hours = decimal.Decimal((epoch_time + time_entry['duration'])/60/60)
                if description in pomodoroDict:
                    pomodoroDict[description] += float(round(time_in_hours, 2))
                else:
                    pomodoroDict[description] = float(round(time_in_hours, 2))
        return pomodoroDict

    def get_daily_pomodoros(self):
        dates = [time.strftime("%Y-%m-%d")]
        return self.get_pomodoros(dates)


    def get_past_seven_days_pomodoros(self):
        dates = []
        today = DT.date.today()
        for i in range(7):
            date = today - DT.timedelta(days=i)
            date = date.strftime("%Y-%m-%d")
            dates.append(date)
        return self.get_pomodoros(dates)
