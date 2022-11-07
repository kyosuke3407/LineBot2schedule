import imgs2calender
import datetime
import calendar
import schedule2google


if __name__ == '__main__':
    dt_now = datetime.datetime.now()
    dt_now = dt_now + datetime.timedelta(days=30)

    #画像処理
    day = imgs2calender.img2schedule(dt_now)

    # 1:休み 2:通し 3:短縮 4:通常
    events = schedule2google.dataloader(day, dt_now.year, dt_now.month)



