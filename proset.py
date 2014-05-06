##################
# Projective Set #
#  Sam Ettinger  #
#   April 2014   #
##################

import random, pygame, sys
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'

# Colors
aqua    = (0, 255, 255)
bgcol   = (230, 230, 230)
black   = (0, 0, 0)
blue    = (0, 0, 255)
fuschia = (255, 0, 255)
gray    = (128, 128, 128)
green   = (0, 128, 0)
lime    = (0, 255, 0)
orange  = (255, 165, 0)
red     = (255, 0, 0)
white   = (255, 255, 255)
yellow  = (255, 255, 50)
# saddlebrown = (139, 69, 19)

# (x,y) coords of top-left corner of cards in various modes
cardposlist = [
[(120, 100), (240, 100), (120, 270), (240, 270)],
[(120, 100), (240, 100), (60, 270),  (180, 270), (300, 270)],
[(60, 100),  (180, 100), (300, 100), (60, 270),  (180, 270), (300, 270)],
[(120, 100), (240, 100), (60, 270),  (180, 270), (300, 270), (120, 440), (240, 440)],
[(60, 100),  (180, 100), (300, 100), (120, 270), (240, 270), (60, 440),  (180, 440), (300, 440)],
[(60, 100),  (180, 100), (300, 100), (60, 270),  (180, 270), (300, 270), (60, 440),  (180, 440), (300, 440)],
[(120, 100), (240, 100), (360, 100), (60, 270),  (180, 270), (300, 270), (420, 270), (120, 440), (240, 440), (360, 440)]]

# (x,y) coords of dots' centers in various modes, relative to top-left corner of card
dotposlist = [
[(50, 25), (50, 75), (50, 125)],
[(25, 50), (75, 50), (25, 100), (75, 100)],
[(25, 25), (75, 25), (50, 75),  (25, 125), (75, 125)],
[(25, 25), (75, 25), (25, 75),  (75, 75),  (25, 125), (75, 125)],
[(50, 19), (25, 47), (75, 47),  (50, 75),  (25, 103), (75, 103), (50, 131)],
[(25, 19), (75, 19), (50, 47),  (25, 75),  (75, 75),  (50, 103), (25, 131), (75, 131)],
[(17, 25), (50, 25), (83, 25),  (17, 75),  (50, 75),  (83, 75),  (17, 125), (50, 125), (83, 125)]]

# Aaaaand colors of dots 1-n in difficulty level n
dotcollist = [
[red, yellow, blue],
[red, orange, blue,   fuschia],
[red, orange, green,  blue,   fuschia],
[red, orange, yellow, green,  blue,  fuschia],
[red, yellow, orange, green,  blue,  aqua,  fuschia],
[red, orange, lime,   yellow, green, aqua,  blue, fuschia],
[red, lime,   orange, yellow, gray,  green, blue, aqua, fuschia]]

# Dot radii, card size, etc
radius = 16
cardsize = (cardwidth, cardheight) = (100, 150)

# Choose number of bits on card (3-9)
pygame.init()
screen = pygame.display.set_mode((460, 660)) 
cardpos = cardposlist[3]
screen.fill(bgcol)
for k in range(7):
    power = k+3
    dotpos = dotposlist[k]
    dotcol = dotcollist[k]
    pos = (x,y) = (cardpos[k][0], cardpos[k][1])
    pygame.draw.rect(screen, bgcol, Rect(pos, cardsize))
    pygame.draw.rect(screen, black, Rect((x-1, y-1), (cardwidth+2, cardheight+2)), 1)
    for dot in range(power):
        pygame.draw.circle(screen, black, (x+dotpos[dot][0],y+dotpos[dot][1]), radius+2)
        pygame.draw.circle(screen, dotcol[dot], (x+dotpos[dot][0],y+dotpos[dot][1]), radius)
if pygame.font:
    font = pygame.font.Font(None, 24)
    font2 = pygame.font.Font(None, 18)
    title = font.render("Projective Set", 1, black)
    instr = font.render("Choose difficulty:", 1, black)
    rules1 = font2.render("RULE: Select a subset of cards such that each color has an even", 1, black)
    rules2 = font2.render("number of dots. COMMANDS: Number keys or click to toggle", 1, black)
    rules3 = font2.render("selection. Type \'c\' to clear selection. Type \'r\' to reset.", 1, black)
    titlep = title.get_rect(centerx=230, y=10)
    instrp = instr.get_rect(centerx=230, y=70)
    rules1p = rules1.get_rect(centerx=230, y=600)
    rules2p = rules2.get_rect(centerx=230, y=618)
    rules3p = rules3.get_rect(centerx=230, y=636)
    screen.blit(title, titlep)
    screen.blit(instr, instrp)
    screen.blit(rules1, rules1p)
    screen.blit(rules2, rules2p)
    screen.blit(rules3, rules3p)
pygame.display.update()

# Loop until power is chosen
power = 0
while power not in range(3,10):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            mousepos = event.pos
            for k in range(7):
                cardrect = Rect(cardpos[k], cardsize)
                if cardrect.collidepoint(mousepos): power = k+3
        elif event.type == KEYDOWN:
            if event.key == K_q: sys.exit()
            if event.key == K_1: power = 3
            if event.key == K_2: power = 4
            if event.key == K_3: power = 5
            if event.key == K_4: power = 6
            if event.key == K_5: power = 7
            if event.key == K_6: power = 8
            if event.key == K_7: power = 9

