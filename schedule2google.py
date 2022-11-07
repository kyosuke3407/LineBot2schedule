import csv
import googleapiclient.discovery
import google.auth

# ①Google APIの準備をする
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = '4e1009a2ca388a1542d035d10f8b45ed88ddc19784dea4628483e0b816141396@group.calendar.google.com'
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file('scheduleapi-366608-32e9631d3f92.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

# 1:休み 2:通し 3:短縮 4:通常
def startTimeconfig(y, m, d):
    r = str(y) + "-" + str(m) + "-" + str(d) + "T06:30:00"
    return r


def endTimeconfig(y, m, d, mode):
    r=""
    if mode == 2:
        r = str(y) + "-" + str(m) + "-" + str(d) + "T18:30:00"
    elif mode == 3:
        r = str(y) + "-" + str(m) + "-" + str(d) + "T12:00:00"
    elif mode == 4:
        r = str(y) + "-" + str(m) + "-" + str(d) + "T15:00:00"
    return r


# 1:休み 2:通し 3:短縮 4:通常
def dataloader(days, year,month):
    events = []

    for i in range(len(days)):
        if days[i] == 1:
            continue
        else:
            try:
                event = {
                    'summary': '出勤',
                    'location': '',
                    'description': '',
                    'start': {
                        'dateTime': '2015-05-28T09:00:00-07:00',
                        'timeZone': 'Japan',
                    },
                    'end': {
                        'dateTime': '2015-05-28T17:00:00-07:00',
                        'timeZone': 'Japan',
                    },
                }

                event["start"]["dateTime"] = startTimeconfig(year, month+1, i+1)
                event["end"]["dateTime"] = endTimeconfig(year, month+1, i+1, days[i])
                #print(event)
                events.append(event)
            except Exception as e:
                print(type(e))
                print(e.args)

    for i in events:
        print(i)
        i = service.events().insert(calendarId=calendar_id, body=i).execute()