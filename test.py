from bd_direct import bdDirect

db = bdDirect('Data Base/db.db')
#user = db.getUser(377648563)

db.changeUserHomewFlag(607216794, True)
db.changeUserSchedFlag(607216794, True)
db.changeUserAddHomewFlag(607216794, True)
db.changeUserDelHomewFlag(607216794, True)
db.changeUserGetLessDateFlag(607216794, True)
db.changeUserStepCode(607216794, 2)


db.close()
