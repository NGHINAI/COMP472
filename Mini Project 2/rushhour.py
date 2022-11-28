from queue import PriorityQueue
import numpy as np
import copy
import time

class puzzle:
    openList_gamestate = []

    def __init__(self, array, gas):
        self.array = array
        self.gas = gas
        self.cost = 0
        self.previousState = []
        self.previousMove = ""
        self.horver = {}
        self.carsizes = {}

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # Checks if the game is done based on if the ambulance is in its final position.
    def isgamedone(self, currarray):
        if currarray[2][5] == 'A' and currarray[2][4] == 'A':

            return True
        else:
            return False

    def h1(self, h1array):
        # List keeping track of all the cars blocking the ambulance
        carsinfront = []
        ambulancerow = h1array[2]
        # Position of the ambulance
        ampos = np.argwhere(ambulancerow == 'A')
        # Position of the ambulance that is closest to the exit
        closesttoexit = ampos[self.carsizes['A'] - 1][0]
        # Iterate through all of the positions in front of the ambulance and see if a car is blocking it or not, no repeat values
        for x in range(closesttoexit + 1, 6):
            if ambulancerow[x] != '.' and ambulancerow[x] not in carsinfront:
                carsinfront.append(self.array[2][x])
        # Return the number of cars in front of the ambulance
        return len(carsinfront)

    def h2(self, h2array):
        # List keeping track of all the blocked positions
        blockedpositions = []
        ambulancerow = h2array[2]
        # Position of the ambulance
        ampos = np.argwhere(ambulancerow == 'A')
        # Position of the ambulance that is closest to the exit
        closesttoexit = ampos[self.carsizes['A'] - 1][0]
        # Iterate through all the positions in front of the ambulance and see if it is occupied or not.
        for x in range(closesttoexit + 1, 6):
            if self.array[2][x] != '.':
                blockedpositions.append(self.array[2][x])
        # Return the number of blocked positions in front of the ambulance.
        return len(blockedpositions)

    def h3(self, h3array):
        theta = 3

        # Return the value of h1 multiplied by a constant factor.
        return theta * self.h1(h3array)

    # def moveCar(car, direction, distance, currentarray): # How do we want to take gas into account

    def h4(self, currentArray):
        # number of cars around the ambulance
        # if we want to ignore parallel cars check if horver.get(currentArray[row][col+1] == "v")
        carsAround = []
        # row above
        for row in range(1, 4):
            for col in range(0, self.array.shape[1]):
                if (currentArray[row][col + 1] == 'A' and self.horver.get(
                        currentArray[row][col + 1] == "v")):  # column after is A
                    carsAround.append(currentArray[row][col])
                if (currentArray[row][col - 1] == 'A' and self.horver.get(
                        currentArray[row][col - 1] == "v")):  # column before is A
                    carsAround.append(currentArray[row][col])
                if (currentArray[row + 1][col] == 'A' and self.horver.get(
                        currentArray[row + 1][col] == "v")):  # row below is A
                    carsAround.append(currentArray[row][col])
                if (currentArray[row - 1][col] == 'A' and self.horver.get(
                        currentArray[row - 1][col] == "v")):  # row above is A
                    carsAround.append(currentArray[row][col])
        carsAround = set(carsAround)
        return len(carsAround)

    def canValet(self, valarr):
        ambulancerow = valarr[2]
        if ambulancerow[5] == ambulancerow[4] and ambulancerow[5] != '.':
            return True
        else:
            return False

    def removeValet(self, valremove):
        removeVal = valremove[2][5]
        ambulancerow = valremove[2]
        for x in range(0, 6):
            if ambulancerow[x] == removeVal:
                ambulancerow[x] = '.'

    def possmoves(self, statearray, gasarray):
        emptyspots = np.argwhere(statearray == ".")
        possmoves = []
        for spot in emptyspots:
            horizontalrow = statearray[spot[0]]
            if (spot[1] < 5):
                spottoright = horizontalrow[spot[1] + 1]
                if (spottoright != "." and self.horver[spottoright] == "h"):
                    if (gasarray[spottoright] >= 1):
                        possmoves.append([spottoright, "L", 1])
            if (spot[1] > 0):
                spottoleft = horizontalrow[spot[1] - 1]
                if (spottoleft != '.' and self.horver[spottoleft] == "h"):
                    if (gasarray[spottoleft] >= 1):
                        possmoves.append([spottoleft, "R", 1])

            verticalcol = statearray[:, spot[1]]
            if (spot[0] < 5):
                spotbelow = verticalcol[spot[0] + 1]
                if (spotbelow != "." and self.horver[spotbelow] == "v"):
                    if (gasarray[spotbelow] >= 1):
                        possmoves.append(([spotbelow, "U", 1]))
            if (spot[0] > 0):
                spotabove = verticalcol[spot[0] - 1]
                if (spotabove != "." and self.horver[spotabove] == "v"):
                    if (gasarray[spotabove] >= 1):
                        possmoves.append(([spotabove, "D", 1]))

        # print(possmoves)
        return possmoves

    def movecar(self, gamestate, movedetails):
        temparr = copy.deepcopy(gamestate)
        # print(f"game state: \n{temparr} \n with {movedetails}")
        if (movedetails[1] == "L"):
            carplacement = np.argwhere(gamestate == movedetails[0])
            leftmostcar = carplacement[0]
            rightmostcar = carplacement[len(carplacement) - 1]
            temparr[leftmostcar[0], leftmostcar[1] - 1] = movedetails[0]
            temparr[rightmostcar[0], rightmostcar[1]] = '.'
        elif (movedetails[1] == "R"):
            carplacement = np.argwhere(gamestate == movedetails[0])
            leftmostcar = carplacement[0]
            rightmostcar = carplacement[len(carplacement) - 1]
            temparr[leftmostcar[0], leftmostcar[1]] = '.'
            temparr[rightmostcar[0], rightmostcar[1] + 1] = movedetails[0]

        elif (movedetails[1] == "U"):
            carplacement = np.argwhere(gamestate == movedetails[0])
            upmostcar = carplacement[0]
            bottommostcar = carplacement[len(carplacement) - 1]
            temparr[upmostcar[0] - 1, upmostcar[1]] = movedetails[0]
            temparr[bottommostcar[0], bottommostcar[1]] = '.'
        elif (movedetails[1] == "D"):
            carplacement = np.argwhere(gamestate == movedetails[0])
            upmostcar = carplacement[0]
            bottommostcar = carplacement[len(carplacement) - 1]
            temparr[upmostcar[0], upmostcar[1]] = '.'
            temparr[bottommostcar[0] + 1, bottommostcar[1]] = movedetails[0]
        # print(temparr)
        return temparr


