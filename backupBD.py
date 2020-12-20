import shutil
import os
import datetime
from VK_BOT import Delete_OldHomework

FILE = 'Data Base/db.db'

if not os.path.isdir('Data Base/Backups'):
    os.mkdir('Data Base/Backups')

if os.path.isfile(FILE):
    shutil.copy(FILE, 'Data Base/Backups/db_' +
                datetime.datetime.now().strftime('%d-%m-%Y') + '.db')
    status = Delete_OldHomework(1)
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
