from cmu_graphics import *
from collections import deque

'''
This is an implementation of pac-man's endless mode. The key feature of this
project is the ghost AI, which tracks pacman's position in real time to hunt it down.
The ghost AI uses a grid-based algorithm but has the illusion of smooth movement.
Each ghost AI has a unique behavior which is as follows:

-Blinky (red) charges straight at pacman's current location
-Pinky (pink) guesses where you are going and tries to cut you off
-Inky (cyan) tries to box you in by moving between Blinky and Pinky
-Clyde (orange) does his own thing. Chases you when far, runs away when close.

The grading shortcuts are as follows:
-Press 'i' to toggle invulnerability, for testing the ghost AI
-Press 'p' to pause the game, for testing the ghost AI
-Press 'l' reset the pellets. This is done automatically when full cleared, but
you may not wish to wait that long
-Press 'r' upon losing all your lives to restart the game
'''

#Hardcoding the points where the ghosts can move, for the ghost pathfinding algorithm.
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

#These are the distances between any two adjacent points, for ghost pathing
directions = [(30,0), (-30,0), (0,30), (0,-30)] 

#Starting an empty dictionary to store the graph
graph = {}

#Constructing the graph of neighbors for the graph theory
for (x,y) in points:
    neighbors = []
    for (dx, dy) in directions:
        neighbor = (x + dx, y + dy)
        if neighbor in points:
            neighbors.append(neighbor)
    graph[(x,y)] = neighbors 


#Prevent clipping through the ghost box by removing the edges that would allow it.
graph[(230,275)] = [(200,275), (260,275)]
graph[(200,275)] = [(200,245), (170,275), (230,275)]
graph[(230,305)] = [(230,275)]
graph[(200,305)] = [(230,305)]
graph[(260,305)] = [(230,305)]
graph[(170,305)] = [(140,305), (170,275), (170,335)]
graph[(290,305)] = [(320,305), (290,335), (290,275)]
graph[(200,335)] = [(170,335), (230,335)]
graph[(230,335)] = [(200,335), (260,335)]
graph[(260,335)] = [(230,335), (290,335)]

#This is the ghost pathing algorithm. I had some assistance from chatGPT to debug and get this working.
def bfs(start, target, graph): 
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


#Constructing our ghost class, for easy modification.
class Ghost:
    def __init__(self, startPosition, color, type):
        #standard ghost features such as start position
        self.position = startPosition
        self.pixelX, self.pixelY = startPosition
        self.color = color
        self.type = type
        #Pathfinding variables
        self.target = startPosition
        self.nextNode = None
        self.prevPosition = None
        self.path = []
        self.speed = 2
        #Eye direction
        self.eyeDirX = 0
        self.eyeDirY = 0
    #Update function, which will be called every few steps to construct a path to hunt pacman.
    def update(self, pacmanPosition, pacmanDirection, graph):
        #Check to see if you are at the next node in the sequence
        #See the helper function isAtNode() below as well.
        if self.nextNode is None or self.isAtNode():
            self.position = (rounded(self.pixelX), rounded(self.pixelY))
            #Update target accordingly, and then plot a path to it
            self.chooseTarget(pacmanPosition, pacmanDirection)
            path = bfs(self.position, self.target, graph)
            #Plot the course to the immediate next target
            if len(path) > 1:
                nextStep = path[1]
                self.prevPosition = self.position
                self.nextNode = nextStep
        #This code chunk is used to smooth the ghost's pathing, taking it off the grid based system
        if self.nextNode != None:
            nx, ny = self.nextNode
            dx = nx - self.pixelX
            dy = ny - self.pixelY
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                self.eyeDirX = dx / dist
                self.eyeDirY = dy / dist
            if dist <= self.speed:
                self.pixelX, self.pixelY = self.nextNode
            else:
                self.pixelX += self.speed * dx / dist
                self.pixelY += self.speed * dy / dist
    #Check to see if the ghost has reached the next node
    def isAtNode(self):
        return abs(self.pixelX - self.nextNode[0]) < 1 and abs(self.pixelY - self.nextNode[1]) < 1

    #This function determines how the ghost will chase pacman, and pick a path target accordingly.
    def chooseTarget(self, pacmanPosition, pacmanDirection):
        #Charge straight at pacman
        if self.type == 'r':
            self.target = pacmanPosition
        #Target where pacman is likely going
        elif self.type == 'p':
            dx,dy = pacmanDirection
            step = 30
            target = (pacmanPosition[0] + dx*step*4, pacmanPosition[1] + dy*step*4)
            self.target = getClosestNode(target)
        #Box in pacman by placing itself between two other ghosts
        elif self.type == 'i':
            px,py = pacmanPosition
            bx, by = Blinky.position
            step = 30
            targetX = px + (px - bx)
            targetY = py + (py - by)
            self.target = getClosestNode((targetX, targetY))
        #Do their own thing. Chase when far, run when close.
        elif self.type == 'c':
            dist = abs(self.position[0] - pacmanPosition[0]) + abs(self.position[1] - pacmanPosition[1])
            if dist > 150:
                self.target = pacmanPosition
            else:
                self.target = (20,95) 

