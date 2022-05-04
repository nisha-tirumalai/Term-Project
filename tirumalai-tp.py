from cmu_cs3_graphics import *
import os 
import math
import random 
from PIL import Image 


##########################################
# main app 
##########################################

def onAppStart(app):
    app.ticks = 0 
    app.mode = 'startMode'
    app.gridRows, app.gridCols, app.gridMargin = 30, 30, 0
    app.rows, app.cols, app.margin = 8, 8, 0
    app.initialScreen = True 
    app.startX, app.startY = -60, app.height//1.9
    app.resetX, app.resetY = app.width//3.7 + app.width//4.7, app.height + 60 
    app.infoX, app.infoY = app.width + 60, app.height//1.9 
    app.mouseX, app.mouseY = 0, 0
    app.startR, app.resetR, app.infoR = 60, 60, 60
    app.gameStart = False 
    app.currKey = ''
    i = generateRandomParagraph(app)
    app.L = createParagraph(app, i)
    app.wordNum = 0
    app.currLetterIndex = 0
    app.nitroX1, app.nitroY1 = app.width//2, 0
    app.nitroX2, app.nitroY2 = app.height//2 - 3, 0
    app.number = 1
    app.board = createBoard(app)
    app.mazeList = []
    app.colorList = []
    app.inMaze = []
    app.frontierList = []
    app.number = 1
    app.stepsPerSecond = 15
    app.directions = []
    createColorList(app)
    initialMazeList(app)
    primsAlgorithm(app)
    x = solveMaze(app)
    while(x == None):
        initialMazeList(app)
        primsAlgorithm(app)
        solveMaze(app)
    gridWidth = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows 
    app.currCell = (0, 0) 
    app.carX = app.margin + cellWidth*app.currCell[1] 
    app.carY = app.margin + cellHeight*app.currCell[0] 
    app.currDirection = ''
    app.cumulative = 0 
    app.characters = getLengthPara(app, app.L)
    app.currNumber = 1
    app.currWPM = 0 
    app.currAccuracy = 0 
    app.charactersWrong = 0 
    app.secondsPassed = 0 
    app.wordsTyped = 0 
    app.quitLeft = 347
    app.quitTop = 587
    app.quitWidth = 106
    app.quitHeight = 53
    

