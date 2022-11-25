from queue import PriorityQueue
import numpy as np
import copy

class puzzle:

    def __init__(self, array, gas):
        self.array = array
        self.gas = gas
        self.cost = 0
        self.arrcount = 0  # Used to place the car value at the correct index
        self.gascount = 0  # Used to count which gas value we are currently reading
        self.carsingame = []  # Used to keep track of all the car names that are in the game
        self. horver = {}  # Dictionary which tracks if the car can move horizontally or vertically.
        self.carsizes = {}  # Dictionary containing the size of all cards.

    # Checks if the game is done based on if the ambulance is in its final position.
    def isgamedone(currarray):
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

    def canValet(valarr):
        ambulancerow = valarr[2]
        if ambulancerow[5] == ambulancerow[4] and ambulancerow[5] != '.':
            return True
        else:
            return False

    def removeValet(valremove):
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
                    if (gasarray[spottoright] > 1):
                        possmoves.append([spottoright, "L", 1])
            if (spot[1] > 0):
                spottoleft = horizontalrow[spot[1] - 1]
                if (spottoleft != '.' and self.horver[spottoleft] == "h"):
                    if (gasarray[spottoleft] > 1):
                        possmoves.append([spottoleft, "R", 1])

            verticalcol = statearray[:, spot[1]]
            if (spot[0] < 5):
                spotbelow = verticalcol[spot[0] + 1]
                if (spotbelow != "." and self.horver[spotbelow] == "v"):
                    if (gasarray[spotbelow] > 1):
                        possmoves.append(([spotbelow, "U", 1]))
            if (spot[0] > 0):
                spotabove = verticalcol[spot[0] - 1]
                if (spotabove != "." and self.horver[spotabove] == "v"):
                    if (gasarray[spotabove] > 1):
                        possmoves.append(([spotabove, "D", 1]))

        # print(possmoves)
        return possmoves

    def movecar(gamestate, movedetails):
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

def uniformcostsearch(puzzle):
    open_list = PriorityQueue()
    closed_list = []


