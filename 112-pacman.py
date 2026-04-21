from cmu_graphics import *

def withinRect(cx, cy, left, top, width, height):
    radius = 11
    closestX = max(left, min(cx, left + width))
    closestY = max(top, min(cy, top + height))
    dx = cx - closestX
    dy = cy - closestY
    return (dx * dx + dy * dy) <= (radius * radius)

def collidesWithGhost(app):
    for ghostX, ghostY in app.antagonistPositions:
        dx = app.pacmanX - ghostX
        dy = app.pacmanY - ghostY
        if (dx * dx + dy * dy)**0.5 <= 11:
            return True
    return False

def onAppStart(app):
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



def redrawAll(app):
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
    if not app.gameOver:
        if collidesWithGhost(app):
            app.lives -= 1
            app.antagonistPositions = [(230, 275), (200, 305), (230, 305), (260, 305)]
            app.pacmanX = 230
            app.pacmanY = 455
            app.lifeIcons.pop()
            if app.lives == 0:
                app.gameOver = True

def main():
    runApp()

main() 