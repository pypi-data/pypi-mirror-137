#!/usr/bin/python3
#
# (c) MMXXII UNKNOWN
#
# PROGRAM: PYTHON CONSOLE DATABASE BROWSER
# MODULE : MAIN PROGRAM
#
# VERSION: 0.1f
#
# CHANGELOG:
#
# 20220202 CONED [ CONNECTION EDITOR ]
# 20220201 BUGFIXING
# 20220131 ORA VERSION
# 20220130 INITIAL VERSION
#
# WORKDLOG:
#
# SCROLL, ORDER, FILTER
#
# BUGS:
#
# m,i in left fails when over the list
#
# TBD:
# 
# OPEN CELL VALUE IN WINDOW (FOR LONG TEXTS)
#

import curses
import traceback
import os.path
import sys

from pydbro.py_prn_list import prn_list
from pydbro.py_curses_lib import init_colors
from pydbro.py_key_moves import key_moves 
from pydbro.py_error_handler import error_handler
from pydbro.py_log import msg_log
from pydbro.py_cmd_params import cmd_params
import pydbro.py_break_handler

con = None
DB = None
screen = None
col = None
he = None
wi = None

def prn_intro_scr():
  logo = """ 

  ______   _____ ___   ___ ______    ____
  \     `\|  |  |   `\|   |\     `\/'    |
   |   T  |  |  |>    |  <__|   >  |     |
   |   '_,|__   |     |     |     /'  T  |
   |   |  __/  /|  T  |  T  |     `|  :  |
   |   | |     ||  '  |  '  |   |  |     |
   `---' `-----'`-----'-----'---'--`-----'
  %xxxxxxxxx<  CONSOLE PYTHON  >xxxxxxxxx%
  ----------< DATABASE BROWSER >----------
  %xxxxxxxxx< (c) 2022 UNKNOWN >xxxxxxxxx%
  ----------------------------------------

"""
  cls()
  curli=0
  shift = int(wi / 4)
  for line in logo.split('\n'):
    screen.move(curli,0+shift)
    screen.addstr(line,col["hiGr"])
    curli+=1
  screen.move(0,wi-1)
  screen.getch()
  cls()

str_help = """
  Help Keyboard Controls:
  
  ?   - this help
  
  j   - move down
  k   - move up
  h   - move left
  l   - move right
  L   - shift columns right
  H   - shift columns left
  0   - go to upper left table corner
  G   - go to lower right table corner
  n   - next 10 records
  u   - previous 10 records
  s   - sort ascending by current column
  S   - sort descending by current column
  f   - filter (enter claus after where ... )
  tab - toggle left / right panel (tables, table content)
  m   - move rows view by 1 page down
  i   - move rows view by 1 page up
  /   - in left panel filter table list
"""

sql_tab_cols = {
  "sqlite"   : "",
  "mysql"    : "",
  "postgres" : "",
  "oracle"   : ""
}

# sqlite
sql_tab_cols["sqlite"] = """-- GET TABLE COLUMNS
select group_concat(name,'|') as cols
from pragma_table_info('%TABLE%')
order by cid asc"""

# mysql
sql_tab_cols["mysql"] = """-- GET TABLE COLUMNS
SELECT group_concat(COLUMN_NAME) as cols
  FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = 'bhxfcz9969' AND TABLE_NAME = '%TABLE%'""";

# postgres
sql_tab_cols["postgres"] = """-- GET TABLE COLUMNS
select string_agg(column_name,'|') as cols
from information_schema.columns
where table_name = '%TABLE%'
and table_schema = 'public'
and table_catalog = 'osm'"""

# oracle
sql_tab_cols["oracle"] = """-- GET TABLE COLUMNS
select listagg(column_name,'|') as "cols"
from user_tab_columns
where table_name = '%TABLE%'
order by column_name asc"""

sql_get_tabs = {
  "sqlite": "",
  "mysql": "",
  "postgres": "",
  "oracle": ""
}