# set up

# Open the input file to get values
with open('inputfile.txt') as f:
    lines = f.readlines()

# Initialization of variables to track data
array = np.empty((6, 6), dtype=object)  # Array that holds the car positions
arrcount = 0  # Used to place the car value at the correct index
gascount = 0  # Used to count which gas value we are currently reading
carsingame = []  # Used to keep track of all the car names that are in the game
cargas = {}  # Dictionary containing all the gas values for cars with restricted car values.
horver = {}  # Dictionary which tracks if the car can move horizontally or vertically.
carsizes = {}  # Dictionary containing the size of all cards.

# Read through every line, we split each line into words based on empty space.
for line in lines:
    word = line.split(' ')
    # Check to make sure that the line isn't a comment or empty.
    if "#" not in word[0]:
        if line.strip():
            # Move every character in the word into a 6 x 6 array.
            for char in word[0]:
                row = int(arrcount / 6) % 6
                col = arrcount % 6
                # Add car name values that have not been added yet to carsingame.
                if char not in carsingame and char != '.' and char != '\n':
                    carsingame.append(char)
                arrcount = arrcount + 1
                if (arrcount <= 36):
                    array[row, col] = char

        gascount = 0
        # Take all the words after the first as that is where the gas values begin.
        word = word[1:]
        # For each word found after, we append the value to a cargas dictionary.
        with open("ucs-sol-#.txt", "w+") as sol:
            sol.write(str(array))
        for words in word:
            print("word: ")
            print(words)
            currcarletter = word[gascount][0]
            currcargas = int(word[gascount][1])
            cargas[currcarletter] = currcargas
            gascount = gascount + 1

for car in carsingame:
    stringtochararray = list(car)
    test = stringtochararray
    if car not in cargas.keys():
        cargas[car] = 100

# print(cargas)

