# -*- coding: utf8 -*-
#
import os
import sys
import pathlib
#
sys.path.insert(1, os.path.join(sys.path[0], '..'))
#
import shutil
import datetime
from request_db import requestDB
import config_pars
from config.config import PATH_SETTINGS, PATH_DB
#
#
PATH = str(pathlib.Path(__file__).parent.absolute())
PATH = os.path.normpath(PATH + os.sep + os.pardir)
FILE = PATH + os.sep + PATH_DB
#


def delete_old_homework():
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
    db.close()
    return wasItDeleted


if not os.path.isdir(PATH + f'{os.sep}db{os.sep}Backups'):
    os.mkdir(PATH + f'{os.sep}db{os.sep}Backups')


if os.path.isfile(FILE):
    shutil.copy(FILE, PATH + f'{os.sep}db{os.sep}Backups{os.sep}db_' +
                datetime.datetime.now().strftime('%Y-%m-%d') + '.db')
    status = delete_old_homework()
    logfile = open(PATH + f'{os.sep}db{os.sep}log.txt', 'a', encoding='utf-8')
    if status == True:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание очищено.\n')
    else:
        logfile.write('[' + str(datetime.datetime.now()) +
                      '] - Cоздан бэкап базы данных, старое домашнее задание не было найдено.\n')
    logfile.close()
else:
    logfile = open(PATH + f'{os.sep}db{os.sep}log.txt', 'a', encoding='utf-8')
    logfile.write('[' + str(datetime.datetime.now()) +
                  '] - Ошибка бэкапа: отсуствует файл БД.\n')
    logfile.close()

config_pars.change_week_config(PATH_SETTINGS)