#Loading our four ghosts.
Blinky = Ghost((230, 275), 'red', 'r')
Pinky = Ghost((230, 305), 'pink', 'p')
Inky = Ghost((200, 305), 'cyan', 'i')
Clyde = Ghost((260, 305), 'orange', 'c')

#Locate pacman for the purposes of pathfinding.
def getClosestNode(pos):
    x, y = pos
    return min(points, key=lambda p: abs(p[0]-x) + abs(p[1]-y)) 

#This code chunk determines whether pacman will hit a wall.
def withinRect(cx, cy, left, top, width, height):
    radius = 11
    closestX = max(left, min(cx, left + width))
    closestY = max(top, min(cy, top + height))
    dx = cx - closestX
    dy = cy - closestY
    return (dx * dx + dy * dy) <= (radius * radius)

def eatPellet(app):
    #Eat a pellet, add it to score
    for i in range(len(app.pellets)):
        pelletX, pelletY = app.pellets[i]
        dx = app.pacmanX - pelletX
        dy = app.pacmanY - pelletY
        #Remove a pellet when eaten, and add to score.
        if (dx * dx + dy * dy)**0.5 <= 11:
            app.score += 10
            app.pellets.pop(i)
            break
    #Respawn pellets if all are eaten, for an endless mode.
    if len(app.pellets) == 0:
        app.pellets =[(20,95), (50,95), (80,95), (110,95), (140,95), (170,95), (200,95), 
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

#Ghost collision code, sees if pacman is "too close" to a ghost.
def collidesWithGhost(app):
    for ghost in app.ghosts:
        ghostX, ghostY = ghost.position
        dx = app.pacmanX - ghostX
        dy = app.pacmanY - ghostY
        if (dx * dx + dy * dy)**0.5 <= 11 and app.invulnurable == False:
            return True
    return False

#This function is used for both ghost pathfinding and for drawing the mouth.
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

#Initialize the various starting variables. Names have been carefully chosen
#so it is immediately apparent what each one is.
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
    #Walls are hardcoded in a set to reduce computation time.
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
    #Pellet locations are initially hardcoded, as they were previously written for ghost pathfinding as well.
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
    #draw the pellets.
    for pelletX, pelletY in app.pellets:
        drawCircle(pelletX, pelletY, 5, fill='white', align='center')
    #draw pacman
    drawCircle(app.pacmanX, app.pacmanY, 11, fill='yellow')
    #draw the mouth, uses a polygon to give the illusion of the open mouth.
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
    #Code to allow the left-right off grid traversal.
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
    #Draws the ghosts
    for ghost in app.ghosts:
        cx, cy = ghost.pixelX, ghost.pixelY
        drawCircle(cx, cy - 4, 11, fill=ghost.color)
        drawRect(cx - 11, cy - 4, 22, 11, fill=ghost.color)
        drawCircle(cx - 7, cy + 7, 4, fill=ghost.color)
        drawCircle(cx + 7, cy + 7, 4, fill=ghost.color)
        drawCircle(cx, cy + 7, 4, fill=ghost.color)
        drawCircle(cx - 4, cy - 2, 3, fill='white')
        drawCircle(cx + 4, cy - 2, 3, fill='white')
        drawCircle(cx - 4 + ghost.eyeDirX*2, cy - 2 + ghost.eyeDirY*2, 1.5, fill='blue')
        drawCircle(cx + 4 + ghost.eyeDirX*2, cy - 2 + ghost.eyeDirY*2, 1.5, fill='blue')
    #Draw the walls
    for wall in app.walls:
        left, top, width, height = wall
        drawRect(left, top, width, height, fill='blue')
    #Draw the life icons, along with their "mouths"
    for lifeX, lifeY in app.lifeIcons:
        drawCircle(lifeX, lifeY, 10, fill='yellow')
    for icon in app.lifeIcons:
        drawPolygon(icon[0], icon[1], icon[0] + 10, 
                    icon[1] - 5, icon[0] + 10, 
                    icon[1] + 5, fill='black')
    drawLabel(f'Score: {app.score}', 350, 25, fill='white', size=20, bold=True)

def onKeyHold(app, keys):
        #store original pacman-location
        ocx = app.pacmanX
        ocy = app.pacmanY
        #Check if a move is legal, and rotate pacman according to the user input.
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
    #Restart and grading shortcuts.
    if key == 'r' and app.gameOver:
        onAppStart(app)
    if key == 'i':
        app.invulnurable = not app.invulnurable
    if key == 'p':
        app.paused = not app.paused
    if key == 'l':
        app.pellets = []

def onStep(app):
    app.steps += 1
    if not app.gameOver and app.steps % 5 == 0 and not app.paused:
        eatPellet(app)
        #Check to see if pacman should die, and reset the ghosts as needed.
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
    #Ghost pathfinding code. This is called constantly to update their positions.
    if not app.gameOver and not app.paused:
        for ghost in app.ghosts:
            pacmanPos = getClosestNode((app.pacmanX, app.pacmanY))
            pacmanDirection = getPacmanDirection(app)
            ghost.update(pacmanPos, pacmanDirection, graph)

def main():
    runApp()

main() 