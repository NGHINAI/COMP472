import numpy as np
import copy
import time

class puzzle:
    openList_gamestate = []

    #Defining puzzle objects
    def __init__(self, array, gas):
        self.array = array
        self.gas = gas
        self.cost = 0
        self.previousState = []
        self.previousMove = ""
        self.horver = {}
        self.carsizes = {}
        self.distanceTravelled = 0

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

        for col in range(0, self.array.shape[1]):
            if col<=4 and currentArray[2][col-1] == 'A' and self.horver.get(currentArray[2][col+1]) == "v" and currentArray[2][col] == 'A':  # column after is A
                carsAround.append(currentArray[2][col+1])

        length = len(carsAround)
        return length
    def canValet(self, valarr):
        ambulancerow = valarr[2]
        if ambulancerow[5] == ambulancerow[4] and ambulancerow[5] != '.':
            return True
        else:
            return False

    def removeValet(self, valremove):
        #This function removes cars from the valet spotby seeing the value at the valet spot and then removing all the
        #instances from the game.
        removeVal = valremove[2][5]
        ambulancerow = valremove[2]
        for x in range(0, 6):
            if ambulancerow[x] == removeVal:
                ambulancerow[x] = '.'

    def possmoves(self, statearray, gasarray):
        #This function returns all the possible moves (of length one) possible at a state. We first look at all the
        #empty spots in the game.
        emptyspots = np.argwhere(statearray == ".")
        possmoves = []
        #Iterate through every empty spot.
        for spot in emptyspots:
            #Checking fo horizontal moves.
            horizontalrow = statearray[spot[0]]
            #Check the spot to the right as long as we aren't at the right most column.
            if (spot[1] < 5):
                spottoright = horizontalrow[spot[1] + 1]
                #Check the value to the right, if it's a car that moves horizontally and has gas, it can move to
                #the left 1 spot.
                if (spottoright != "." and self.horver[spottoright] == "h"):
                    if (gasarray[spottoright] >= 1):
                        possmoves.append([spottoright, "L", 1])
            #Check the spot to the left as long as we aren't at the left most column.
            if (spot[1] > 0):
                spottoleft = horizontalrow[spot[1] - 1]
                #Check the value to the left, if it's a car that moves horizontally and has gas, it can move to
                #the right 1 spot.
                if (spottoleft != '.' and self.horver[spottoleft] == "h"):
                    if (gasarray[spottoleft] >= 1):
                        possmoves.append([spottoleft, "R", 1])

            #Checking vertical moves.
            verticalcol = statearray[:, spot[1]]
            #Check that we aren't at the top most row.
            if (spot[0] < 5):
                spotbelow = verticalcol[spot[0] + 1]
                #If there is a vertical car below with gas, it can move up once.
                if (spotbelow != "." and self.horver[spotbelow] == "v"):
                    if (gasarray[spotbelow] >= 1):
                        possmoves.append(([spotbelow, "U", 1]))

            #Check that we aren't at the bottom most row
            if (spot[0] > 0):
                spotabove = verticalcol[spot[0] - 1]
                #If there is a vertical car above with gas, it can move down once.
                if (spotabove != "." and self.horver[spotabove] == "v"):
                    if (gasarray[spotabove] >= 1):
                        possmoves.append(([spotabove, "D", 1]))
        return possmoves

    def movecar(self, gamestate, movedetails):
        temparr = copy.deepcopy(gamestate)

        #Moves the car based on the move details, will shift all the values of the car by one in that direction.
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
        return temparr

