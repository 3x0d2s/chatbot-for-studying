import shutil
import os
import datetime
from request_db import requestDB
import config_pars


FILE = 'Data Base/db.db'


def delete_OldHomework():
    db = requestDB('Data Base/db.db')
    allHomework = db.get_allHomework()
    wasItDeleted = False
    #
    rowcount = len(allHomework)
    if rowcount > 0:
        now = datetime.datetime.now().replace(
            hour=0, second=0, microsecond=0, minute=0)
        for row in range(rowcount):
            date = allHomework[row][0]
            homew_date = datetime.datetime.strptime(
                date, '%d.%m.%Y')
            if now > homew_date:
                lesson = allHomework[row][1]
                db.del_Homework(date, lesson)
                if wasItDeleted == False:
                    wasItDeleted = True
    #
    if wasItDeleted == True:
        return True
    else:
        return False
    db.close()


if not os.path.isdir('Data Base/Backups'):
    os.mkdir('Data Base/Backups')


if os.path.isfile(FILE):
    shutil.copy(FILE, 'Data Base/Backups/db_' +
                datetime.datetime.now().strftime('%d-%m-%Y') + '.db')
    status = delete_OldHomework()
    logfile = open('Data Base/log.txt', 'a', encoding='utf-8')
    if status == True:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание очищено.\n')
    else:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание не было найдено.\n')
    logfile.close()
else:
    logfile = open('Data Base/log.txt', 'a', encoding='utf-8')
    logfile.write('[' + str(datetime.datetime.now()) +
                  '] - Ошибка бэкапа: отсуствует файл БД.\n')
    logfile.close()

config_pars.changeWeekConfig('Settings.ini')
