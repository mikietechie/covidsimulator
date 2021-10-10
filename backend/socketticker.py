import socketio, time, datetime, random, math, csv
from graphics import *


class Cell:
    def __init__(self, x, y, infected, mask, timer):
        self.x = x
        self.y = y
        self.infected = infected
        self.mask = mask
        self.timer = timer
    
    @property
    def jso(self):
        return {
            "x": self.x //8,
            "y": self.y //8,
            "infected": bool(self.infected),
            "mask": bool(self.mask),
            "timer": self.timer
        }

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    ###############################################
    #AVERAGES:
    #Trials: 25
    #0% compliance: 56 epochs    
    #MIN: 35 MAX: 71 

    #50% compliance: 90 epochs
    #MIN: 60 MAX: 123

    #75% compliance: 149 epochs
    #MIN: 98 MAX: 233

    #90% compliance: 221 epochs  
    #MIN: 152 MAX: 299

    #100% compliance: 354 epochs 
    #MIN: 234 MAX: 484

    #Set up the screen itself
    #IMPORTANT------------ screen WIDTH is the X coordinate, while screen HEIGHT is the Y coordinate
    #define variables and lists
    running = True
    #Size of each section of the grid
    boxSize = 8 #original size 12 store size 8
    #epochs
    epoch = 5
    list4 = []
    #the % of people wearing masks
    maskCompliance = 50
    #for recording long chunks of data
    dataset = []
    #average amount of time it takes to infect the whole screen:
    averageEpoch = 0
    #The rate of infection:
    infectionRate = 19 #its actually 19.2%
    #The rate of infection if the person WITHOUT covid has a mask on:
    recieverMask = 6 #its actually 6.144%
    #The rate of infection if the person WITH covid has a mask on:
    spreaderMask = 6
    #The rate of infection if BOTH people have a mask on
    bothMask = 2 #its actually 1.966%
    #vaccination rate
    vaccinationRate = 50
    numberOfCells = int(146 // (7/2)) #original number 250 bar number 146 store number 33
    screenWidth = int(564 // (7/2)) #original size 960 bar size 564 store size 976
    screenHeight = int(564 // (7/2)) #original size 600 bar size 564 store size 976
    density = ((screenWidth*screenHeight)/(boxSize*boxSize))/numberOfCells #orignial design is 16, bar is 1.6 and grocery store is 41.7
    #Size of the side bar
    sideBarSize = 350
    #border size is in number of cubes apart.
    borderSize = 0
    randomVariable = 0
    randomVariable1 = 0
    trialsList = []

    while running == True:
        print("Entered first while true")
        randomVariable1 = 1
        #All cells that are actively drawn
        activeCells = []
        #Define list for drawable rectangles
        rectList = []
        printStatement = 0
        #Setup random amount of squares
        for i in range(0, numberOfCells):
            x = random.randint((borderSize*boxSize), screenWidth-(borderSize*boxSize))
            y = random.randint((borderSize*boxSize), screenHeight-(borderSize*boxSize))
            x = x // boxSize
            y = y // boxSize
            # isInfected = random.randint(1, 3)
            infected = 0
            if i == 0:
                infected = 1
            mask = random.randint(1, 100)
            if mask > maskCompliance:
                mask = 0
                cell1 = Cell(x, y, infected, mask, 0)
            elif mask <= maskCompliance:
                mask = 1
                cell1 = Cell(x, y, infected, mask, 0)
            if i == 0:
                activeCells.append(Cell(screenWidth//(boxSize*2),screenHeight//(boxSize*2),infected,mask, 0))
            else:
                activeCells.append(cell1)

        #Shows the cells to the user
        for cell1 in activeCells:
            #Use the indicies and draws out the positions of the rectangles
            r = Rectangle(Point(cell1.x*boxSize, cell1.y*boxSize), Point(cell1.x*boxSize + boxSize, cell1.y*boxSize + boxSize))
            if cell1.infected == 1:
                r.setFill("red")
            elif cell1.infected == 0:
                r.setFill("black")
            rectList.append(r)

        while True:
            # for i in range(len(trialsList))
            #number infected vs not infected
            numInfected = 0
            numNotInfected = 0
            #number of people off screen
            offScreen = 0
            #Define the next list for the cells to be added
            nextStageCells = []
            #Logic of the Game of Life'
            list1 = []
            for i in range(len(activeCells)):
                list1.append((activeCells[i].x, activeCells[i].y, activeCells[i].infected, activeCells[i].mask))
            for cell1 in activeCells:
                if cell1.timer > 0:
                    cell1.timer += 1
                if cell1.timer > 15*epoch:
                    cell1.infected = 1
                #Checks to see if infected
                # print(cell1.x, cell1.y, cell1.infected)
                if cell1.infected == 1:
                    numInfected += 1
                else:
                    numNotInfected += 1
                if cell1.infected == 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            x = 0
                            if cell1.mask == 0:
                                if (cell1.x + i, cell1.y + j, 1, 0) in list1:
                                    x = random.randint(1, 100)
                                    if x <= infectionRate:
                                        x = 1
                                elif (cell1.x + i, cell1.y + j, 1, 1) in list1:
                                    x = random.randint(1, 100)
                                    if x <= spreaderMask:
                                        x = 1
                            if cell1.mask == 1:
                                if (cell1.x + i, cell1.y + j, 1, 0) in list1:
                                    x = random.randint(1, 100)
                                    if x <= recieverMask:
                                        x = 1
                                elif (cell1.x + i, cell1.y + j, 1, 1) in list1:
                                    x = random.randint(1, 100)
                                    if x <= bothMask:
                                        x = 1
                            if x == 1 and cell1.timer == 0:
                                cell1.timer += 1
            isInfected = []
            wearingMasks = []
            normal = []
            for cell3 in activeCells:
                if cell3.infected == 1:
                    isInfected.append((cell3.x, cell3.y))
                elif cell3.mask == 1:
                    wearingMasks.append((cell3.x, cell3.y))
                else:
                    normal.append((cell3.x, cell3.y))
            minutes = ((printStatement // epoch) // 1) % 60
            hours = (printStatement // epoch) // 60
            # emit maskcomplience
            sio.emit("stats", {
                "numberOfPeople": numberOfCells,
                "maskCompliance": maskCompliance,
                "numInfected": numInfected,
                "percentageInfected": numInfected*100//numberOfCells,
                "hours": hours,
                "minutes": minutes,
                "epoch": epoch
            })
            
            randomVariable = 1
            if hours == 0 and minutes == 30 and printStatement % epoch == 0 or hours == 0 and minutes == 45 and printStatement % epoch == 0 or hours == 1 and minutes == 0 and printStatement % epoch == 0 or hours == 1 and minutes == 30 and printStatement % epoch == 0 or hours == 2 and minutes == 0 and printStatement % epoch == 0 or hours == 3 and minutes == 0 and printStatement % epoch == 0:
                list4.append(numInfected)
            for i in range(numberOfCells):
                # Checks to see if they are infected, if they are, set it to red, if it's wearing a mask, set it to yellow, otherwise black
                if (activeCells[i].x, activeCells[i].y) in isInfected:
                    rectList[i].setFill("red")
                elif (activeCells[i].x, activeCells[i].y) in wearingMasks:
                    rectList[i].setFill("yellow")
                else:
                    rectList[i].setFill("light gray")
                #moves all of them by 1
                moveX = random.randint(-1, 1) * boxSize
                moveY = random.randint(-1, 1) * boxSize
                #Check if they are off the map, so it moves them back in
                if activeCells[i].y >= (screenHeight // boxSize) - borderSize - 1 or activeCells[i].x >= (screenWidth // boxSize) - borderSize - 1 or activeCells[i].x <= borderSize or activeCells[i].y <= borderSize:
                    if activeCells[i].y >= (screenHeight // boxSize) - borderSize - 1:
                        activeCells[i].y -= 1
                        rectList[i].move(0, -(boxSize))
                    if activeCells[i].x >= (screenWidth // boxSize) - borderSize - 1:
                        activeCells[i].x -= 1
                        rectList[i].move(-(boxSize*1), 0)
                    if activeCells[i].x <= borderSize:
                        activeCells[i].x += 1
                        rectList[i].move((boxSize*1), 0)
                    if activeCells[i].y <= borderSize:
                        activeCells[i].y += 1
                        rectList[i].move(0, (boxSize*1))
                else:
                    rectList[i].move(moveX, moveY)
                    activeCells[i].x += moveX // boxSize
                    activeCells[i].y += moveY // boxSize
            sio.emit("cells", [cell.jso for cell in activeCells])
            sio.emit("cells_data", {
                "infected": [f"{i[0]},{i[1]}" for i in isInfected],
                "masked": [f"{i[0]},{i[1]}" for i in wearingMasks],
                "normal": [f"{i[0]},{i[1]}" for i in normal]
            })
            time.sleep(1.5)
            printStatement += 1
            # if printStatement % epoch == 0:
            # 	print("Epoch " + str(printStatement // epoch) + ", " + str(numInfected) + ", " + str(numNotInfected))
            #Check if everyone is infected:
            if printStatement // epoch > 180:
                dataset.append(list4)
                list4 = []
                print(dataset)
                # for i in range(len(dataset)):
                # 	averageEpoch += (dataset[i])
                # averageEpoch = averageEpoch // len(dataset)
                # print("The average amount of Epochs it takes to infected the whole screen for " + str(maskCompliance) +
                #  " percent compliance rate is: " + str(averageEpoch))
                # for i in range(len(dataset)-1, -1, -1):
                # 	minutes = ((dataset[i]) // 1) % 60
                # 	hours = (dataset[i]) // 60
                # 	text = Text(Point(screenWidth + sideBarSize/2, 400 + 20*(len(dataset)-i)), "Trial " + str(i+1) + ": " + str(hours) + "h " + str(minutes) + "m ")
                # 	trialsList.append(text)
                # 	text.draw(win)
                averageEpoch = 0
                if len(dataset) >= 15:
                    #Setting up the csv file
                    filename = "data.csv"
                    with open(filename, 'a') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow((maskCompliance, density, dataset))  
                    dataset = []
                    if maskCompliance == 0:
                        maskCompliance = 50
                    elif maskCompliance == 50:
                        maskCompliance = 90
                    elif maskCompliance == 90:
                        maskCompliance = 100
                    elif maskCompliance == 100:
                        maskCompliance = 0
                        # boxSize = 8
                        screenHeight = 976
                        screenWidth = 976
                        if screenWidth == 564:
                            numberOfCells -= 10
                            if numberOfCells < 20:
                                numberOfCells = 60
                                screenWidth == 976
                                screenHeight == 976
                        if screenWidth == 976:
                            numberOfCells -= 5
                        density = ((screenWidth*screenHeight)/(boxSize*boxSize))/numberOfCells #orignial design is 16, bar is 1.6 and grocery store is 41.7
                break

            # print("Currently, there are " + str(numInfected) + " infected people and " + str(numNotInfected) + " people not infected")
            # print("There are " + str(offScreen) + " cells off screen."

@sio.event
def connect_error():
    print("The connection failed!")

@sio.on("tick")
def tickHandler(data):
    print("handling tick")
    print(data)


@sio.on("kill")
def kill():
    print("Exiting!")
    sio.disconnect()
    exit()



sio.connect("http://localhost:5000/")