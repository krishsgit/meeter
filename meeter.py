from meeterclasses import *
# This is a program to calculate the cost of meetings

'''
Here is what the program is supposed to do

Inputs:
    A name for the meeting
    Number of regular attendees
    Number of executive attendees
    Number of consultants
    Average rate of pay ($200/hour, execs at $300, consultants at $250)
    Have a start time
    Have a pause
    Have a stop
    Currency (default USD)

Outputs:
    An odometer style ticker that shows price as it rises
    A clock that shows seconds/minues elapsed
    An amazon or other shopping API that periodically fetches a random object for a given price (say every 5 minutes)
    And/or something that can be done in "x" minutes

UI:
    Input:
        Textbox for input of meeting name
        +/- counter for number of attendees, execs and consultants
        Start button, pause button and stop button
        Expected duration

    Output:
        Odometer for cost
        Timer for time
        Goodies for purchaseable objects

Calculatons:
    Simple multiplication of rate of pay
'''

if (__name__ == '__main__'):
    #newcurrency="INR"
    #converted=convertrate(200, newcurrency)
    #print(newcurrency, converted)

    stockticker = "VMW"
    stockquote = get_quote(stockticker)
    stockprice = float(stockquote[0])

    print(stockticker, " stock is at ", stockprice)

    meeterboard = MeeterBoard()
    tickerarea = TickerArea(meeterboard.screen)
    prizearea = PrizeArea(meeterboard.screen, 'object')

    attendees = getattendees()
    attendeepanel = AttendeePanel(meeterboard.screen, attendees)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                for attendee in attendees:
                    if attendee.namelabel.rect.collidepoint(pos):
                        if attendee.present:
                            attendee.leave()
                        else:
                            attendee.enter()

                if attendeepanel.startall.rect.collidepoint(pos):
                    for attendee in attendees:
                            if not attendee.present:
                                attendee.enter()
                elif attendeepanel.endall.rect.collidepoint(pos):
                    for attendee in attendees:
                        if attendee.present:
                            attendee.leave()
                elif attendeepanel.plusbutton.rect.collidepoint(pos):
                    attendeepanel.addattendee()

        tickerarea.totalcost = 0
        for attendee in attendees:
            if attendee.present:
                attendee.updatecost()

            tickerarea.totalcost += attendee.cost
            prizearea.prize = "# of " + stockticker + " shares: " + str("%.1f" % (tickerarea.totalcost / stockprice))

        attendeepanel.updateattendees()
        tickerarea.update()
        prizearea.update(tickerarea.totalcost)
