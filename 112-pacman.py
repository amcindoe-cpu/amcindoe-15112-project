from cmu_graphics import *

def withinRect(cx, cy, left, top, width, height):
    radius = 11
    closestX = max(left, min(cx, left + width))
    closestY = max(top, min(cy, top + height))
    dx = cx - closestX
    dy = cy - closestY
    return (dx * dx + dy * dy) <= (radius * radius)

def eatPellet(app):
    for i in range(len(app.pellets)):
        pelletX, pelletY = app.pellets[i]
        dx = app.pacmanX - pelletX
        dy = app.pacmanY - pelletY
        if (dx * dx + dy * dy)**0.5 <= 11:
            app.score += 10
            app.pellets.pop(i)
            break

def collidesWithGhost(app):
    for ghostX, ghostY in app.antagonistPositions:
        dx = app.pacmanX - ghostX
        dy = app.pacmanY - ghostY
        if (dx * dx + dy * dy)**0.5 <= 11:
            return True
    return False

def onAppStart(app):
    app.steps = 0
    app.background = 'black'
    app.height = 650
    app.width = 460
    app.lives = 3
    app.score = 0
    app.rotation = 'right'
    app.gameOver = False
    app.pacmanX = 230
    app.pacmanY = 455
    app.lifeIcons = [(15, 635), (45, 635), (75, 635)]
    app.ghostColors = ['red', 'pink', 'cyan', 'orange']
    app.antagonistPositions = [(230, 275), (200, 305), (230, 305), (260, 305)] #In order: Blinky, Pinky, Inky, Clyde
    app.walls = {(5,50,30,30), (35,50,30,30), (65,50,30,30), (95,50,30,30), #top row of walls
                 (125,50,30,30), (155,50,30,30), (185,50,30,30), (215,50,30,30), #top row of walls
                 (245,50,30,30), (275,50,30,30), (305,50,30,30), (335,50,30,30), #top row of walls
                 (365,50,30,30), (395,50,30,30), (425,50,30,30), (215,80,30,30), #first two rows
                 (35,110,30,30), (65,110,30,30), (125,110,30,30), (155,110,30,30), #Third row, left side
                 (215,110,30,30), (275,110,30,30), (305,110,30,30), (365,110,30,30), #Third row, right side
                 (395,110,30,30), (35,170,30,30), (65,170,30,30), (125,170,30,30), #Fifth row, left side
                 (185,170,30,30), (215,170,30,30), (245,170,30,30), (305,170,30,30), #Fifth row, middle
                 (365,170,30,30), (395,170,30,30), (125,200,30,30), (215,200,30,30), #6th row
                 (305,200,30,30), (5,230,30,30), (35,230,30,30), (65,230,30,30), #7th row left
                 (125,230,30,30), (155,230,30,30), (215,230,30,30), (275,230,30,30), #7th row center
                 (305,230,30,30), (365,230,30,30), (395,230,30,30), (425,230,30,30), #7th row end
                 (5,260,30,30), (35,260,30,30), (65,260,30,30), (125,260,30,30), #8th row left
                 (305,260,30,30), (365,260,30,30), (395,260,30,30), (425,260,30,30), #8th row right
                 (5,320,30,30), (35,320,30,30), (65,320,30,30), (125,320,30,30), #10th row left
                 (305,320,30,30), (365,320,30,30), (395,320,30,30), (425,320,30,30), #10th row right
                 (5,350,30,30), (35,350,30,30), (65,350,30,30), (125,350,30,30), #11th row left
                 (185,350,30,30), (215,350,30,30), (245,350,30,30), (305,350,30,30), #11th row middle
                 (365,350,30,30), (395,350,30,30), (425,350,30,30), (215,380,30,30), #11th row right
                 (35,410,30,30), (65,410,30,30), (125,410,30,30), (155,410,30,30), #13th row left
                 (215,410,30,30), (275,410,30,30), (305,410,30,30), (365,410,30,30), #13th row middle-right
                 (395,410,30,30), (65,440,30,30), (365,440,30,30), (5,470,30,30), #14th/PACMAN row
                 (65,470,30,30), (125,470,30,30), (185,470,30,30), (215,470,30,30), #15th row left
                 (245,470,30,30), (305,470,30,30), (365,470,30,30), (425,470,30,30), #15th row right
                 (125,500,30,30), (215,500,30,30), (305,500,30,30), (35,530,30,30), #16th row
                 (65,530,30,30), (95,530,30,30), (125,530,30,30), (155,530,30,30), #17th row, left side
                 (215,530,30,30), (275,530,30,30), (305,530,30,30), (335,530,30,30), #17th row right
                 (365,530,30,30), (395,530,30,30), (5,590,30,30), (35,590,30,30), #Bottom row
                 (65,590,30,30), (95,590,30,30), (125,590,30,30), (155,590,30,30), #Bottom row
                 (185,590,30,30), (215,590,30,30), (245,590,30,30), (275,590,30,30), #Bottom row
                 (305,590,30,30), (335,590,30,30), (365,590,30,30), (395,590,30,30), #Bottom row
                 (425,590,30,30), (0,50,5,240), (455,50,5,240), (0,320,5,300), #Thin border walls
                 (455,320,5,300)} #Thin border walls
    app.pellets = [(20,95), (50,95), (80,95), (110,95), (140,95), (170,95), (200,95), 
                   (260,95), (290,95), (320,95), (350,95), (380,95), (410,95), (440,95), #end of row 1
                   (20,125), (110,125), (200,125), (260,125), (350,125), (440,125), #end of row 2
                   (20,155), (50,155), (80,155), (110,155), (140,155), (170,155), (200,155),
                   (230,155), (260,155), (290,155), (320,155), (350,155), (380,155), (410,155), (440,155), #end of row 3
                   (20,185), (110,185), (170,185), (290,185), (350,185), (440,185), #end of row 4
                   (20,215), (50,215), (80,215), (110,215), (170,215), (200,215), 
                   (290,215), (260,215), (350,215), (380,215), (410,215), (440,215), (110,245), (350,245), #end of row 6
                   (110,275), (350,275), (110,305), (350,305), (110,335), (350,335), #end of row 9
                   (110,365),(350,365), (20,395), (50,395), (80,395), (110,395), #end of row 10
                   (140,395), (170,395), (200,395), (260,395), (290,395), (320,395), #row 11
                   (350,395), (380,395), (410,395), (440,395), (20,425), (110,425), (200,425), #row 12
                   (260,425), (350,425), (440,425), (20,455), (50,455), (110,455), #end of row 12
                   (140,455), (170,455), (200,455), (260,455), (290,455), 
                   (320,455), (350,455), (410,455), (440,455), (50,485), (110,485), #end of row 13
                   (170,485), (290,485), (350,485), (410,485), (20,515), (50,515), #end of row 14
                   (80,515), (110,515), (170,515), (200,515), (260,515), (290,515),
                   (350,515), (380,515), (410,515), (440,515), (20,545), (200,545), #end of row 15
                   (260,545), (440,545), (20,575), (50,575), (80,575), (110,575), 
                   (140,575), (170,575), (200,575), (230,575), (260,575), (290,575), 
                   (320,575), (350,575), (380,575), (410,575), (440,575)] #Final row of pellets



