from urllib import request
from meeterconfig import *
from RGBcolors import *
import time
import pygame
from urllib.request import urlopen
import json

def get_quote(symbol):
    try:
        base_url = 'http://finance.google.com/finance/info?q='
        content = urlopen(base_url + symbol).read().decode()
        new_content = ''
        for i in range(6,len(content)-2):
            if content[i] != '\n':
                new_content = new_content + content[i]
        json_content = json.loads(new_content)
        price = json_content['l']
        change = json_content['c']
        last_trade = json_content['lt']
        return [ price, change, last_trade ]
    except:
        return [10,10,10]

def convertrate(usd, newcurrency):
    # This is an function to convert currency from USD to a given currency
    # Returns the numeric value of new currency
    base_url='http://api.fixer.io/latest?base=USD'
    content = request.urlopen(base_url).read().decode()
    content_json = json.loads(content)
    rates = content_json['rates']
    if (newcurrency in rates.keys()):
        return usd * rates[newcurrency]
    else:
        return usd

class Button(object):
    # Class that defines a generic button - can be used for labels, buttons
    def __init__(self, display, left, top, width, height, name, color=OFFWHITE, font=DEFAULTFONT, fontsize=20, fontcolor=BLACK):
        self.display = display
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.name = name
        self.color = color
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.textx = self.left + (self.width - self.fontsize/2 * len(self.name))/2 - 4*PADDING
        self.texty = self.top + (self.height - self.fontsize)/2
        self.add()

    def add(self, textorientation=None):
        # Method that adds the button. This method also doubles as the mechanism to update
        self.rect = pygame.draw.rect(self.display, self.color, (self.left, self.top, self.width, self.height))
        self.border = pygame.draw.rect(self.display, BLACK, (self.left, self.top, self.width, self.height),2)
        font = pygame.font.SysFont(self.font, self.fontsize)
        text = font.render(self.name, True, self.fontcolor)
        textpos = text.get_rect()
        if (textorientation == 'left'):
            textpos.left = self.rect.left + PADDING
        else:
            textpos.centerx = self.rect.centerx
        if (textorientation=="top"):
            textpos.top = self.top + PADDING
        else:
            textpos.centery = self.rect.centery
        self.display.blit(text, textpos)

    # The update method is the same as the add - the attributes can get changed outside the class and the update can be called
    update = add

class Attendee():
    # Class that defines an attendee
    def __init__(self, name='JaneJohn', attendeetype='employee'):
        self.name = name
        self.starttime = time.time()
        self.attendeetype = attendeetype
        self.payrate = payrate[self.attendeetype]
        self.present = False
        self.cost = 0
        self.color = GRAY

    def enter(self):
        self.present = True
        self.starttime = time.time()
        self.color = FORESTGREEN
        pygame.display.update(self.namelabel.rect)

    def leave(self):
        self.present = False
        self.color = DARKORANGE
        pygame.display.update(self.namelabel.rect)

    def updatecost(self):
        self.cost += (time.time() - self.starttime) * self.payrate / 3600
        self.starttime = time.time()

class MeeterBoard():
    # Class that defines the meeter board
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(DEFAULTFONT, 25)
        pygame.display.set_caption(MEETINGTITLE)
        self.screen = pygame.display.set_mode(MEETERBOARDSIZE, 0, 32)
        self.screen.fill(OFFWHITE)
        pygame.display.flip()

class PrizeObject():
    def __init__(self, display, prizearea):
        self.display = display
        self.area = prizearea
        self.prizeimage = pygame.image.load(PRIZEIMAGE)
        self.prizecost = float(PRIZECOST)

    def update(self, totalcost):
        #drawarea(self.display,0, TICKERAREAHEIGHT, PRIZEAREA, PRIZEAREACOLOR)
        self.totalcost = totalcost
        self.imagepos = self.prizeimage.get_rect()
        self.imagepos.centerx = self.area.centerx
        self.imagepos.centery = self.area.centery
        self.display.blit(self.prizeimage, self.imagepos)
        maskstartx = int(self.imagepos.left +  self.imagepos.width * totalcost/self.prizecost)
        maskwidth =  int(self.imagepos.width * (1 - totalcost/self.prizecost)) + PADDING
        #print(totalcost, self.imagepos.width, maskwidth)
        if self.totalcost < PRIZECOST:
            myrect = pygame.draw.rect(self.display, PRIZEAREACOLOR, (maskstartx, self.imagepos.top, maskwidth, self.imagepos.height))
            pygame.display.update(myrect)
        else:
            multiplier = self.totalcost/PRIZECOST
            multiplierstring = " x " + str("%.2f" % multiplier)
            self.prizemultiplier = Button(self.display, self.imagepos.right, self.imagepos.top, 65, 40, multiplierstring, color=PRIZEAREACOLOR, fontsize=20)
            self.prizemultiplier.add('left')