def uniformcostsearch(puzzleObj, puzzleNumber):
    print(f"UCS puz#{puzzleNumber}")
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt",
              "w+") as sol:
        sol.write(str(array))
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt",
              "a") as sol:
        sol.write(f"\n\n\n{str(cargas)}")
    with open(f".\search\\ucs-search-{puzzleNumber}.txt", "w+") as sol:
        sol.write(f"\n")

    start = time.time()

    open_list = []
    closed_list = []

    #Initalize all the values based on the puzzle that was passed.
    currentArray = puzzleObj.array
    currentGasArray = puzzleObj.gas
    currentState = puzzleObj
    closed_list.append(puzzleObj)

    movesLeft = False
    #Loop while the game isn't done and while there are still moves left.
    while (not (puzzleObj.isgamedone(currentArray)) and movesLeft == False):
        currentPossMoves = puzzleObj.possmoves(currentArray, currentGasArray)

        #Look at every possible move.
        for move in currentPossMoves:
            carBeingMoved = move[0]
            newCost = currentState.cost
            #If the move is not the same as the last (not a car moving to the right one time again) increase the cost.
            if not (move == currentState.previousMove):
                newCost = currentState.cost + 1
            with open(f".\search\\ucs-search-{puzzleNumber}.txt", "a") as sol:
                sol.write(f"\n{newCost}\t{newCost}\t0\t{currentArray[0][0:6]}{ currentArray[1][0:6]}{ currentArray[2][0:6]}{ currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
            #Update arrays
            newGasArray = copy.deepcopy(currentGasArray)
            newEntry = {carBeingMoved: newGasArray.get(carBeingMoved) - 1}
            newGasArray.update(newEntry)

            #Create a temporary array containing the array after the move is applied.
            tempArray = puzzleObj.movecar(currentArray, move)

            #If we can valet  a car that is not the ambulance remove it.
            if puzzleObj.canValet(tempArray) and tempArray[2][5] != 'A':
                tempArray = puzzleObj.removeValet(tempArray)

            # print(type(puzzle))
            #Create a a new state based on the values set above
            newState = puzzle.__new__(puzzle)
            newState.__init__(tempArray, newGasArray)
            newState.cost = newCost
            newState.previousState = currentArray
            newState.previousMove = move
            newState.horver = puzzleObj.horver
            newState.carsizes = puzzleObj.carsizes

            inClosedState = False
            #Check if the state exists in the closed states.
            for closedState in closed_list:
                if np.array_equal(closedState.array, newState.array):
                    inClosedState = True

            #Check if the state exists in the open states and if it does, select the 'cheapest'
            inOpenState = False
            for openState in open_list:
                if np.array_equal(openState.array, newState.array):
                    if (openState.cost > newState.cost):
                        openState.cost = newState.cost
                    inOpenState = True

            #If the state is not in the open or closed state, add it to the open list.
            if not (inOpenState) and not (inClosedState):
                open_list.append(newState)

        #See if the state is already in the closed list once again.
        alreadyInClosedList = False
        for value in range(len(closed_list)):
            if np.array_equal(currentState, closed_list[value]):
                alreadyInClosedList = True

        #If there are no more moves in the open list and there are no more possible moves, cars don't have any gas left
        #or it's already in the closed list, print that there is no solution.
        if len(open_list) == 0 and (len(puzzleObj.possmoves(closed_list[len(closed_list) - 1].array, closed_list[
            len(closed_list) - 1].gas)) == 0 or alreadyInClosedList):
            print("No Solution")
            with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "w") as sol:
                sol.write("No Solution")
            break

        lowestCost = open_list[0].cost

        #To select the next move, we look for the lowest cost in the open moves.
        for openPuzzle in open_list:
            if openPuzzle.cost < lowestCost:
                lowestCost = openPuzzle.cost

        puzzleArray = []
        #Create an array containing all the states whose cost is the lowest cost.
        for openPuzzle in open_list:
            if lowestCost == openPuzzle.cost:
                puzzleArray.append(openPuzzle)

        #Append the values from the first values in the puzzle array to the closed list and remove it from the open list.
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
    movesList = []
    searchLength = len(closed_list)
    end = time.time()
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nExecution Time: {end-start} seconds \t order in reversed")
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt","a") as sol:
        sol.write(f"\nFinal State: \n{tempMove.array}")
    reversedArray = []
    # store all info in a couple lists then iterate through
    while np.shape(tempMove.previousState) == (6, 6):
        # print(tempMove.array, tempMove.cost)

        for i in range(len(closed_list)):
            if np.array_equal(closed_list[i].array, tempMove.previousState):
                tempMove = closed_list[i]
                movesList.append(closed_list[i].previousMove)
                reversedArray.append(tempMove)
                with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
                    sol.write(f"\n{ tempMove.previousMove}\t{tempMove.array[0][0:6]}{ tempMove.array[1][0:6]}{ tempMove.array[2][0:6]}{ tempMove.array[3][0:6]}{tempMove.array[4][0:6]}{ tempMove.array[5][0:6]}")
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\n{tempMove.array}")
        # print(f"{tempMove.array}, {tempMove.cost}\n")
        # readbale console

    solnLength = 0
    movesList.remove('')
    solutionPath = []
    previousMove = []
    for move in range(len(movesList)):
        if not np.array_equal(movesList[move], previousMove):
            solnLength = solnLength + 1
            solutionPath.append(movesList[move])
        else:
            solutionPath[len(solutionPath) - 1][2] += 1

        previousMove = movesList[move]
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSearch path length: {searchLength} ")
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path length: {solnLength} ")
    with open(f".\solutions\\ucs-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path: {solutionPath} ")
    #adding to an analysis
    with open(f".\\analysis.txt", "a") as sol:
        sol.write(f"\n{puzzleNumber}\t UCS\tNA\t{solnLength}\t{searchLength} \t{end - start} ")