# Go through all the cars in the game and create a dictionary which tracks which way it can move.
for car in carsingame:
    currarr = np.argwhere(array == car)
    row1 = currarr[0][0]
    row2 = currarr[1][0]
    if row1 == row2:
        horver[car] = "h"
    else:
        horver[car] = "v"

# Create dictionary with size of all cars.
for car in carsingame:
    currarr = np.argwhere(array == car)
    carsizes[car] = int(np.prod(currarr.shape) / 2)

with open("ucs-sol-#.txt", "a") as sol:
    sol.write(f"\n\n\n{str(cargas)}")


def uniformcostsearch(puzzleObj):
    start = time.time()

    open_list = []
    closed_list = []

    currentArray = puzzleObj.array
    currentGasArray = puzzleObj.gas
    currentState = puzzleObj
    closed_list.append(puzzleObj)

    print(currentArray)
    movesLeft = False
    while (not (puzzleObj.isgamedone(currentArray)) and movesLeft == False):
        currentPossMoves = puzzleObj.possmoves(currentArray, currentGasArray)

        for move in currentPossMoves:
            carBeingMoved = move[0]
            newCost = currentState.cost
            if not (move == currentState.previousMove):
                newCost = currentState.cost + 1

            newGasArray = copy.deepcopy(currentGasArray)
            newEntry = {carBeingMoved: newGasArray.get(carBeingMoved) - 1}
            newGasArray.update(newEntry)

            tempArray = puzzleObj.movecar(currentArray, move)

            if puzzleObj.canValet(tempArray) and tempArray[2][5] != 'A':
                tempArray = puzzleObj.removeValet(tempArray)

            # print(type(puzzle))
            newState = puzzle.__new__(puzzle)
            newState.__init__(tempArray, newGasArray)
            newState.cost = newCost
            newState.previousState = currentArray
            newState.previousMove = move
            newState.horver = puzzleObj.horver
            newState.carsizes = puzzleObj.carsizes

            inClosedState = False
            for closedState in closed_list:
                if np.array_equal(closedState.array, newState.array):
                    inClosedState = True

            inOpenState = False
            for openState in open_list:
                if np.array_equal(openState.array, newState.array):
                    if (openState.cost > newState.cost):
                        openState.cost = newState.cost
                    inOpenState = True

            if not (inOpenState) and not (inClosedState):
                open_list.append(newState)

        lowestCost = open_list[0].cost

        for openPuzzle in open_list:
            if openPuzzle.cost < lowestCost:
                lowestCost = openPuzzle.cost

        puzzleArray = []
        for openPuzzle in open_list:
            if lowestCost == openPuzzle.cost:
                puzzleArray.append(openPuzzle)

        closed_list.append(puzzleArray[0])
        open_list.remove(puzzleArray[0])
        currentState = puzzleArray[0]
        currentArray = puzzleArray[0].array
        currentGasArray = puzzleArray[0].gas

        # if not open_list and closed_list[len(closed_list)-1].array[2][5] != 'A':
        #    movesLeft = True
        #    print("no moves left")
    finalMove = closed_list[len(closed_list) - 1]
    tempMove = finalMove
    end = time.time()
    with open("ucs-sol-#.txt", "a") as sol:
        sol.write(f"\nExecution Time: {end-start} seconds")
    reversedArray = []
    # store all info in a couple lists then iterate through
    while np.shape(tempMove.previousState) == (6, 6):
        print(tempMove.array, tempMove.cost)

        for i in range(len(closed_list)):
            if np.array_equal(closed_list[i].array, tempMove.previousState):
                tempMove = closed_list[i]
                reversedArray.append(tempMove)
                with open("ucs-sol-#.txt", "a") as sol:
                    sol.write(f"\n{ tempMove.previousMove}\t{tempMove.array[0][0:6]}{ tempMove.array[1][0:6]}{ tempMove.array[2][0:6]}{ tempMove.array[3][0:6]}{tempMove.array[4][0:6]}{ tempMove.array[5][0:6]}")
    with open("ucs-sol-#.txt", "a") as sol:
        sol.write(f"\n{tempMove.array}")

initialPuzzle = puzzle.__new__(puzzle)
initialPuzzle.__init__(array, cargas)
initialPuzzle.horver = horver
initialPuzzle.carsizes = carsizes

uniformcostsearch(initialPuzzle)