class TickerArea():
    def __init__(self, display):
        self.display = display
        drawarea(self.display, 0, 0, TICKERAREA)
        self.totalcost = 0
        self.update()

    def update(self):
        self.ticker = Button(self.display, 2*PADDING, 2*PADDING, TICKERAREAWIDTH - 3 * PADDING,
                             TICKERAREAHEIGHT - 3 * PADDING, str("$ %.2f" % self.totalcost), fontcolor=RED, fontsize=150)

class PrizeArea():
    def __init__(self, display, prizetype):
        self.display = display
        self.area = drawarea(self.display, 0, TICKERAREAHEIGHT, PRIZEAREA, PRIZEAREACOLOR)
        self.prize = ""
        self.prizetype = prizetype
        if prizetype == 'object':
            self.prizeobject = PrizeObject(self.display, self.area)

    def update(self, totalcost):
        if (self.prizetype == 'stock'):
            self.prize = Button(self.display, 2*PADDING, 2*PADDING + TICKERAREAHEIGHT, TICKERAREAWIDTH - 3 * PADDING,
                             TICKERAREAHEIGHT - 3 * PADDING, self.prize, fontcolor=DARKORANGE, fontsize=50)
        elif (self.prizetype == 'object'):
            self.prizeobject.update(totalcost)

class AttendeePanel():
    def __init__(self, display, attendees):
        self.display = display
        self.area = drawarea(self.display, TICKERAREAWIDTH, 0, ATTENDEEAREA, WHITE)
        self.attendees = attendees
        pygame.display.update()
        self.updateattendees()

    def addattendee(self):
        name = "Attendee #" + str(self.numattendees + 1)
        self.attendees.append(Attendee(name))
        self.updateattendees()

    def updateattendees(self):
        self.area = drawarea(self.display, TICKERAREAWIDTH, 0, ATTENDEEAREA, WHITE)
        self.numattendees = len(self.attendees)
        self.lblheight = int((ATTENDEEAREAHEIGHT - ATTENDEELABELHEIGHT - ATTENDEECONTROLSHEIGHT) / self.numattendees)
        top = ATTENDEELABELHEIGHT

        # Build the attendee labels
        for attendee in self.attendees:
            attendee.namelabel = Button(self.display,TICKERAREAWIDTH + PADDING, top, ATTENDEENAMEWIDTH-PADDING, self.lblheight, attendee.name, attendee.color)
            attendee.namelabel.add(textorientation='left')
            attendee.costlabel = Button(self.display, TICKERAREAWIDTH + ATTENDEENAMEWIDTH + PADDING, top, ATTENDEECOSTWIDTH - PADDING, self.lblheight, str("$ %.2f" % attendee.cost), LTGRAY)
            top += self.lblheight

        # Build the controls and the titles
        self.attendeetitle = Button(self.display, TICKERAREAWIDTH + PADDING, PADDING, ATTENDEENAMEWIDTH - PADDING,
                                        ATTENDEELABELHEIGHT, "Attendee", WHITE)

        self.costtitle = Button(self.display, TICKERAREAWIDTH + ATTENDEENAMEWIDTH + PADDING, PADDING,
                            ATTENDEECOSTWIDTH - PADDING, ATTENDEELABELHEIGHT, "Cost", WHITE)
        self.startall = Button(self.display, TICKERAREAWIDTH + PADDING, ATTENDEEAREAHEIGHT - ATTENDEECONTROLSHEIGHT,
                           int(ATTENDEEAREAWIDTH / 3) - PADDING, ATTENDEECONTROLSHEIGHT, "Start All", FORESTGREEN)
        self.endall = Button(self.display, TICKERAREAWIDTH + int(ATTENDEEAREAWIDTH / 3) + PADDING,
                         ATTENDEEAREAHEIGHT - ATTENDEECONTROLSHEIGHT, int(ATTENDEEAREAWIDTH / 3) - PADDING,
                         ATTENDEECONTROLSHEIGHT, "End All", DARKORANGE)
        self.plusbutton = Button(self.display, TICKERAREAWIDTH + int(2 * ATTENDEEAREAWIDTH / 3) + PADDING,
                             ATTENDEEAREAHEIGHT - ATTENDEECONTROLSHEIGHT, int(ATTENDEEAREAWIDTH / 3) - PADDING,
                             ATTENDEECONTROLSHEIGHT, "+", OFFWHITE)
        pygame.display.update(self.area)

def drawarea(display, left, top, area, color=BROWN):
    # A function to draw generic rectangles with borders
    width, height = area
    newarea = pygame.draw.rect(display, color, (left + PADDING, top + PADDING, width - PADDING, height - PADDING))
    areaborder = pygame.draw.rect(display, BLACK, (left + PADDING, top + PADDING, width - PADDING, height - PADDING), 2)
    return newarea

def getattendees():
    # A function to read the list of attendees
    # It is expected to see each attendee in a seaprate line
    # There can be a comma with the attendee type
    attendees = []
    with open(ATTENDEELIST, 'r') as attendeelist:
        for name in attendeelist:
            if name != "\n":
                name = name.replace('\n', '')
                if ',' in name:
                        name, type = name.split(',')
                        type = type.replace(' ', '')
                        print(name, type)
                else:
                    type = 'employee'
                attendees.append(Attendee(name, type))

        return attendees