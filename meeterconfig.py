from RGBcolors import *

payrate = {
    'employee': 200,
    'exec' : 300,
    'consultant' : 350
}
DEFAULTCURRENCY='USD'
DEFAULTDURATION=60 # Minutes
MEETINGTITLE="The Wonderful World of Meetings!"
MEETERBOARDWIDTH = 1024
MEETERBOARDHEIGHT = 768
MEETERBOARDSIZE = (MEETERBOARDWIDTH, MEETERBOARDHEIGHT)
DEFAULTFONT = 'Calibri'
ATTENDEELIST = 'attendeelist.txt'
PRIZEIMAGE="tesla.jpg"
PRIZECOST=400
PADDING = 5
TICKERAREAWIDTH=int(MEETERBOARDWIDTH*2/3)
TICKERAREAHEIGHT=int(MEETERBOARDHEIGHT/2)
TICKERAREA = (TICKERAREAWIDTH, TICKERAREAHEIGHT)

PRIZEAREAWIDTH=int(MEETERBOARDWIDTH*2/3)
PRIZEAREAHEIGHT=int(MEETERBOARDHEIGHT/2)
PRIZEAREA = ( PRIZEAREAWIDTH, PRIZEAREAHEIGHT)
PRIZEAREACOLOR = DARKORANGE

ATTENDEEAREAWIDTH=int(MEETERBOARDWIDTH/3)
ATTENDEEAREAHEIGHT=MEETERBOARDHEIGHT
ATTENDEEAREA=(ATTENDEEAREAWIDTH, ATTENDEEAREAHEIGHT)

ATTENDEENAMEWIDTH = int(ATTENDEEAREAWIDTH*2/3)
ATTENDEECOSTWIDTH = int(ATTENDEEAREAWIDTH/3)

ATTENDEELABELHEIGHT = ATTENDEECONTROLSHEIGHT = int(ATTENDEEAREAHEIGHT/20)