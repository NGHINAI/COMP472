
import numpy as np

# Open the input file to get values
with open('inputfile.txt') as f:
    lines = f.readlines()

# Initialization of variables to track data
array = np.empty((6,6), dtype=object)  # Array that holds the car positions
arrcount = 0  # Used to place the car value at the correct index
gascount = 0  # Used to count which gas value we are currently reading
carsingame = []  # Used to keep track of all the car names that are in the game
cargas = {}  # Dictionary containing all the gas values for cars with restricted car values.
horver = {}  # Dictionary which tracks if the car can move horizontally or vertically.
carsizes = {} # Dictionary containing the size of all cards.
carrows = {} # Idk if we would want these  but might be easy to make a list for each row and column detailing which cars can move in
            # that direction so that we just search for . and then we know how to move it.
carcols = {}

# Read through every line, we split each line into words based on empty space.
for line in lines:
    word = line.split(' ')
    # Check to make sure that the line isn't a comment or empty.
    if "#" not in word[0]:
        if line.strip():
            # Move every character in the word into a 6 x 6 array.
            for char in word[0]:
                row = int(arrcount/6) % 6
                col = arrcount % 6
                # Add car name values that have not been added yet to carsingame.
                if char not in carsingame and char != '.' and char != '\n':
                    carsingame.append(char)
                arrcount = arrcount+1
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
            gascount = gascount+1

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
    carsizes[car] = int(np.prod(currarr.shape)/2)


# Checks if the game is done based on if the ambulance is in its final position.
def isGameDone( currArray ):
    if currArray[2][5] == 'A' and currArray[2][4] == 'A':
        return True
    else:
        return False

def h1( h1array ):
    # List keeping track of all the cars blocking the ambulance
    carsinfront = []
    ambulancerow = h1array[2]
    # Position of the ambulance
    ampos = np.argwhere(ambulancerow == 'A')
    # Position of the ambulance that is closest to the exit
    closesttoexit = ampos[carsizes['A']-1][0]
    # Iterate through all of the positions in front of the ambulance and see if a car is blocking it or not, no repeat values
    for x in range(closesttoexit+1, 6):
        if ambulancerow[x] != '.' and ambulancerow[x] not in carsinfront:
            carsinfront.append(array[2][x])
    # Return the number of cars in front of the ambulance
    return len(carsinfront)

def h2( h2array ):
    # List keeping track of all the blocked positions
    blockedpositions = []
    ambulancerow = h2array[2]
    # Position of the ambulance
    ampos = np.argwhere(ambulancerow == 'A')
    # Position of the ambulance that is closest to the exit
    closesttoexit = ampos[carsizes['A']-1][0]
    # Iterate through all the positions in front of the ambulance and see if it is occupied or not.
    for x in range(closesttoexit+1, 6):
        if array[2][x] != '.':
            blockedpositions.append(array[2][x])
    # Return the number of blocked positions in front of the ambulance.
    return len(blockedpositions)

def h3( h3array ):
    theta = 3
    # Return the value of h1 multiplied by a constant factor.
    return theta*h1(h3array)


# def moveCar(car, direction, distance, currentarray): # How do we want to take gas into account