def redrawAll(app):
    for pelletX, pelletY in app.pellets:
        drawCircle(pelletX, pelletY, 5, fill='white', align='center')
    drawCircle(app.pacmanX, app.pacmanY, 11, fill='yellow')
    if app.rotation == 'right':
        drawPolygon(app.pacmanX, app.pacmanY, app.pacmanX + 11, 
                    app.pacmanY - 5, app.pacmanX + 11, 
                    app.pacmanY + 5, fill='black')
    elif app.rotation == 'left':
        drawPolygon(app.pacmanX, app.pacmanY, app.pacmanX - 11, 
                    app.pacmanY - 5, app.pacmanX - 11, 
                    app.pacmanY + 5, fill='black')
    elif app.rotation == 'up':
        drawPolygon(app.pacmanX, app.pacmanY, app.pacmanX - 5, 
                    app.pacmanY - 11, app.pacmanX + 5, 
                    app.pacmanY - 11, fill='black')
    elif app.rotation == 'down':
        drawPolygon(app.pacmanX, app.pacmanY, app.pacmanX - 5, 
                    app.pacmanY + 11, app.pacmanX + 5, 
                    app.pacmanY + 11, fill='black')
    rightEdgeofPacman = app.pacmanX + 11
    leftEdgeofPacman = app.pacmanX - 11
    if rightEdgeofPacman > app.width:
        pixelsBeyondRightEdgeOfCanvas = rightEdgeofPacman - app.width
        cx = -11 + pixelsBeyondRightEdgeOfCanvas
        drawCircle(cx, app.pacmanY, 11, fill='Yellow')
    if leftEdgeofPacman < 0:
        pixelsBeyondLeftEdgeOfCanvas = -leftEdgeofPacman
        cx = app.width + 11 - pixelsBeyondLeftEdgeOfCanvas
        drawCircle(cx, app.pacmanY, 11, fill='Yellow')
    for i in range(4):
        ghostX, ghostY = app.antagonistPositions[i]
        drawCircle(ghostX, ghostY, 11, fill=app.ghostColors[i])
    for wall in app.walls:
        left, top, width, height = wall
        drawRect(left, top, width, height, fill='blue')
    for lifeX, lifeY in app.lifeIcons:
        drawCircle(lifeX, lifeY, 10, fill='yellow')
    for icon in app.lifeIcons:
        drawPolygon(icon[0], icon[1], icon[0] + 10, 
                    icon[1] - 5, icon[0] + 10, 
                    icon[1] + 5, fill='black')
    drawLabel(f'Score: {app.score}', 350, 25, fill='white', size=20, bold=True)

