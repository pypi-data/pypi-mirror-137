#
# PROGRAM: PYTHON CONSOLE DATABASE BROWSER
# MODULE : READ USER INPUT AS STRING
#

import curses

def read_str(screen, col, p_banner, strdef = "", passwd = 0):
  curses.curs_set(1)
  key = "0"
  if strdef != "":
    vstr = strdef
  else:
    vstr = ""
  screen.move(0,0)
  screen.addstr(p_banner,col["miGr"])
  #screen.move(1,0)
  #screen.addstr("-"*(wi-1),col["loGr"])
  screen.move(1,0)
  if len(vstr)>0:
    if passwd == 1:
      screen.addstr("*"*(len(vstr)),col["hiGr"])
    else:
      screen.addstr(vstr,col["hiGr"])
  while key != 10:
    #screen.clrtoeol()
    key = screen.getch()
    if (
         (key >= ord(" ") and key <= ord("~"))
      or (key == 127 or key == 263 or key == 8)
    ):
      strlen = len(vstr)
      if (key == 127 or key == 263 or key == 8):
        if strlen >= 0:
          vstr = vstr[:-1]
          strlen = len(vstr)
          screen.move(1,strlen)
          screen.delch()
      else:
        vstr += chr(key)
        screen.attrset(col["hiGr"])
        if passwd == 1:
          screen.addch("*")
        else:
          screen.addch(chr(key))
  curses.curs_set(0)
  return(vstr)