# sqlite
sql_get_tabs["sqlite"] = """-- GET TABLES
select name
from sqlite_master sm
where type in ('table','view')
order by name asc
limit ?, ?"""

# mysql
sql_get_tabs["mysql"] = """-- GET TABLES
select table_name as "name"
from information_schema.tables
where %FILTER%
and table_schema = 'bhxfcz9969'
order by table_name asc
limit %s, %s"""

# postgres 
sql_get_tabs["postgres"] = """-- GET TABLES
select table_name "name"
from information_schema.tables
where %FILTER%
and table_catalog in ('osm')
and table_schema in ('public')
order by table_name asc
limit 10 offset 0"""

# oracle
sql_get_tabs["oracle"] = """-- GET TABLES
select table_name as "name"
from user_tables sm
where %FILTER%
order by table_name asc
offset :1 rows fetch 
next :2 rows only"""

sql_get_tab = {
  "sqlite"    : "",
  "mysql"     : "",
  "postgres"  : "",
  "oracle"    : ""
}

# sqlite
sql_get_tab["sqlite"] = """-- GET TABLE CONTENT
select a.rowid, a.*
from %TABLE% a
where %FILTER%
order by %SORTED%
limit ?, ?"""

# mysql
sql_get_tab["mysql"] = """-- GET TABLE CONTENT
select @rowid:=@rowid+1 as rowid, a.*
from %TABLE% a, (select @rowid := 0) as init
where %FILTER%
order by %SORTED%
limit %s, %s"""

# mysql
sql_get_tab["postgres"] = """-- GET TABLE CONTENT
-- select row_number() over (order by 1 asc) as rowid, a.*
select 1 rowid, a.*
from %TABLE% a
where %FILTER%
order by %SORTED%
limit 10 offset 0"""

# oracle
sql_get_tab["oracle"] = """-- GET TABLE CONTENT
select a.rowid as "rowid", a.*
-- select 1 as "rowid", a.*
from %TABLE% a
where %FILTER%
order by %SORTED%
offset :1 rows fetch 
next :2 rows only"""

def prn_title(title):
  screen.move(he-1,0)
  screen.clrtoeol()
  screen.addstr(str(title),col["loGr"])

def prn_info(p_str):
  screen.move(he-2,0)
  screen.clrtoeol()
  screen.addstr(str(p_str),col["miGr"])


def cls():
  #screen.clear()
  screen.move(0,0)
  cy=0
  for cy in range(0,he):
    screen.move(cy,0)
    screen.clrtoeol()

def read_str(p_banner):
  curses.curs_set(1)
  key = "0"
  str = ""
  screen.move(he-1,0)
  screen.addstr(p_banner,col["hiGr"])
  screen.move(0,0)
  while key != 10:
    screen.clrtoeol()
    key = screen.getch()
    if (    
         (key >= ord("0") and key <= ord("9"))
      or (key >= ord("A") and key <= ord("Z"))
      or (key >= ord("a") and key <= ord("z"))
      or  key == ord("=")  or  key == ord(" ")
      or  key == ord(">")  or  key == ord("<")
      or  key == ord("_")  or  key == ord("-")
      or  key == ord("%")  or  key == ord("*")
      or  key == ord("!")  or  key == ord("$")
      or  key == ord('"')  or  key == ord("'")
      or  key == ord("(")  or  key == ord(")")
      or (key == 127 or key == 263 or key == 8)
    ):
      strlen = len(str)
      if (key == 127 or key == 263 or key == 8):
        if strlen >= 0:
          str = str[:-1]
          strlen = len(str)
          screen.move(0,strlen)
          screen.delch()
      else:
        str += chr(key)
        screen.attrset(col["hiGr"])
        screen.addch(chr(key))
  return(str)

