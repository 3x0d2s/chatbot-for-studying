from request_db import requestDB


id_admin = '132123123'
db = requestDB('Data Base/db.db')

dt = input()
db.add_Homework(id_admin, dt, '', '', '')


less = input()
db.changeHomw(id_admin, less)

# task = input()