# Now that power's chosen, initialize things    
cardpos = cardposlist[power-3]
dotpos = dotposlist[power-3]
dotcol = dotcollist[power-3]

# Initialize Deck
deck = range(1,2**power)
random.shuffle(deck)
selected = []
inPlay = [0]*(power+1)

if power==9: width = 580
else: width = 460
if power==2: height = 270
elif power<6: height = 440
else: height = 610

size = (width, height)

screen = pygame.display.set_mode(size)

def drawdot(x,y,color):
    pygame.draw.circle(screen, black, (x,y), radius+2)
    pygame.draw.circle(screen, color, (x,y), radius)

def drawcard(x,y,num,isSelected):
    if num != 0:
        if isSelected: pygame.draw.rect(screen, gray, Rect((x,y),cardsize))
        else: pygame.draw.rect(screen, bgcol, Rect((x,y),cardsize))
        pygame.draw.rect(screen, black, Rect((x-1,y-1),(cardwidth+2,cardheight+2)),1)
        for k in range(power):
            if (2**k & num) == 2**k:
                drawdot(x+dotpos[k][0], y+dotpos[k][1], dotcol[k])

def isSet(cardlist):
    if len(cardlist)>2: return (reduce(lambda x,y:x^y,cardlist)==0)
    else: return False

win = False
sets = 0

clk = pygame.time.Clock()
ms = 0

while 1:
    # Check for win
    if len(deck)==0 and inPlay == [0]*(power+1):
        win = True
        # Change text?

    # Check if a valid set is selected
    if isSet(selected):
        for k in range(power+1):
            if inPlay[k] in selected: inPlay[k] = 0
        sets += 1
        selected = []
    
    # Check for selections
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            mousepos = event.pos
            for k in range(power+1):
                cardrect = Rect(cardpos[k], cardsize)
                if cardrect.collidepoint(mousepos):
                    if inPlay[k] in selected: selected.remove(inPlay[k])
                    else: selected.append(inPlay[k])
        elif event.type == KEYDOWN:
            if event.key == K_r:
                deck = range(1,2**power)
                random.shuffle(deck)
                selected = []
                inPlay = [0]*(power+1)
                ms = 0
                win = False
                sets = 0
            if event.key == K_c: selected = []
            if event.key == K_1 and power>0:
                if inPlay[0] in selected: selected.remove(inPlay[0])
                else: selected.append(inPlay[0])
            if event.key == K_2 and power>0:
                if inPlay[1] in selected: selected.remove(inPlay[1])
                else: selected.append(inPlay[1])
            if event.key == K_3 and power>1:
                if inPlay[2] in selected: selected.remove(inPlay[2])
                else: selected.append(inPlay[2])
            if event.key == K_4 and power>2:
                if inPlay[3] in selected: selected.remove(inPlay[3])
                else: selected.append(inPlay[3])
            if event.key == K_5 and power>3:
                if inPlay[4] in selected: selected.remove(inPlay[4])
                else: selected.append(inPlay[4])
            if event.key == K_6 and power>4:
                if inPlay[5] in selected: selected.remove(inPlay[5])
                else: selected.append(inPlay[5])
            if event.key == K_7 and power>5:
                if inPlay[6] in selected: selected.remove(inPlay[6])
                else: selected.append(inPlay[6])
            if event.key == K_8 and power>6:
                if inPlay[7] in selected: selected.remove(inPlay[7])
                else: selected.append(inPlay[7])
            if event.key == K_9 and power>7:
                if inPlay[8] in selected: selected.remove(inPlay[8])
                else: selected.append(inPlay[8])
            if event.key == K_0 and power>8:
                if inPlay[9] in selected: selected.remove(inPlay[9])
                else: selected.append(inPlay[9])

    # Deal cards
    if 0 in inPlay:
        for k in range(power+1):
            if inPlay[k]==0 and len(deck)>0: inPlay[k] = deck.pop()

    # Update time
    if not win: ms = ms + clk.tick()
    rawtime = int(ms/1000)
    second = rawtime%60
    strsec = str(second)
    if len(strsec)==1: strsec = '0'+strsec
    minute = ((rawtime-second)%3600)/60
    strmin = str(minute)
    if len(strmin)==1: strmin = '0'+strmin
    hour = (rawtime-second-(60*minute))/3600
    strhr = str(hour)
    
    # Draw display
    screen.fill(bgcol)
    if pygame.font:
        font = pygame.font.Font(None, 24)
        title = font.render("Projective Set", 1, black)
        timer = font.render(strhr + ':' + strmin + ':' + strsec, 1, black)
        nset = font.render("Sets: " + str(sets), 1, black)
        ncard = font.render("Cards left: " + str(len(deck)),1, black)

        titlep = title.get_rect(centerx=width/2, y=10)
        screen.blit(title, titlep)
        timerp = timer.get_rect(centerx=width/2, y=60)
        screen.blit(timer, timerp)
        nsetp = nset.get_rect(centerx = width/2-90, y=40)
        screen.blit(nset, nsetp)
        ncardp = ncard.get_rect(centerx=width/2+90, y=40)
        screen.blit(ncard, ncardp)        
    for card in range(power+1):
        if inPlay[card] != 0: drawcard(cardpos[card][0], cardpos[card][1], inPlay[card], (inPlay[card] in selected))
    pygame.display.update()