##########################################
# start mode  
########################################## 
def startModeOnStep(app):
    app.ticks += 1
    if(app.nitroY1 < app.height//2.68):
        app.nitroY1 += 30
    if(app.nitroY2 < app.height//2.68):
        app.nitroY2 += 30
    else:
        if (app.startX + 30 < app.width//3.7):
            app.startX += 30
        if(app.resetY - 20 > app.height//1.9):
            app.resetY -= 50
        if(app.infoX - 20 > app.width//3.7 + app.width//2.3):
            app.infoX -= 30
    
class Circle(object):
    def __init__(self, app, name, color, cx, cy, r, labelSize, borderSize):
        self.name = name 
        self.color = color 
        self.cx = cx 
        self.cy = cy 
        self.r = r 
        self.labelSize = labelSize
        self.borderSize = borderSize 

    def drawCirc(self):
        drawCircle(self.cx, self.cy, self.r, fill = 'white', border = self.color, 
        borderWidth = self.borderSize)
        drawLabel(self.name, self.cx, self.cy, fill = self.color, size = self.labelSize)
    

def isEven(app, num):
    if(num % 2 == 0):
        return True
    return False 

def isOdd(app, num):
    if(num % 2 == 1):
        return True
    return False

# in my game of chess that I coded for extra credit a while ago, 
# I used a similar logic to be able to create a checkerboard 
# https://cs3.academy.cs.cmu.edu/ide#31988 
def displayInitialScreen(app):
    color = ''
    for row in range(app.gridRows):
        for col in range(app.gridCols):
            (left, top, width, height) = getCellBounds(app, row, col)
            # if row is even and column is odd, cell is gray
            if(isEven(app,row) and isOdd(app, col)):
                color = 'gray'
            # if row is odd and column is even, cell is gray
            elif(isOdd(app, row) and isEven(app, col)):
                color = 'gray'
            # otherwise, cell is white
            else:
                color = 'white'
            drawRect(left, top, width, height, fill = color)
    drawRect(0, app.height//3, app.width, app.height//3, 
    fill = 'lightblue')
    drawLabel('''WELCOME TO NITROTYPE ELITE!''', app.nitroX1, app.nitroY1, 
    bold = True, size = 45, fill = 'darkblue' )
    drawLabel('''WELCOME TO NITROTYPE ELITE!''', app.nitroX2, app.nitroY2, 
    fill = 'dodgerBlue', size = 45, borderWidth = 10)
    startButton = Circle(app, "START", 'green', app.startX, app.startY, app.startR, 30, 3)
    resetButton = Circle(app, "RESET", 'maroon', app.resetX, app.resetY, app.resetR, 30, 3)
    infoButton = Circle(app, "INFO", 'purple', app.infoX, app.infoY ,app.infoR, 30, 3)
    startButton.drawCirc()
    resetButton.drawCirc()
    infoButton.drawCirc()

# this function, getcellBounds, was inspired by the course Notes- 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html        
def getCellBounds(app, row, col):
    gridWidth = app.width - 2*app.gridMargin
    gridHeight = app.height - 2*app.gridMargin
    cellWidth = gridWidth/app.gridCols
    cellHeight = gridHeight/app.gridRows 
    left = app.gridMargin + cellWidth*col 
    top = app.gridMargin + cellHeight*row
    return (left, top, cellWidth, cellHeight)

def startModeOnMousePress(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY 
    if(pressedStart(app, mouseX, mouseY)):
        app.ticks = 0 
        onAppStart(app)
        app.mode = 'readyMode'
    elif(pressedReset(app, mouseX, mouseY)):
        app.startX = app.width//2 - app.width//7
        app.infoX = app.width//2 + app.width//7
        f = open("scores.txt", "a")
        f.write('0\n')
        f.write('0\n')
        f.close()
        app.mode = 'resetMode'
    elif(pressedInfo(app, mouseX, mouseY)):
        app.startX = app.width//2
        app.startY = app.height - app.height//4
        app.mode = 'infoMode'

def startModeOnMouseMove(app,mouseX,mouseY):
    if(pressedStart(app, mouseX, mouseY) == True):
        app.startR = 80
    if(pressedStart(app, mouseX, mouseY) == False):
        app.startR = 60 
    if(pressedReset(app, mouseX, mouseY) == True):
        app.resetR = 80
    if(pressedReset(app, mouseX, mouseY) == False):
        app.resetR = 60 
    if(pressedInfo(app, mouseX, mouseY) == True):
        app.infoR = 80 
    if(pressedInfo(app, mouseX, mouseY) == False):
        app.infoR = 60 

def pressedReset(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.resetX, app.resetY) <= app.resetR):
        return True 
    return False

def pressedInfo(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.infoX, app.infoY) <= app.infoR):
        return True 
    return False

def pressedStart(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.startX, app.startY) <= app.startR):
        return True 
    return False

def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

# note that the idea of having different types of "modes" was 
# inspired by the course website 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

def startModeRedrawAll(app):
    displayInitialScreen(app)

##########################################
# ready mode  
##########################################
def displayReadyMode(app):
    drawRect(0,0, app.width, app.height, fill = 'lightBlue')
    if(app.gameStart == False):
        drawLabel("READY TO RACE? ", app.width//2, app.height//3, fill = 'black', size = 70)
        drawLabel("READY TO RACE? ", app.width//2 - 4, app.height//3, fill = 'red', size = 70)
        filename = "raceFlags.webp"
        image = Image.open("raceFlags.webp")
        new_raceCar = image.resize((700, 500))
        new_raceCar.save('newRaceFlag.png')
        drawImage('newRaceFlag.png', app.width/2 - 350 , app.height/2.5)
        image = Image.open("cheering.webp")
        new_image = image.resize((800, 220))
        new_image.save("newCheering.webp")
        drawImage("newCheering.webp", 0 , 0)

def readyModeRedrawAll(app):
    displayReadyMode(app)
    if(app.gameStart == False):
        if(app.ticks > 40 and app.ticks <= 80): 
            drawLabel("3", app.width//2, app.height//2, fill = 'black', size = 190, 
            border = 'white', borderWidth = 2, bold = True)
        if(app.ticks > 80 and app.ticks <= 120):
            drawLabel("2", app.width//2, app.height//2, fill = 'black', size = 190,
            border = 'white', borderWidth = 2, bold = True)
        if(app.ticks > 120 and app.ticks <= 160):
            drawLabel("1", app.width//2, app.height//2, fill = 'black', size = 190,
            border = "white", borderWidth = 2, bold = True)
def readyModeOnStep(app):
    app.ticks += 3
    if(app.ticks > 160):
        app.gameStart = True 
        app.ticks = 0 
        app.mode = 'gameMode'

##########################################
# game mode  
##########################################

class Letter (object):
    def __init__(self, app, letter, isHighlighted, isWrong):
        self.letter = letter 
        self.highlight = isHighlighted 
        self.isWrong = isWrong 
        self.color = "black"
        self.bold = False 
        if(self.highlight == True):
            self.color = "purple"
            self.bold = True 

class Box (object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.left = True
        self.right = True
        self.up = True
        self.down = True  
    
    def drawBox(self, app):
        left, top, cellWidth, cellHeight = getNewCellBounds(app, self.row, self.col, app.width, app.height//1.5)
        right = left + cellWidth
        bottom = top + cellHeight
        if self.left == True:
            drawLine(left, top, left, bottom, lineWidth = 10, fill = 'yellow')
        if self.right == True:
            drawLine(right, top, right, bottom, lineWidth = 10, fill = 'yellow')
        if self.up == True:
            drawLine(left, top, right, top, lineWidth = 10, fill = 'yellow')
        if self.down == True:
            drawLine(left, bottom, right, bottom, lineWidth = 10, fill = 'yellow')

# SOLVING THE MAZE I CREATED, using the depth-first search algorithm. 
# I read about the pseudocode of the algorithm here: 
# https://hurna.io/academy/algorithms/maze_pathfinder/dfs.html 

def createBoard(app):
    board = [None]*app.rows 
    for i in range(app.rows):
        board[i] = [None]*app.cols
    return board 

def createColorList(app):
    for row in range(app.rows):
        for col in range(app.cols):
            app.colorList.append((row, col))
    return app.colorList 
        
def onBoard(app, currLocation):
    currRow, currCol = currLocation[0], currLocation[1]
    if (currRow < 0 or currRow >= app.rows):
         return False
    elif(currCol < 0 or currCol >= app.cols):
        return False
    return True
    
def solveMaze(app):
    return solveMazeHelper(app, [0,0], 1)

def solveMazeHelper(app, currLocation, number):
    if(app.board[currLocation[0]][currLocation[1]] != None):
        return None
    else: 
        app.board[currLocation[0]][currLocation[1]] = number
        if(currLocation[0] == app.rows - 1 and currLocation[1] == app.cols - 1):
            return app.board
        else:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            keys = ['left', 'right', 'up', 'down']
            moveSet = [0, 1, 2, 3]
            while moveSet != []:
                randIndex = random.choice(moveSet)
                moveSet.remove(randIndex)
                randomDirection = keys[randIndex]
                drow, dcol = directions[randIndex]
                randomLocation = (currLocation[0] + drow, currLocation[1] + dcol)
                if(movesFreely(app, currLocation, randomLocation, randomDirection)):
                    solution = solveMazeHelper(app, randomLocation, number + 1)
                    if(solution != None):
                        app.number += 1
                        app.directions.append(randomDirection)
                        return solution 
            app.board[currLocation[0]][currLocation[1]] = None
            if(randomDirection in app.directions):
                app.directions.pop()
            number -= 1
        return None 
        
def movesFreely(app, currLocation, randomLocation, randomDirection):
    row1, col1 = currLocation 
    row2, col2 = randomLocation 
    if(onBoard(app, randomLocation) and onBoard(app, currLocation)):
            if(randomDirection == "left"):
                if(app.mazeList[row1][col1].left != True and app.mazeList[row2][col2].right != True):
                    return True 
            elif(randomDirection == 'right'):
                if(app.mazeList[row1][col1].right != True and app.mazeList[row2][col2].left != True):
                    return True 
            elif(randomDirection == 'up'):
                if(app.mazeList[row1][col1].up != True and app.mazeList[row2][col2].down != True):
                    return True
            elif(randomDirection == 'down'):
                if(app.mazeList[row1][col1].down != True and app.mazeList[row2][col2].up != True):
                    return True
    return False   

# DRAWING THE HELPER GRID 
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            fill = None
            left,top,width,height = getNewCellBounds(app, row, col, app.width,app.height//1.5)
            drawRect(left,top,width,height, fill = fill, border = 'purple', borderWidth = 1, opacity = 40)
            
def initialMazeList(app):
    for row in range(app.rows):
        rowList = []
        for col in range(app.cols):
            box = Box(row, col)
            rowList.append(box)
        app.mazeList.append(rowList)

def addNodes(app, currCell):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for drow, dcol in directions:
        newRow, newCol = drow + currCell[0] , dcol + currCell[1]
        chosenCell = (newRow, newCol)
        if(onBoard(app, chosenCell) and chosenCell not in app.frontierList):
            app.frontierList.append(chosenCell)
    return None  


##Note: My understanding of the pseudocode for prim's was guided by this external source:
# https://course.ccs.neu.edu/cs2510asp20/lecture32.html                
def primsAlgorithm(app):
    createPrimMaze(app, (0,0))
    
def createPrimMaze(app, currCell):
    # have a list of frontier nodes which is everywhere you can go from the places you have been in the past
    app.inMaze.append(currCell)
    addNodes(app, currCell)
    if len(set(app.inMaze)) >= len(app.colorList):
        return None 
    else: 
        chosenCell = random.choice(app.frontierList)
        newRow, newCol = chosenCell[0], chosenCell[1]
        app.frontierList.remove(chosenCell)
        app.inMaze.append(chosenCell)
        row, col = currCell[0], currCell[1]
        for r,c in app.inMaze:
            a = (newRow - r == 0 and abs(newCol - c) == 1) 
            b = (abs(newRow - r) == 1 and newCol - c == 0) 
            if (a or b):
                row, col = r,c 
                break 
        direction = (newRow - row , newCol - col)
        if direction == (-1, 0):
            app.mazeList[row][col].up = False
            app.mazeList[newRow][newCol].down = False 
        elif direction == (1,0):
            app.mazeList[row][col].down = False 
            app.mazeList[newRow][newCol].up = False 
        elif direction == (0,-1):
            app.mazeList[row][col].left = False
            app.mazeList[newRow][newCol].right = False
        elif direction == (0,1):
            app.mazeList[row][col].right = False
            app.mazeList[newRow][newCol].left = False
        currCell = random.choice(app.frontierList)
        app.inMaze.append(currCell)
        #app.frontierList.remove(currCell)
        createPrimMaze(app, currCell)
            

# From the course website, inspired by getCellBounds 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html  
def getNewCellBounds(app, row, col, width, height):
    gridWidth = width - 2*app.margin
    gridHeight = height - 2*app.margin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows 
    left = app.margin + cellWidth*col 
    top = app.margin + cellHeight*row
    return (left, top, cellWidth, cellHeight)

def drawPath(app):
    for row in range(len(app.board)): 
        for col in range(len(app.board[row])):
            if(app.board[row][col] != None ):
                left, top, cellWidth, cellHeight = getNewCellBounds(app, row, col, app.width, app.height//1.5)
                drawLabel(f'{app.board[row][col]}', left + cellWidth/2, top + cellHeight/2, size = 30, bold = True, 
                fill = "yellow")
                #drawRect(left, top, cellWidth, cellHeight, fill = 'yellow', opacity = 50)
               
def isLegal(app, row, col):
    if row < 0 or row >= len(app.mazeList) or col < 0 or col >= len(app.mazeList[0]):
        return False
    elif app.mazeList[row][col] in app.visited:
        return False
    return True
   
def drawMaze(app):
    for row in range(len(app.mazeList)):
        for col in range(len(app.mazeList[0])):
            box = app.mazeList[row][col]
            box.drawBox(app)

# KRUSKAL's algorithm, I read about the pseudocode here: 
# https://pythonwife.com/kruskal-and-prims-algorithm-in-python/

def gameModeOnKeyPress(app, key):
    gridWidth = app.width - 2*app.margin
    gridHeight = app.height//1.5 - 2*app.margin
    cellWidth = gridWidth/app.cols
    cellHeight = gridHeight/app.rows 
    s = app.characters/(app.number)
    sizer = cellHeight/s
    # car calculations:
    # first calculate how much of a box each the car should move on each character 
    if(app.cumulative == 0):
        app.carX = 0
        app.carY = 0
    if(len(app.directions)) > 0:
        app.currDirection = app.directions[-1]
    # if done w the last word, then end the game
    if(app.wordNum == len(app.L)):
        app.gameStart = False
    if(app.currLetterIndex == len(app.L[app.wordNum])):
            app.wordsTyped += 1
            app.currLetterIndex = 0
            app.wordNum += 1
    # if u are on the last letter of the word, make ur letter back to 1 and index to the next word
    if(app.gameStart == True):
        if(app.wordNum == len(app.L) -1  and app.currLetterIndex == len(app.L[app.wordNum]) - 1):
            app.gameStart = False 
            app.startR, app.resetR, app.infoR = 60, 60, 60
            app.startX = 250
            app.resetX = 400 
            app.startY = app.height//1.6
            app.resetY = app.height//1.6
            app.infoY = app.height//1.6
            app.infoX = 550
            app.currAccuracy = int( (((app.characters - app.charactersWrong) /  app.characters)*100) )
            app.currWPM = int ((app.wordsTyped/2) / (app.secondsPassed)*60 ) 
            app.mode = "statMode"
        app.currKey = app.L[app.wordNum][app.currLetterIndex].letter
        if(key == app.currKey or key == 'space' and (app.currKey == ' ' or app.currKey == '_')):
            if(app.L[app.wordNum][app.currLetterIndex].letter == '_'):
                app.L[app.wordNum][app.currLetterIndex].letter = ' '
            app.L[app.wordNum][app.currLetterIndex].color = 'darkGreen'
            app.L[app.wordNum][app.currLetterIndex].bold = False
            app.currLetterIndex += 1 
            app.cumulative += 1 
            if(app.cumulative == 1):
                app.carX = (cellWidth/2)*(app.currCell[1] + 1) - 25
                app.carY = (cellHeight/2)*(app.currCell[0] + 1) - 25
            if(app.cumulative > math.floor(sizer) and app.cumulative != 1):
                app.cumulative = 1
                if(len(app.directions)) > 0:
                    app.directions.pop()
                for row in range(len(app.board)):
                    for col in range(len(app.board[0])):
                        if app.board[row][col] == app.currNumber:
                            app.currCell = (row, col)
            if(app.currDirection == "left"):
                app.carX -= (1/sizer)*cellWidth
            elif(app.currDirection == "right"):
                app.carX += (1/sizer)*cellWidth
            elif(app.currDirection == "down"):
                app.carY += (1/sizer)*cellHeight
            elif(app.currDirection == "up"):
                app.carY -= (1/sizer)*cellHeight
        elif(key != app.currKey):
            app.charactersWrong += 1
            if(app.currKey == ' '):
                app.L[app.wordNum][app.currLetterIndex].letter = '_'
            app.L[app.wordNum][app.currLetterIndex].bold = True 
            app.L[app.wordNum][app.currLetterIndex].color = 'red'
        # left = cellWidth*col 
        # top = cellHeight*row
def getLengthPara(app, L):
    characters = 0 
    for row in range(len(app.L)): 
        for col in range(len(app.L[row])):
            characters += 1
    return characters 

def gameModeOnStep(app):
    app.ticks += 1 
    if(app.ticks % 15 == 0):
        app.secondsPassed += 1 

def generateRandomParagraph(app):
    L = []
    with open("1984.txt",'r') as file:
        for line in file:
            data = line.split('.')
            for i in data:
                if(len(i) >= 160 and len(i) < 220):
                    L += [i]
    with open("catchingFire.txt",'r') as file1:
        for line1 in file1:
            data1 = line1.split('.')
            for j in data1:
                if(len(j) >= 160 and len(j) < 220):
                    L += [j]
    num = random.randint(0, len(L) - 1)
    if(L[num][0] == ' '):
        return L[num][1:]
    else: 
        return L[num]

def createParagraph(app,para):  
    para = para + ' '
    currWord = []
    output = []
    for c in range(len(para)):
        if(para[c] == ' '):
            output.append(currWord)
            output.append([Letter(app, " ", False, False)])
            currWord = []
            continue
        elif(c == 0):
            letter = Letter(app, para[c], True, False)
        elif(c > 0): 
            letter = Letter(app, para[c], False, False)
        currWord.append(letter)
    return output



def gameModeRedrawAll(app):
    if(app.gameStart == True):
        drawRect(0,0, app.width, app.height, fill = rgb(50,50,50))
        #drawGrid(app)
        drawPath(app)
        drawMaze(app)
        drawRect(0,0, app.width, app.height//1.5, fill = None, border = "black", borderWidth = 10 )
        drawRect(0, app.height//1.5, app.width, app.height, fill = "black")
        drawRect(15, app.height//1.45, app.width - 30, app.height//3.5, fill = "white")
        x = app.width//15
        y = app.height - app.height//3.8
        word = ''
        for j in range(len(app.L)):
            word = app.L[j] 
            if(x + len(word)*20 > app.width - app.width//15):
                y += 30
                x = app.width//15
            for i in range(len(word)):
                letter = word[i]
                x += 20
                drawLabel(letter.letter,x ,y,fill= letter.color, size = 25, align = 'bottom', bold = letter.bold) 
        image = Image.open('car.png')
        new_image = image.resize((50, 50))
        new_image.save('newCar.png')
        drawImage('newCar.png', app.carX, app.carY)

##########################################
# reset mode  
##########################################

def displayResetMode(app):
    for row in range(app.gridRows):
        for col in range(app.gridCols):
            (left, top, width, height) = getCellBounds(app, row, col)
            # if row is even and column is odd, cell is gray
            if(isEven(app,row) and isOdd(app, col)):
                color = 'gray'
            # if row is odd and column is even, cell is gray
            elif(isOdd(app, row) and isEven(app, col)):
                color = 'gray'
            # otherwise, cell is white
            else:
                color = 'white'
            drawRect(left, top, width, height, fill = color)
    drawRect(app.width//16, app.height//13, app.width - app.width//8, app.height//1.25)
    drawLabel("Scores have",app.width//2, app.height//6, fill = "maroon" , size = 55, bold = True, 
    border = 'white', borderWidth = 1)
    drawLabel("been reset!",app.width//2, app.height//4.3, fill = "maroon" , size = 55, bold = True, 
    border = 'white', borderWidth = 1)
    startButton = Circle(app, "START", 'green', app.startX, app.startY, app.startR, 30, 3)
    infoButton = Circle(app, "INFO", 'purple', app.infoX, app.infoY ,app.infoR, 30, 3)
    startButton.drawCirc()
    infoButton.drawCirc()

def resetModeOnMousePress(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY 
    if(pressedStart(app, mouseX, mouseY)):
        app.mode = 'readyMode'
        app.ticks = 0 
    elif(pressedInfo(app, mouseX, mouseY)):
        app.startX = app.width//2
        app.startY = app.height - app.height//4
        app.mode = 'infoMode'

def resetModeOnMouseMove(app,mouseX,mouseY):
    if(pressedStart(app, mouseX, mouseY) == True):
        app.startR = 80
    if(pressedStart(app, mouseX, mouseY) == False):
        app.startR = 60 
    if(pressedInfo(app, mouseX, mouseY) == True):
        app.infoR = 80 
    if(pressedInfo(app, mouseX, mouseY) == False):
        app.infoR = 60 

def pressedInfo(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.infoX, app.infoY) <= app.infoR):
        return True 
    return False

def pressedStart(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.startX, app.startY) <= app.startR):
        return True 
    return False

def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    

def resetModeRedrawAll(app):
    displayResetMode(app)

##########################################
# info mode  
##########################################

def displayInfoMode(app):
    for row in range(app.gridRows):
        for col in range(app.gridCols):
            (left, top, width, height) = getCellBounds(app, row, col)
            # if row is even and column is odd, cell is gray
            if(isEven(app,row) and isOdd(app, col)):
                color = 'gray'
            # if row is odd and column is even, cell is gray
            elif(isOdd(app, row) and isEven(app, col)):
                color = 'gray'
            # otherwise, cell is white
            else:
                color = 'white'
            drawRect(left, top, width, height, fill = color)
    drawRect(app.width//16, app.height//13, app.width - app.width//8, app.height//1.25)
    drawLabel("INFO: how to play!",app.width//2, app.height//8, fill = "maroon" , size = 60, bold = True, 
    border = 'white', borderWidth = 1)
    image = Image.open("info.png")
    #new_image = image.resize((800, 220))
    #new_image.save("newCheering.webp")
    drawImage("info.png", app.width//11 , app.height//6, width = 600, height = 400)
    startButton = Circle(app, "START", 'green', app.width//2, app.height - app.height//4, app.startR, 30, 3)
    startButton.drawCirc()

def infoModeOnMousePress(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY 
    if(pressedStart(app, mouseX, mouseY)):
        app.ticks = 0
        onAppStart(app)
        app.mode = 'readyMode' 

def infoModeOnMouseMove(app,mouseX,mouseY):
    if(pressedStart(app, mouseX, mouseY) == True):
        app.startR = 80
    if(pressedStart(app, mouseX, mouseY) == False):
        app.startR = 60 


def pressedStart(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.startX, app.startY) <= app.startR):
        return True 
    return False

def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

def infoModeRedrawAll(app):
    displayInfoMode(app)

##########################################
# stat mode  
##########################################

def displayStatMode(app):
    f = open("scores.txt", "r")
    lines = f.readlines()
    f.close() 
    f1 = open("scores.txt", "a")
    if (app.currAccuracy > int(lines[-2]) and app.currWPM > int(lines[-1])):
        x = str(app.currAccuracy)
        y = str(app.currWPM)
        f1.write(x + '\n')
        f1.write(y + '\n')
    elif(app.currAccuracy > int(lines[-2])):
        x = str(app.currAccuracy)
        y = lines[-1]
        f1.write(x + '\n')
        f1.write(y)
    elif(app.currWPM > int(lines[-1])):
        x = lines[-2]
        y = str(app.currWPM)
        f1.write(x)
        f1.write(y + '\n')
    f1.close()
    f = open("scores.txt", "r")
    lines = f.readlines()
    bestWPM = lines[-1]
    bestA = lines[-2] 
    f.close()
    for row in range(app.gridRows):
        for col in range(app.gridCols):
            (left, top, width, height) = getCellBounds(app, row, col)
            # if row is even and column is odd, cell is gray
            if(isEven(app,row) and isOdd(app, col)):
                color = 'gray'
            # if row is odd and column is even, cell is gray
            elif(isOdd(app, row) and isEven(app, col)):
                color = 'gray'
            # otherwise, cell is white
            else:
                color = 'white'
            drawRect(left, top, width, height, fill = color)
    drawRect(app.width//16, app.height//13, app.width - app.width//8, app.height//1.25)
    drawLabel("FINISHED!",app.width//2, app.height//10, fill = "yellow" , size = 80, bold = True, 
    border = 'maroon', borderWidth = 3)
    image = Image.open("banner.png")
    #new_image = image.resize((800, 220))
    #new_image.save("newCheering.webp")
    drawImage("banner.png", 107 , 133, width = app.width - app.width//3.58, height = app.height//1.5)
    #drawLabel(f'Accuracy for this round: {app.currAccuracy}', 100, 100, size = 80)
    startButton = Circle(app, "START", 'green', app.startX, app.startY, app.startR, 30, 3)
    resetButton = Circle(app, "RESET", 'maroon', app.resetX, app.resetY, app.resetR, 30, 3)
    infoButton = Circle(app, "INFO", 'purple', app.infoX, app.infoY ,app.infoR, 30, 3)
    startButton.drawCirc()
    resetButton.drawCirc()
    infoButton.drawCirc()
    quitButton = Quit(app, "QUIT", app.quitLeft, app.quitTop, app.quitWidth, app.quitHeight)
    quitButton.drawRect()
    drawLabel("QUIT", 400, 613, fill = "white", bold = True, size = 20)
    image = Image.open("trophy.png")
    new_image = image.resize((55, 55))
    new_image.save("newTrophy.png")
    drawImage("newTrophy.png", app.width//4.5, app.height//2.5)
    drawLabel(f'Accuracy for this round: {app.currAccuracy}%', app.width//2.33, app.height//3.5, fill = "white", size = 25, bold = True)
    drawLabel(f'WPM for this round: {app.currWPM}', app.width//2.56, app.height//3.0, fill = "white", size = 25, bold = True)
    drawLabel(f'Best accuracy: {bestA[:-1]}%', app.width//2.1, app.height//2.4, fill = "yellow", size = 25, bold = True)
    drawLabel(f'Best WPM: {bestWPM[:-1]}', app.width//2.3, app.height//2.2, fill = "yellow", size = 25, bold = True)

def statModeOnMousePress(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY 
    if(pressedStart(app, mouseX, mouseY)):
        app.ticks = 0 
        onAppStart(app)
        app.mode = 'readyMode' 
    elif(pressedReset(app, mouseX, mouseY)):
        app.startX = app.width//2 - app.width//7
        app.infoX = app.width//2 + app.width//7
        f = open("scores.txt", "a")
        f.write('0\n')
        f.write('0\n')
        f.close()
        app.mode = 'resetMode'
    elif(pressedInfo(app, mouseX, mouseY)):
        app.startX = app.width//2
        app.startY = app.height - app.height//4
        app.mode = 'infoMode'
    elif(pressedQuit(app, mouseX, mouseY)):
        app.mode = 'gameOver'

def statModeOnMouseMove(app, mouseX,mouseY):
    if(pressedStart(app, mouseX, mouseY) == True):
        app.startR = 80
    if(pressedStart(app, mouseX, mouseY) == False):
        app.startR = 60 
    if(pressedReset(app, mouseX, mouseY) == True):
        app.resetR = 80
    if(pressedReset(app, mouseX, mouseY) == False):
        app.resetR = 60 
    if(pressedInfo(app, mouseX, mouseY) == True):
        app.infoR = 80 
    if(pressedInfo(app, mouseX, mouseY) == False):
        app.infoR = 60 
    if(pressedQuit(app, mouseX, mouseY) == True):
        app.quitLeft = 320 
        app.quitTop = 560 
        app.quitWidth = 160
        app.quitHeight = 107
    if(pressedQuit(app, mouseX, mouseY) == False):
        app.quitLeft = 347
        app.quitTop = 587
        app.quitWidth = 106
        app.quitHeight = 53

def pressedReset(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.resetX, app.resetY) <= app.resetR):
        return True 
    return False

def pressedInfo(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.infoX, app.infoY) <= app.infoR):
        return True 
    return False

def pressedStart(app, mouseX, mouseY):
    if(distance (mouseX, mouseY, app.startX, app.startY) <= app.startR):
        return True 
    return False

def pressedQuit(app, mouseX, mouseY):
    if(mouseX > app.quitLeft and mouseY > app.quitTop):
        if(mouseX < (app.quitLeft + app.quitWidth) and mouseY < (app.quitTop + app.quitHeight) ):
            return True 
    return False 

def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

class Quit(object):
    def __init__(self, app, title, left, top, width, height):
        self.title = title 
        self.left = left 
        self.top = top 
        self.width = width 
        self.height = height 
    
    def drawRect(self):
        drawRect(self.left, self.top, self.width, self.height, fill = "gray")

def statModeRedrawAll(app):
    displayStatMode(app)


##########################################
# game over mode  
##########################################

def displayGameOver(app):
    for row in range(app.gridRows):
        for col in range(app.gridCols):
            (left, top, width, height) = getCellBounds(app, row, col)
            # if row is even and column is odd, cell is gray
            if(isEven(app,row) and isOdd(app, col)):
                color = 'gray'
            # if row is odd and column is even, cell is gray
            elif(isOdd(app, row) and isEven(app, col)):
                color = 'gray'
            # otherwise, cell is white
            else:
                color = 'white'
            drawRect(left, top, width, height, fill = color)
    drawRect(app.width//16, app.height//13, app.width - app.width//8, app.height//1.25)
    drawLabel("GAME OVER!",app.width//2, app.height//3, fill = "maroon" , size = 60, bold = True, 
    border = 'white', borderWidth = 1)
    pass 


def gameOverRedrawAll(app):
    displayGameOver(app)


def main():
    runApp(width=800, height=800)
main()
