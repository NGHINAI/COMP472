import numpy as np

# Open the input file to get values
with open('inputfile.txt') as f:
    lines = f.readlines()

t1 = [['B' 'B' 'B' '.' '.' 'M'], ['C' 'C' 'D' 'D' '.' 'M'], ['A' 'A' 'K' 'L' 'E' 'M'], ['J' '.' 'K' 'L' 'E' '.'], ['J' '.' 'G' 'G' '.' '.'], ['J' 'H' 'H' 'H' 'I' 'I']]
t2 = [['B' 'B' 'B' '.' '.' 'M'], ['C' 'C' 'D' 'D' '.' 'M'], ['A' 'A' 'K' 'L' 'E' 'M'], ['J' '.' 'K' 'L' 'E' '.'], ['J' '.' 'G' 'G' '.' '.'], ['J' 'H' 'H' 'H' 'I' 'I']]

h1 = hash(t1)
h1a = hash(t1)
h2 = hash(t2)

print(f"{h1}\n{h1a}\n{h2}")
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


# Checks if the game is done based on if the ambulance is in its final position.
def isgamedone(currarray):
    if currarray[2][5] == 'A' and currarray[2][4] == 'A':
        return True
    else:
        return False


def h1(h1array):
    # List keeping track of all the cars blocking the ambulance
    carsinfront = []
    ambulancerow = h1array[2]
    # Position of the ambulance
    ampos = np.argwhere(ambulancerow == 'A')
    # Position of the ambulance that is closest to the exit
    closesttoexit = ampos[carsizes['A'] - 1][0]
    # Iterate through all of the positions in front of the ambulance and see if a car is blocking it or not, no repeat values
    for x in range(closesttoexit + 1, 6):
        if ambulancerow[x] != '.' and ambulancerow[x] not in carsinfront:
            carsinfront.append(array[2][x])
    # Return the number of cars in front of the ambulance
    return len(carsinfront)


def h2(h2array):
    # List keeping track of all the blocked positions
    blockedpositions = []
    ambulancerow = h2array[2]
    # Position of the ambulance
    ampos = np.argwhere(ambulancerow == 'A')
    # Position of the ambulance that is closest to the exit
    closesttoexit = ampos[carsizes['A'] - 1][0]
    # Iterate through all the positions in front of the ambulance and see if it is occupied or not.
    for x in range(closesttoexit + 1, 6):
        if array[2][x] != '.':
            blockedpositions.append(array[2][x])
    # Return the number of blocked positions in front of the ambulance.
    return len(blockedpositions)


def h3(h3array):
    theta = 3
    # Return the value of h1 multiplied by a constant factor.
    return theta * h1(h3array)


# def moveCar(car, direction, distance, currentarray): # How do we want to take gas into account

def h4(currentArray):
    # number of cars around the ambulance
    # if we want to ignore parallel cars check if horver.get(currentArray[row][col+1] == "v")
    carsAround = []
    # row above
    for row in range(1, 4):
        for col in range(0, array.shape[1]):
            if (currentArray[row][col + 1] == 'A' and horver.get(
                    currentArray[row][col + 1] == "v")):  # column after is A
                carsAround.append(currentArray[row][col])
            if (currentArray[row][col - 1] == 'A' and horver.get(
                    currentArray[row][col - 1] == "v")):  # column before is A
                carsAround.append(currentArray[row][col])
            if (currentArray[row + 1][col] == 'A' and horver.get(currentArray[row + 1][col] == "v")):  # row below is A
                carsAround.append(currentArray[row][col])
            if (currentArray[row - 1][col] == 'A' and horver.get(currentArray[row - 1][col] == "v")):  # row above is A
                carsAround.append(currentArray[row][col])
    carsAround = set(carsAround)
    return len(carsAround)


def canValet(valarr):
    ambulancerow = valarr[2]
    if ambulancerow[5] == ambulancerow[4]:
        return True
    else:
        return False


def removeValet(valremove):
    removeVal = valremove[2][5]
    ambulancerow = valremove[2]
    for x in range(0, 6):
        if ambulancerow[x] == removeVal:
            ambulancerow[x] = '.'


