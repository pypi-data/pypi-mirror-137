#
# PROGRAM: PYTHON CONSOLE DATABASE BROWSER
# MODULE : POSTGRES DATABASE CONNECTOR
#

import psycopg2
import traceback
import sys
import os
import json
import curses
from pydbro.py_log import msg_log

connfile = "sqlpk_conn.json"

constr = None
dsn = None

def create_con():
    global con
    global constr
    if os.path.exists("sqlpk_conn.json"):
        f = open("sqlpk_conn.json", "r")
        dbcontmp = f.read()
        f.close()
        constr = json.loads(dbcontmp)
    else:
        curses.endwin()
        print("Please use coned to prepare connection")
        exit()
    #print(str(constr))
    con = psycopg2.connect(**constr)
    return(con)

def set_conn(p_db_name):
    global connstr
    connstr = p_db_name

def get_conn():
    global connstr
    return connstr

def qry2dict(qry, qry_params=()):
    global constr
    global con
    res = {}
    try:
      con = create_con()
      cur = con.cursor()
      cur.execute(qry, qry_params)
      #con.commit()
      data = cur.fetchall()
      cols = []
      for col in cur.description:
        cols.append(col[0])
      con.close()
      if len(data) > 0:
        i = 0
        for col in cols:
          res[col] = []
          for row in data:
            res[col].append(row[i])
          i += 1
      return(res,cols)
    except Exception as e:
      #traceback.print_exc(file=sys.stdout)
      #print(str(e))
      msg_log("ERROR : " +str(e) + qry)
      pass
 
