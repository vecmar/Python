# Hra Space Invaders
# Pygame Zero
# Pouzitie so suborom pre micro:bit space_micro.py.
# Ovladanie pohybu naklapanim microbita podla osi X, strelba tlacidlo A na micro:bite
# Autor: Mario Vecera

from random import randint
import serial

port = "COM3"
baud = 115200
s = serial.Serial(port)
s.baudrate = baud

WIDTH = 800
HEIGHT = 600


def draw():
    screen.fill((0, 0, 0))
    ship.draw()
    for s in range(len(shoots)):
        shoots[s].draw()
    for i in range(len(invaders)):
        invaders[i].draw()
    for b in range(len(barricade)):
        barricade[b].draw()
    screen.draw.text("SCORE " + str(score), topleft=(10,10), color=(255,0,0), fontsize=38)
    if ship.status > 0:
        ship.image = ("destroy")#ship.images[1]
        screen.draw.text("GAME OVER\nDo you want play again?\nPress Button B", center=(WIDTH/2, HEIGHT/2), color=(255,0,0), fontsize=52)
    if len(invaders) == 0 :
        screen.draw.text("GREAT, you killed all attackers\nDo you want play again?\nPress Button B", center=(WIDTH/2, HEIGHT/2), color=(255,0,0), fontsize=52)

def update():
    global ship,shoots,invaderStepTimer
    data = s.readline()
    come = 0
    try:
        come = int(data)
    except ValueError:
        print ("")
    if ship.status < 1 and len(invaders) > 0:
        if come > 250 and come < 5000 and ship.right < WIDTH:
            ship.right += 5
        if come < -250 and ship.left > 0:
            ship.left -= 5

        if come == 9999:
            if ship.rocketLoad == 1:
                ship.rocketLoad = 0
                clock.schedule(reloadRocket, 0.8)
                cs = len(shoots)
                shoots.append(Actor("rocket", (ship.x,ship.y)))
                shoots[cs].status = 0
                shoots[cs].type = 1
        shootsLife()
        invaderStepTimer += 1
        if invaderStepTimer == 30:
            invaderStepTimer = 0
            invadersLife()
    else:
        if come == 8888:
            newgame()

def reloadRocket():
    global ship
    ship.rocketLoad = 1

def shootsLife():
    global shoots, invaders, barricade
    for sn in range(len(shoots)):
        if shoots[sn].type == 0:
            shoots[sn].y += 2
            laserHit(sn)
            if shoots[sn].y > 600:
                shoots[sn].status = 1
        if shoots[sn].type == 1:
            shoots[sn].y -= 5
            rocketHit(sn)
            if shoots[sn].y < 10:
                shoots[sn].status = 1
    shoots = reorganizeList(shoots)
    invaders = reorganizeList(invaders)
    barricade = reorganizeList(barricade)

def reorganizeList(old):
    reorganized = []
    for nl in range(len(old)):
        if old[nl].status == 0: reorganized.append(old[nl])
    return reorganized

def laserHit(sn):
    global ship
    if ship.collidepoint((shoots[sn].x, shoots[sn].y)):
        ship.status = 1
        shoots[sn].status = 1
    for b in range(len(barricade)):
        if barricade[b].barricadeHit(shoots[sn]):
            barricade[b].status = 1
            shoots[sn].status = 1

def rocketHit(sn):
    global score
    for b in range(len(barricade)):
        if barricade[b].barricadeHit(shoots[sn]):
            shoots[sn].status = 1
    for i in range(len(invaders)):
        if invaders[i].collidepoint((shoots[sn].x, shoots[sn].y)):
            shoots[sn].status = 1
            invaders[i].status = 1
            score += 10

def invadersLife():
    global shoots, jumps, orientation
    stepX = stepY = 0
    if orientation == 1:
        if jumps > 0:
            stepX = +15
            jumps -= 1
        else:
            orientation = -1
            jumps = 15
            stepY = +40
    else:
        if jumps > 0:
            stepX = -15
            jumps -= 1
        else:
            orientation = 1
            jumps = 15
            stepY = +40
    for a in range(len(invaders)):
        animate(invaders[a], pos=(invaders[a].x + stepX, invaders[a].y + stepY), duration=0.25, tween='linear')
        if randint(0, 15) == 4:
            shoots.append(Actor("laser", (invaders[a].x,invaders[a].y)))
            shoots[len(shoots)-1].status = 0
            shoots[len(shoots)-1].type = 0
        if invaders[a].y > 460 and ship.status == 0:
            ship.status = 1

def barricadeHit(self, other):
    return (
        self.x-35 < other.x +5 and
        self.y+5 < other.y+20 and
        self.x+35 > other.x-5
    )

def newgame():
    global ship, orientation, jumps, shoots, score, invaderStepTimer
    ship = Actor("ship",(WIDTH/2, HEIGHT-50))
    orientation = ship.rocketLoad = 1
    invaderStepTimer = ship.status = score = ship.laserCountdown = 0
    jumps = 15
    newInvaders()
    newBarricade()
    shoots = []

def newInvaders():
    global invaders
    invaders = []
    invnum=0
    for row in range(4):
        for column in range(6):
            invaders.append(Actor("invader", (80+column*80,50+row*60)))
            invaders[invnum].status = 0
            invnum+=1

def newBarricade():
    global barricade
    barricade = []
    barnum = 0
    for column in range(7):
        for row in range(5):
            barricade.append(Actor("barricade", midbottom=(100+column*100,460+row*12)))
            barricade[barnum].barricadeHit = barricadeHit.__get__(barricade[barnum])
            barricade[barnum].status = 0
            barnum +=1

newgame()