def possmoves(statearray, gasarray):
    emptyspots = np.argwhere(statearray == ".")
    possmoves = []
    for spot in emptyspots:
        horizontalrow = statearray[spot[0]]
        if (spot[1] < 5):
            spottoright = horizontalrow[spot[1] + 1]
            if (spottoright != "." and horver[spottoright] == "h"):
                if (gasarray[spottoright] > 1):
                    possmoves.append([spottoright, "L", 1])
        if (spot[1] > 0):
            spottoleft = horizontalrow[spot[1] - 1]
            if (spottoleft != '.' and horver[spottoleft] == "h"):
                if (gasarray[spottoleft] > 1):
                    possmoves.append([spottoleft, "R", 1])

        verticalcol = statearray[:, spot[1]]
        if (spot[0] < 5):
            spotbelow = verticalcol[spot[0] + 1]
            if (spotbelow != "." and horver[spotbelow] == "v"):
                if (gasarray[spotbelow] > 1):
                    possmoves.append(([spotbelow, "U", 1]))
        if (spot[0] > 0):
            spotabove = verticalcol[spot[0] - 1]
            if (spotabove != "." and horver[spotabove] == "v"):
                if (gasarray[spotabove] > 1):
                    possmoves.append(([spotabove, "D", 1]))

    # print(possmoves)
    return possmoves


def movecar(gamestate, movedetails):
    temparr = gamestate
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


def uniformCostSearch(array, gasarray):
    costcount = 0
    openList_gamestate = []
    openList_cost = []
    openList_moves = []
    closeList_gamestate = []
    gasDict = gasarray
    movesList = []
    closeList_moves = []
    # heuristicList = []

    openList_gamestate.append(array)
    openList_moves.append(possmoves(array, gasDict))
    openList_cost.append(9999)

    while (not (isgamedone(array))):

        # 1 we append the moves that are generated as an array them self into the openList_moves
        # [
        # [[B,R,1],[A,R,1],...] state 0
        # [[D,R,1],[A,L,1],...] state 1
        # ]
        # we need to handle the possible moves in respect to the state we are in when we "make a move"

        # 2 do for each state loop then inside do the for move loop might fix it

        # 3 or we have to add one more inner for loop
        # moves to generate the possible states, states to check if it exists and can be added then another inner loop
        for move in possmoves(array, gasarray):
            print(f"\nstate: \n{array} \n Next move: {move}")
            potentialState = movecar(array, move)
            notInClosedState = False
            # checking if the prospective state is in the closed state
            # and if it is not then check conditions for open state
            for state in range(len(closeList_gamestate)):
                if np.array_equal(potentialState, closeList_gamestate[state]):
                    notInClosedState = True
            if not notInClosedState:
                for state in range(len(openList_gamestate)):
                    # handles if the state to be added to the open list exists already
                    if np.array_equal(potentialState, openList_gamestate[state]):
                        # if new state has a lower cost then replace the old state and order accordingly
                        if (costcount + 1) < openList_cost[state]:
                            newcost = costcount + 1
                            for i in range(len(openList_cost)): #never enters
                                if i == newcost-1:
                                    # moves the new values into ascending order by cost
                                    tempcost = openList_cost[0:i].append(newcost) + openList_cost[i:]
                                    tempgamestate = openList_gamestate[0:i].append(
                                        openList_gamestate[state]) + openList_gamestate[i:]
                                    tempmoves = openList_moves[0:i].append(openList_moves[state]) + openList_moves[i:]
                                    # removes the old information
                                    tempcost.pop(state + 1)
                                    tempgamestate.pop(state + 1)
                                    tempmoves.pop(state + 1)
                                    # reassigns the lists to the reordered lists
                                    openList_cost = tempcost
                                    openList_moves = tempmoves
                                    openList_gamestate = tempgamestate

                    else:
                        openList_moves.append(move)
                        np.append(openList_gamestate, potentialState)
                        openList_cost.append(costcount + 1)

        # now makes a move

        # handle the possible moves in respect to the state they belong to when we "make a move"
        # we should probably check which state we are observing and retrieve that index, so we can use the proper
        # possible moves in openList_moves

        # we also need to fix the openList_cost since it seems it is not adding any values
        # added -1 to line 262 so that it would enter the "if" block I think we need to initialize the cost list with
        # all move cost of the initial state and put them just like the possible openList_moves array

        storedmove = openList_moves[0][0]
        storedgamestate = openList_gamestate[0][0]
        storedcost = openList_cost[0]

        openList_moves =  openList_moves[0][1:]
        openList_gamestate = openList_gamestate[0][1:]
        openList_cost = openList_cost[1:]

        array = movecar(array, storedmove)
        closeList_gamestate.append(storedgamestate)
        closeList_moves.append(storedmove)
        costcount = costcount + 1
        # print(storedmove[0][0])
        # print(gasDict["B"])
        gasDict[storedmove[0][0]] = gasDict.get(storedmove[0][0]) - 1
        # take openlist game states
        # make a move
        # update and append respective variables
        # new state copy into "array" variable

        # print(f"current state: \n{array}")
        # print(f"move done: {storedmove}")
    # print(array)  # if car moves consecutively then count once


# print(array)
print("possible moves:")
uniformCostSearch(array, cargas)