def main():

  global screen
  global col
  global he
  global wi

  try:
  
    # PROCESS PROGRAM COMMAND LINE PARAMETER
    dbfile = ""
    DB, dbfile = cmd_params(sys.argv)
  
    from pydbro.py_qry import setup_qry_method
    qry2dict = setup_qry_method(DB,dbfile)
  
    # CURSES INIT
    screen = curses.initscr()
    curses.noecho()
    col = init_colors()
    he, wi = screen.getmaxyx()
  
    #prn_intro_scr()
  
    curx=0; cury=1; maxx = 0; maxy=0; k=None;
    cur_win = "left"
    p_cur_win = "left"
    tabf = 0
    tabt = 0
    rcurx = 0
    rcury = 1
    rtabf = 0
    rtabt = he - 1
    rsortcol = 1
    act = ""
    is_sorted = 0 
    sortdir = "asc"
    rfilter = "1=1"
    filtered = 0
    maxxd = 1
    maxyd = 1
    curtabsf = 0      # table list shift
    curtabst = he - 2 # table list shift sizeeee
    colshift = 0      # right table column shift
    voidcs = 0        # dummy colshift for left call
    lfiltered = 0     # table list filtered
    prev_tab_sql = ""
    prev_tab_params = None
    prev_tabs_sql = ""
    prev_tabs_params = None
    cols = None
    colsl = None
  
    # MAIN INTERACTION
    while k != ord("q"):
      he, wi = screen.getmaxyx()
      p_cur_win = cur_win
      if cur_win == "left":
        curx, cury, cur_win, tabf, tabt, act, curtabsf, colshift  = key_moves(
          he,wi,k,curx,cury,maxx,maxy,cur_win,tabf,tabt,act,curtabsf,colshift
        )
      else:
        rcurx, rcury, cur_win, rtabf, rtabt, act, curtabsf, colshift  = key_moves(
          he,wi,k,rcurx,rcury,maxxd,maxyd,cur_win,rtabf,rtabt,act,curtabsf,colshift
        )
      #cols=["None"]
      if cur_win != p_cur_win:
        rcurx = 0
        rcury = 1 
        rtabf = 0
        sortdir = ""
        rsortcol = 1
        rfilter = "1=1"
        colshift = 0
        filtered = 0
        is_sorted = 0
        #sql_cur_cols = sql_tab_cols[DB].replace('%TABLE%',cur.replace('\n',''))
        #cols = qry2dict(sql_cur_cols,())
      if act == "filter" and cur_win == "left":
        lfilter = ""
        screen.move(0,0)
        lfilter = read_str("Enter tables filter: lower(table) name like '%...%'")
        if lfilter == "":
          lfiltered = 0
        else:
          lfiltered = 1
          cury=1
        act = ""
        screen.move(0,0)
        screen.clrtoeol()
        sql_act_tabs = sql_get_tabs[DB].replace(
          '%FILTER%',"lower(table_name) like '%{}%'".format(lfilter)
        )
      elif lfiltered == 0:
        lfilter = "1=1"
        sql_act_tabs = sql_get_tabs[DB].replace(
          '%FILTER%',"{}".format(lfilter)
        )
      if cur_win == "left":
        #cur, maxx, maxy, xcolsz = prn_list(
        #  qry2dict,screen,wi,he,sql_act_tabs,(curtabsf,curtabst,),0,0,curx,cury,0,voidcs
        #)
        cur_tabs_params = (curtabsf,curtabst,)
        if prev_tabs_sql != sql_act_tabs or prev_tabs_params != cur_tab_params:
          resl,colsl=qry2dict(sql_act_tabs,cur_tabs_params)
          prev_tabs_sql=sql_act_tabs
          prev_tab_params=cur_tabs_params
        cur, maxx, maxy, xcolsz = prn_list(
          resl,screen,he,wi,0,0,curx,cury,0,voidcs
        )
      sql_cur_tab = sql_get_tab[DB].replace('%TABLE%',cur.replace('\n',''))
      # FILTER
      #cols = qry2dict(sql_tab_cols[DB].replace('%TABLE%',cur.replace('\n','')))
      if act == "filter" and cur_win == "right":
        key=""
        rfilter = ""
        screen.move(0,0)
        rfilter = read_str("Enter table filter: where ... ")
        if rfilter == "":
          rfilter = "1=1"
        act = ""
        filtered = 1
        screen.move(0,0)
        screen.clrtoeol()
      if filtered == 0:
        sql_cur_tab = sql_cur_tab.replace('%FILTER%',"1=1")
      else:
        sql_cur_tab = sql_cur_tab.replace('%FILTER%',rfilter)
      if act == "asc" or act == "desc": 
        rsortcol = rcurx+2
        sql_cur_tab = sql_cur_tab.replace('%SORTED%',str(rsortcol)+" "+act)
        is_sorted = rsortcol
        sortdir = act
      if is_sorted == 0:
        sql_cur_tab = sql_cur_tab.replace('%SORTED%',"1 asc")
      screen.move(0,wi-1)
      sql_cur_tab = sql_cur_tab.replace('%FILTER%',rfilter)
      if act == "asc" or act == "desc": 
        rsortcol = rcurx+2
        sql_cur_tab = sql_cur_tab.replace('%SORTED%',str(rsortcol)+" "+act)
        is_sorted = rsortcol
        sortdir = act
      if is_sorted != 0:
        sql_cur_tab = sql_cur_tab.replace('%SORTED%',str(rsortcol)+" "+sortdir)
      if cur_win == "left":
        rwinshift=sum(xcolsz)+1
      else:
        rwinshift=2
        screen.move(0,0)
        screen.addstr("<",col["loGr"])
        if colshift > 0:
          screen.move(1,0)
          screen.addstr("<",col["loGr"])
      try:
        cur_tab_params = (rtabf,rtabt,)
        if sql_cur_tab != prev_tab_sql or cur_tab_params != prev_tab_params:
          res,cols = qry2dict(sql_cur_tab,cur_tab_params)
          prev_tab_sql = sql_cur_tab
          prev_tab_params = cur_tab_params
        #curd, maxxd, maxyd, xcoldsz = prn_list(
        #  qry2dict,res,screen,wi,he,sql_cur_tab,(rtabf,rtabt),rwinshift,0,rcurx,rcury,1,colshift
        #)
        curd, maxxd, maxyd, xcoldsz = prn_list(
          res,screen,he,wi,rwinshift,0,rcurx,rcury,1,colshift
        )
      except Exception as e:
        error_handler(screen,he,wi,e,sys.exc_info())
        screen.refresh()
        tmp = screen.getch()
      if maxyd == 0: # NO DATA
        screen.move(0,rwinshift)
        screen.addstr(str('|'.join(cols[1:]))[:(wi-1-rwinshift)],col["miGr"])
        screen.move(1,rwinshift)
        screen.addstr("--| NO DATA |--",col["miGr"])
      if act == "help": 
        prn_intro_scr()
        sy=0
        for li in str_help.split("\n"):
          screen.move(sy,0)
          screen.addstr(li,col["miGr"])
          sy+=1
        screen.move(he-1,0)
        #screen.addstr("Press any key ...",col["loGr"])
        #screen.getch()
      curcol=""
      screen.move(0,wi-1)
      if len(cols)>0:
        curcol=cols[rcurx+colshift+1]
      prn_title(DB+" "+cur_win[0]+" ")
      if filtered == 1:
        screen.addstr("f ",col["loGr"])
      if is_sorted > 0:
        screen.addstr("s ",col["loGr"])
      screen.addstr(cur+" ",col["miGr"])
      #screen.addstr(str(curcol),col["hiGr"])
      screen.addstr(curcol,col["hiGr"])
      screen.move(0,wi-1)
      curses.curs_set(0)
      k = screen.getch()
      he, wi = screen.getmaxyx()
      cls()
    curses.endwin()
  except Exception as e:
    curses.noecho()
    curses.endwin()
    traceback.print_exc(file=sys.stdout)
    exit()

def cli():
  main()

if __name__ == '__main__':
  main()
