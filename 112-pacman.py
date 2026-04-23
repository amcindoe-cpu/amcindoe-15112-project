from cmu_graphics import *
from collections import deque

points = {(20,95), (50,95), (80,95), (110,95), (140,95), (170,95), (200,95), 
                   (260,95), (290,95), (320,95), (350,95), (380,95), (410,95), (440,95), 
                   (20,125), (110,125), (200,125), (260,125), (350,125), (440,125), 
                   (20,155), (50,155), (80,155), (110,155), (140,155), (170,155), (200,155),
                   (230,155), (260,155), (290,155), (320,155), (350,155), (380,155), (410,155), (440,155), 
                   (20,185), (110,185), (170,185), (290,185), (350,185), (440,185), 
                   (20,215), (50,215), (80,215), (110,215), (170,215), (200,215), 
                   (290,215), (260,215), (350,215), (380,215), (410,215), (440,215), (110,245), (350,245), 
                   (110,275), (350,275), (110,305), (350,305), (110,335), (350,335), 
                   (110,365),(350,365), (20,395), (50,395), (80,395), (110,395), 
                   (140,395), (170,395), (200,395), (260,395), (290,395), (320,395), 
                   (350,395), (380,395), (410,395), (440,395), (20,425), (110,425), (200,425), 
                   (260,425), (350,425), (440,425), (20,455), (50,455), (110,455), 
                   (140,455), (170,455), (200,455), (260,455), (290,455), 
                   (320,455), (350,455), (410,455), (440,455), (50,485), (110,485), 
                   (170,485), (290,485), (350,485), (410,485), (20,515), (50,515), 
                   (80,515), (110,515), (170,515), (200,515), (260,515), (290,515),
                   (350,515), (380,515), (410,515), (440,515), (20,545), (200,545), 
                   (260,545), (440,545), (20,575), (50,575), (80,575), (110,575), 
                   (140,575), (170,575), (200,575), (230,575), (260,575), (290,575), 
                   (320,575), (350,575), (380,575), (410,575), (440,575), (200,245), 
                   (260,245), (140,305), (170,275), (200,275), (230,275), (260,275),
                   (290,275), (110,305), (170,305), (290,305), (320,305), (170,335),
                   (200,335), (230,335), (230,305),(260,335), (290,335), (110,365), 
                   (170,365), (290,365), (200,305), (260,305)} #Set up the points where the ghosts or pacman can go

directions = [(30,0), (-30,0), (0,30), (0,-30)] #Directions between two points

graph = {}

for (x,y) in points:
    neighbors = []
    for (dx, dy) in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in points:
            neighbors.append(neighbor)
    graph[(x,y)] = neighbors #Constructing the graph of neighbors for the graph theory

def bfs(start, target, graph): #This is the ghost pathing algorithm.
    queue = deque([start])
    cameFrom = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in graph[current]:
            if neighbor not in cameFrom:
                queue.append(neighbor)
                cameFrom[neighbor] = current
    path = []
    curr = target
    while curr:
        path.append(curr)
        curr = cameFrom.get(curr)
    path.reverse()
    return path

class Ghost: #Initializing the ghost as a vector.
    def __init__(self, startPosition, color, type):
        self.position = startPosition
        self.color = color
        self.type = type
        self.target = startPosition
        self.path = []
        self.mode = 'chase' #For later!
    def update(self, pacmanPosition, pacmanDirection, graph):
        self.chooseTarget(pacmanPosition, pacmanDirection)
        self.path = bfs(self.position, self.target, graph)
        if len(self.path) > 1:
            self.position = self.path[1]
    def chooseTarget(self, pacmanPosition, pacmanDirection):
        if self.type == 'r':
            self.target = pacmanPosition
        elif self.type == 'p':
            dx,dy = pacmanDirection
            step = 30
            target = (pacmanPosition[0] + dx*step*4, pacmanPosition[1] + dy*step*4)
            self.target = getClosestNode(target)
        elif self.type == 'i':
            px,py = pacmanPosition
            bx, by = Blinky.position
            step = 30
            targetX = px + (px - bx)
            targetY = py + (py - by)
            self.target = getClosestNode((targetX, targetY))
        elif self.type == 'c':
            dist = abs(self.position[0] - pacmanPosition[0]) + abs(self.position[1] - pacmanPosition[1])
            if dist > 150:
                self.target = pacmanPosition
            else:
                self.target = (20,95) 

Blinky = Ghost((230, 275), 'red', 'r')
Pinky = Ghost((230, 305), 'pink', 'p')
Inky = Ghost((200, 305), 'cyan', 'i')
Clyde = Ghost((260, 305), 'orange', 'c')

def getClosestNode(pos):
    x, y = pos
    return min(points, key=lambda p: abs(p[0]-x) + abs(p[1]-y)) #locate pacman

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
    for ghost in app.ghosts:
        ghostX, ghostY = ghost.position
        dx = app.pacmanX - ghostX
        dy = app.pacmanY - ghostY
        if (dx * dx + dy * dy)**0.5 <= 11 and app.invulnurable == False:
            return True
    return False

def getPacmanDirection(app):
    if app.rotation == 'right':
        return (1, 0)
    elif app.rotation == 'left':
        return (-1, 0)
    elif app.rotation == 'up':
        return (0, -1)
    elif app.rotation == 'down':
        return (0, 1)
    return (0, 0) #failsafe

def onAppStart(app):
    app.steps = 0
    app.invulnurable = False
    app.background = 'black'
    app.paused = False
    app.height = 650
    app.width = 460
    app.lives = 3
    app.score = 0
    app.rotation = 'right'
    app.gameOver = False
    app.pacmanX = 230
    app.pacmanY = 455
    app.ghosts = [Blinky, Pinky, Inky, Clyde]
    app.lifeIcons = [(15, 635), (45, 635), (75, 635)]
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
                 (455,320,5,300), (185,290,2,30), (187,318,90,2), (275,290,2,30),(185,288,30,2), (245,288,32,2)} #Thin walls around ghost pen
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
    for ghost in app.ghosts:
        cx, cy = ghost.position
        drawCircle(cx, cy, 11, fill=ghost.color)
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
        if not app.gameOver and not app.paused:
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
    if key == 'i':
        app.invulnurable = not app.invulnurable
    if key == 'p':
        app.paused = not app.paused

def onStep(app):
    app.steps += 1
    if not app.gameOver and app.steps % 5 == 0 and not app.paused:
        eatPellet(app)
        if collidesWithGhost(app):
            app.lives -= 1
            if app.lives > 0:
                Blinky.position = (230, 275)
                Pinky.position = (230, 305)
                Inky.position = (200, 305)
                Clyde.position = (260, 305)
                app.pacmanX = 230
                app.pacmanY = 455
            app.lifeIcons.pop()
            if app.lives <= 0:
                app.gameOver = True
    if not app.gameOver and app.steps % 15 == 0 and not app.paused:
        for ghost in app.ghosts:
            pacmanPos = getClosestNode((app.pacmanX, app.pacmanY))
            pacmanDirection = getPacmanDirection(app)
            ghost.update(pacmanPos, pacmanDirection, graph)

def main():
    runApp()

main() 