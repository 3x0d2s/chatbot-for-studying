import shutil
import os
import datetime
from request_db import requestDB
import config_pars
import pathlib
#
PATH = str(pathlib.Path(__file__).parent.absolute())
FILE = PATH + '/Data Base/db.db'
#


def delete_OldHomework():
    db = requestDB(FILE)
    allHomework = db.get_allHomework()
    wasItDeleted = False
    #
    rowcount = len(allHomework)
    if rowcount > 0:
        now = datetime.datetime.now().replace(
            hour=0, second=0, microsecond=0, minute=0)
        delt = 7 + datetime.datetime.now().weekday()
        dur_days = datetime.timedelta(days=(delt))
        dStartLastWeek = now - dur_days
        #
        for row in range(rowcount):
            date = allHomework[row][0]
            homew_date = datetime.datetime.strptime(
                date, '%d.%m.%Y')
            #
            if homew_date < dStartLastWeek:
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


if not os.path.isdir(PATH + '/Data Base/Backups'):
    os.mkdir(PATH + '/Data Base/Backups')


if os.path.isfile(FILE):
    shutil.copy(FILE, PATH + '/Data Base/Backups/db_' +
                datetime.datetime.now().strftime('%d-%m-%Y') + '.db')
    status = delete_OldHomework()
    logfile = open(PATH + '/Data Base/log.txt', 'a', encoding='utf-8')
    if status == True:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание очищено.\n')
    else:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание не было найдено.\n')
    logfile.close()
else:
    logfile = open(PATH + '/Data Base/log.txt', 'a', encoding='utf-8')
    logfile.write('[' + str(datetime.datetime.now()) +
                  '] - Ошибка бэкапа: отсуствует файл БД.\n')
    logfile.close()

config_pars.changeWeekConfig(PATH + '/Settings.ini')