def onKeyHold(app, keys):
        ocx = app.pacmanX
        ocy = app.pacmanY
        if not app.gameOver:
            if 'right' in keys and 'left' not in keys:
                app.rotation = 'right'
                app.pacmanX += 3
                if any(withinRect(app.pacmanX, app.pacmanY, *wall) for wall in app.walls):
                    app.pacmanX = ocx
                if app.pacmanX + 11 >= app.width:
                    app.pacmanX = -11
            if 'left' in keys and 'right' not in keys:
                app.rotation = 'left'
                app.pacmanX -= 3
                if any(withinRect(app.pacmanX, app.pacmanY, *wall) for wall in app.walls):
                    app.pacmanX = ocx
                if app.pacmanX - 11 <= 0:
                    app.pacmanX = app.width + 11
            if 'up' in keys and 'down' not in keys:
                app.rotation = 'up'
                app.pacmanY -= 3
                if any(withinRect(app.pacmanX, app.pacmanY, *wall) for wall in app.walls):
                    app.pacmanY = ocy
            if 'down' in keys and 'up' not in keys:
                app.rotation = 'down'
                app.pacmanY += 3
                if any(withinRect(app.pacmanX, app.pacmanY, *wall) for wall in app.walls):
                    app.pacmanY = ocy

def onKeyPress(app, key):
    if key == 'r' and app.gameOver:
        onAppStart(app)

def onStep(app):
    app.steps += 1
    if not app.gameOver and app.steps % 5 == 0:
        eatPellet(app)
        if collidesWithGhost(app):
            app.lives -= 1
            app.antagonistPositions = [(230, 275), (200, 305), (230, 305), (260, 305)]
            app.pacmanX = 230
            app.pacmanY = 455
            app.lifeIcons.pop()
            if app.lives <= 0:
                app.gameOver = True

def main():
    runApp()

main() 