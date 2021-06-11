# -*- coding: utf8 -*-
#
import os
import sys
import pathlib
#
sys.path.insert(1, os.path.join(sys.path[0], '..'))
#
from request_db import requestDB
from config.config import PATH_DB
#
PATH = str(pathlib.Path(__file__).parent.absolute())
PATH = os.path.normpath(PATH + os.sep + os.pardir)
#
db = requestDB(PATH + os.sep + PATH_DB)
db.clear_tabl_homew_us_f()
db.close()

