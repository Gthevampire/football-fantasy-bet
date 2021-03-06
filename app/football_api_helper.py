import http.client
import json
import datetime


connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': 'fe4c5aaa344a40a78cef8547f5840478' }

class FootballDataApi:

    def get_week_matches(self, dateFrom, dateTo):
        connection.request('GET', '/v2/competitions/2015/matches?dateFrom='+dateFrom+'&dateTo='+dateTo, None, headers )
        return json.loads(connection.getresponse().read().decode())

    def get_this_week_matches(self):
        now = datetime.datetime.utcnow()
        week_number = datetime.date(now.year, now.month, now.day).isocalendar()[1]

        dateFrom, dateTo = self.get_start_and_end_date_from_calendar_week(now.year, week_number-1)
        week_match_data = self.get_week_matches(dateFrom, dateTo)

        match_list = []
        for i in range(0, week_match_data["count"]):
            match_list.append(week_match_data["matches"][i])

        return week_match_data["competition"], match_list

    def get_start_and_end_date_from_calendar_week(self, year, calendar_week):
        monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
        return self.format_date(monday), self.format_date(monday + datetime.timedelta(days=6.9))

    def format_date(self, date):
        return date.strftime('%Y-%m-%d')
