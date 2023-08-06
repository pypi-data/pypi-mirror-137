#
# PROGRAM: PYTHON CONSOLE DATABASE BROWSER
# MODULE : ORACLE DATABASE CONNECTOR
#

import cx_Oracle
import traceback
import sys
import os
import json
import curses
from pydbro.py_log import msg_log

connfile="sqlok_conn.json"

constr=None
dsn=None

def create_dns():
   global con
   global constr
   if os.path.exists(connfile):
     f = open(connfile, "r")
     dbcontmp = f.read()
     f.close()
     constr = json.loads(dbcontmp)
     dsn = cx_Oracle.makedsn(
       host=constr["host"],
       port=constr["port"], 
       service_name=constr["database"]
     )
     con = cx_Oracle.connect(
       user=constr["user"],
       password=constr["password"],
       dsn=dsn
     )
   else:
     curses.endwin()
     print("Please use coned to prepare connection")
     exit()

def set_conn(p_db_name):
  global connstr
  connstr=p_db_name

def get_conn():
  global connstr
  return(connstr)

def qry2dict(qry, qry_params=()):
  global constr
  global con
  data = None
  dsn = create_dns()
  res={}
  try:
    if con is None:
    #con = sqlite3.connect(get_conn())
      con = cx_Oracle.connect(
        user=constr["user"],
        password=constr["password"],
        dsn=dsn
      )
    cur = con.cursor()
    cur.execute(qry,qry_params)
    try:
      data = cur.fetchall()
    except Exception as e:
      con.commit()
      return
    cols=[]
    if cur.description is not None:
      for col in cur.description:
        cols.append(col[0])
    con.close()
    if len(data)>0:
      i=0
      for col in cols:
        res[col]=[]
        for row in data:
          res[col].append(row[i])
        i+=1
    #msg_log(dt+" "+str(qry)+"\n") 
    #msg_log(dt+" "+str(res)+"\n") 
    return (res,cols)
  except Exception as e:
    tramsg=""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traces = traceback.extract_tb(exc_traceback)
    for frame_summary in traces:
      tramsg+="{} {}".format(frame_summary.name, frame_summary.lineno)
    msg_log("ERROR : "+str(e)+" "+qry+" "+tramsg)
    pass