def GBFS(puzzleObj, heuristicNum, puzzleNumber):
    print(f"GBFS puz#{puzzleNumber}")
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt","w+") as sol:
        sol.write(str(array))
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\n\n\n{str(cargas)}")
    with open(f".\search\GBFS-{heuristicNum}-search-{puzzleNumber}.txt", "w+") as sol:
        sol.write(f"\n")
    start = time.time()

    open_list = []
    closed_list = []

    currentArray = puzzleObj.array
    currentGasArray = puzzleObj.gas
    currentState = puzzleObj
    closed_list.append(puzzleObj)

    # print(currentArray)
    movesLeft = False
    #Loop while the game isn't done and while there are still moves left.
    while (not (puzzleObj.isgamedone(currentArray)) and movesLeft == False):
        currentPossMoves = puzzleObj.possmoves(currentArray, currentGasArray)

        #Iterate through all the possible moves of this state.
        for move in currentPossMoves:
            carBeingMoved = move[0]
            newCost = currentState.cost

            newGasArray = copy.deepcopy(currentGasArray)
            newEntry = {carBeingMoved: newGasArray.get(carBeingMoved) - 1}
            newGasArray.update(newEntry)

            tempArray = puzzleObj.movecar(currentArray, move)

            #If this is not a move of the same car in the same direction, set the cost based on the heuristic value
            #passed in the function.
            if not (move == currentState.previousMove):
                if heuristicNum == 1:
                    newCost = puzzleObj.h1(tempArray)
                    with open(f".\search\GBFS-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(newCost)}\t0\t{newCost}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 2:
                    newCost = puzzleObj.h2(tempArray)
                    with open(f".\search\GBFS-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(newCost)}\t0\t{newCost}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 3:
                    newCost = puzzleObj.h3(tempArray)
                    with open(f".\search\GBFS-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(newCost)}\t0\t{newCost}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 4:
                    newCost = puzzleObj.h4(tempArray)
                    with open(f".\search\GBFS-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(newCost)}\t0\t{newCost}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")

            #If there is a car in valet that is not the ambulance, remove it.
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

            #Check whether the state is in the closed state list already.
            inClosedState = False
            for closedState in closed_list:
                if np.array_equal(closedState.array, newState.array):
                    inClosedState = True

            #Check whether the state is in the open list already and if it is, check which has the lowest cost.
            inOpenState = False
            for openState in open_list:
                if np.array_equal(openState.array, newState.array):
                    if (openState.cost > newState.cost):
                        openState.cost = newState.cost
                    inOpenState = True

            #If it is not in the open or closed state append it to the open list.
            if not (inOpenState) and not (inClosedState):
                open_list.append(newState)

        #Check once again if the value is already in the closed list.
        alreadyInClosedList = False
        for value in range(len(closed_list)):
            if np.array_equal(currentState, closed_list[value]):
                alreadyInClosedList =True

        #If there are no more moves in the open list and there are no more possible moves, cars don't have any gas left
        #or it's already in the closed list, print that there is no solution.
        if len(open_list)==0 and (len(puzzleObj.possmoves(closed_list[len(closed_list)-1].array, closed_list[len(closed_list)-1].gas))==0 or alreadyInClosedList):
            print("No Solution")
            with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt","w+") as sol:
                sol.write("No Solution")
            break
        lowestCost = open_list[0].cost

        #Iterate through the open list to find the lowest cost.
        for openPuzzle in open_list:
            if openPuzzle.cost < lowestCost:
                lowestCost = openPuzzle.cost

        #Append all values with the lowest cost to an array.
        puzzleArray = []
        for openPuzzle in open_list:
            if lowestCost == openPuzzle.cost:
                puzzleArray.append(openPuzzle)

        #Append the first value with the lowest cost to the closed list and remove it from the open list.
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
    movesList = []
    searchLength = len(closed_list)
    end = time.time()
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt","a") as sol:
        sol.write(f"\nExecution Time: {end-start} seconds \t order in reversed")
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt","a") as sol:
        sol.write(f"\nFinal State: \n{tempMove.array}")


    # store all info in a couple lists then iterate through
    while np.shape(tempMove.previousState) == (6, 6):
        # print(f"{tempMove.array}, {tempMove.cost}\n")
        #readbale console

        for i in range(len(closed_list)):
            if np.array_equal(closed_list[i].array, tempMove.previousState):
                tempMove = closed_list[i]
                movesList.append(closed_list[i].previousMove)
                with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt","a") as sol:
                    sol.write(f"\n{ tempMove.previousMove}\t{tempMove.array[0][0:6]}{ tempMove.array[1][0:6]}{ tempMove.array[2][0:6]}{ tempMove.array[3][0:6]}{tempMove.array[4][0:6]}{ tempMove.array[5][0:6]}")

    solnLength = 0
    movesList.remove('')
    solutionPath = []
    previousMove = []
    for move in range(len(movesList)):
        if not np.array_equal(movesList[move], previousMove):
            solnLength = solnLength + 1
            solutionPath.append(movesList[move])
        else:
            solutionPath[len(solutionPath) - 1][2] += 1

        previousMove = movesList[move]

    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSearch path length: {searchLength} ")
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path length: {solnLength} ")
    with open(f".\solutions\GBFS-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path: {solutionPath} ")
    #adding to analysis
    with open(f".\\analysis.txt", "a") as sol:
        sol.write(f"\n{puzzleNumber}\t GBFS\th{heuristicNum}\t{solnLength}\t{searchLength} \t{end - start} ")



def AStar(puzzleObj, heuristicNum, puzzleNumber):
    print(f"AStar h:{heuristicNum}; puz#{puzzleNumber}")
    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt","w+") as sol:
        sol.write(str(array))
    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\n\n\n{str(cargas)}")
    with open(f".\search\AStar-{heuristicNum}-search-{puzzleNumber}.txt", "w+") as sol:
        sol.write(f"\n")
    start = time.time()

    open_list = []
    closed_list = []

    currentArray = puzzleObj.array
    currentGasArray = puzzleObj.gas
    currentState = puzzleObj
    closed_list.append(puzzleObj)

    # print(currentArray)
    movesLeft = False
    #Loop while the game isn't done and while there are still moves left.
    while (not (puzzleObj.isgamedone(currentArray)) and movesLeft == False):
        currentPossMoves = puzzleObj.possmoves(currentArray, currentGasArray)

        #Check for all the possible moves.
        for move in currentPossMoves:
            carBeingMoved = move[0]
            newDistanceCost = currentState.distanceTravelled

            #If the move is the same as the last, set it's cost to the g(n) of the previous move.
            if not (move == currentState.previousMove):
                newDistanceCost = currentState.distanceTravelled

            newGasArray = copy.deepcopy(currentGasArray)
            newEntry = {carBeingMoved: newGasArray.get(carBeingMoved) - 1}
            newGasArray.update(newEntry)

            tempArray = puzzleObj.movecar(currentArray, move)
            newCost = currentState.cost

            #Alter the cost of the state based on the heuristic value that was passed in.
            if not (move == currentState.previousMove):
                if heuristicNum == 1:
                    newCost = puzzleObj.h1(tempArray) + newDistanceCost
                    with open(f".\search\AStar-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(puzzleObj.h1(tempArray) + currentState.distanceTravelled)}\t{currentState.distanceTravelled}\t{puzzleObj.h1(tempArray)}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 2:
                    newCost = puzzleObj.h2(tempArray) + newDistanceCost
                    with open(f".\search\AStar-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(puzzleObj.h2(tempArray) + currentState.distanceTravelled)}\t{currentState.distanceTravelled}\t{puzzleObj.h2(tempArray)}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 3:
                    newCost = puzzleObj.h3(tempArray) + newDistanceCost
                    with open(f".\search\AStar-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(puzzleObj.h3(tempArray) + currentState.distanceTravelled)}\t{currentState.distanceTravelled}\t{puzzleObj.h3(tempArray)}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")
                elif heuristicNum == 4:
                    newCost = puzzleObj.h4(tempArray) + newDistanceCost
                    with open(f".\search\AStar-{heuristicNum}-search-{puzzleNumber}.txt", "a") as sol:
                        sol.write(
                            f"\n{(puzzleObj.h4(tempArray) + currentState.distanceTravelled)}\t{currentState.distanceTravelled}\t{puzzleObj.h4(tempArray)}\t{currentArray[0][0:6]}{currentArray[1][0:6]}{currentArray[2][0:6]}{currentArray[3][0:6]}{currentArray[4][0:6]}{currentArray[5][0:6]}")

            #Check if we can valet a car that is not the ambulance.
            if puzzleObj.canValet(tempArray) and tempArray[2][5] != 'A':
                tempArray = puzzleObj.removeValet(tempArray)

            # print(type(puzzle))
            newState = puzzle.__new__(puzzle)
            newState.__init__(tempArray, newGasArray)
            newState.cost = newCost
            newState.distanceTravelled = newCost
            newState.previousState = currentArray
            newState.previousMove = move
            newState.horver = puzzleObj.horver
            newState.carsizes = puzzleObj.carsizes

            #Check if the state is in the closed state list.
            inClosedState = False
            for closedState in closed_list:
                if np.array_equal(closedState.array, newState.array):
                    inClosedState = True

            #Check if the state is in the open state list, if it is, check if it is cheaper than the one currently there.
            inOpenState = False
            for openState in open_list:
                if np.array_equal(openState.array, newState.array):
                    if (openState.cost > newState.cost):
                        openState.cost = newState.cost
                    inOpenState = True

            #Append the state based on whether or not it was found in the open or closed state list.
            if not (inOpenState) and not (inClosedState):
                open_list.append(newState)

        #Check once again if the value is already in the closed list.
        alreadyInClosedList = False
        for value in range(len(closed_list)):
            if np.array_equal(currentState, closed_list[value]):
                alreadyInClosedList = True

        #If there are no more moves in the open list and there are no more possible moves, cars don't have any gas left
        #or it's already in the closed list, print that there is no solution.
        if len(open_list) == 0 and (len(puzzleObj.possmoves(closed_list[len(closed_list) - 1].array, closed_list[
            len(closed_list) - 1].gas)) == 0 or alreadyInClosedList):
            print("No Solution")
            with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt","w+") as sol:
                sol.write("No Solution")
            break

        lowestCost = open_list[0].cost
        #Find the lowest cost in the open list.
        for openPuzzle in open_list:
            if openPuzzle.cost < lowestCost:
                lowestCost = openPuzzle.cost

        puzzleArray = []
        #Put all of the values with the lowest cost into an array.
        for openPuzzle in open_list:
            if lowestCost == openPuzzle.cost:
                puzzleArray.append(openPuzzle)

        #Append the lowest cost array to the closed list and remove it from the open list.
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
    movesList = []
    searchLength = len(closed_list)
    end = time.time()
    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nExecution Time: {end-start} seconds \t order in reversed")


    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt","a") as sol:
        sol.write(f"\nFinal State: \n{tempMove.array}")
    # store all info in a couple lists then iterate through
    while np.shape(tempMove.previousState) == (6, 6):
        # print(f"{tempMove.array}, {tempMove.cost}\n")
        #removed for readable console

        for i in range(len(closed_list)):
            if np.array_equal(closed_list[i].array, tempMove.previousState):
                tempMove = closed_list[i]
                movesList.append(closed_list[i].previousMove)
                with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
                    sol.write(f"\n{ tempMove.previousMove}\t{tempMove.array[0][0:6]}{ tempMove.array[1][0:6]}{ tempMove.array[2][0:6]}{ tempMove.array[3][0:6]}{tempMove.array[4][0:6]}{ tempMove.array[5][0:6]}")

    solnLength = 0
    movesList.remove('')
    solutionPath = []
    previousMove = []
    for move in range(len(movesList)):
        if not np.array_equal(movesList[move], previousMove):
            solnLength = solnLength + 1
            solutionPath.append(movesList[move])
        else:
            solutionPath[len(solutionPath)-1][2] += 1

        previousMove = movesList[move]

    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSearch path length: {searchLength} ")
    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path length: {solnLength} ")
    with open(f".\solutions\AStar-{heuristicNum}-sol-{puzzleNumber}.txt", "a") as sol:
        sol.write(f"\nSolution path: {solutionPath} ")


    #adding to analysis
    with open(f".\\analysis.txt","a") as sol:
        sol.write(f"\n{puzzleNumber}\t A/A*\th{heuristicNum}\t{solnLength}\t{searchLength} \t{end-start} ")
# set up

# Open the input file to get values
with open('inputfile.txt') as f:
    lines = f.readlines()

puzzleNum = 1

for line in lines:
    # Initialization of variables to track data
    array = np.empty((6, 6), dtype=object)  # Array that holds the car positions
    arrcount = 0  # Used to place the car value at the correct index
    gascount = 0  # Used to count which gas value we are currently reading
    carsingame = []  # Used to keep track of all the car names that are in the game
    cargas = {}  # Dictionary containing all the gas values for cars with restricted car values.
    horver = {}  # Dictionary which tracks if the car can move horizontally or vertically.
    carsizes = {}  # Dictionary containing the size of all cards.

    # Read through every line, we split each line into words based on empty space.
    word = line.split(' ')
    # Check to make sure that the line isn't a comment or empty.
    if line.isspace() or "#" in word[0]:
        continue

    elif "#" not in word[0]:
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
        for words in word:
            print("word: ")
            print(words)
            currcarletter = word[gascount][0]
            currcargas = int(word[gascount][1])
            cargas[currcarletter] = currcargas
            gascount = gascount + 1

    #Set the gas for cars that did not have a gas value set for them.
    for car in carsingame:
        stringtochararray = list(car)
        test = stringtochararray
        if car not in cargas.keys():
            cargas[car] = 100


# Go through all the cars in the game and create a dictionary which tracks which way it can move.
    for car in carsingame:
        currarr = np.argwhere(array == car)
        row1 = currarr[0][0]
        row2 = currarr[1][0]
        #Set the axis of the car based on whether their row values are the same or not.
        if row1 == row2:
            horver[car] = "h"
        else:
            horver[car] = "v"

    # Create dictionary with size of all cars.
    for car in carsingame:
        currarr = np.argwhere(array == car)
        carsizes[car] = int(np.prod(currarr.shape) / 2)


    initialPuzzle = puzzle.__new__(puzzle)
    initialPuzzle.__init__(array, cargas)
    initialPuzzle.horver = horver
    initialPuzzle.carsizes = carsizes
    print(f"Puzzle#:{puzzleNum}")
    uniformcostsearch(initialPuzzle, puzzleNum)
    # GBFS(initialPuzzle, 1, puzzleNum)
    # GBFS(initialPuzzle, 2, puzzleNum)
    # GBFS(initialPuzzle, 3, puzzleNum)
    # GBFS(initialPuzzle, 4, puzzleNum)
    # AStar(initialPuzzle, 1, puzzleNum)
    # AStar(initialPuzzle, 2, puzzleNum)
    # AStar(initialPuzzle, 3, puzzleNum)
    # AStar(initialPuzzle, 4, puzzleNum)

    puzzleNum = puzzleNum + 1
