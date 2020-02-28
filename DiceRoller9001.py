# ********************************IMPORTS**********************************
import sys, os, random, time, math
try:
    import pygame
    from pygame.locals import *
    pygame.init()
except:
    print('PyGame not installed: https://www.pygame.org/wiki/GettingStarted')
    time.sleep(5)


# ********************************CONSTANTS**********************************
# Window Size
WIDTH = 810
HEIGHT = 890

# Colors (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 1-6 die faces that will be loaded
DIEFACES = ['images/Dice1.png', 'images/Dice2.png', 'images/Dice3.png', 'images/Dice4.png', 'images/Dice5.png',
            'images/Dice6.png']


# ********************************VARIABLES**********************************
# initialize windows/canvases
window = pygame.display.set_mode((WIDTH, HEIGHT))       # initialize the window and it's size
diceAmtText = pygame.font.SysFont("Product Sans", 30)   # text font for diceAmt and total
mouse = pygame.mouse                                    # mouse data
_image_library = {}                                     # loaded images
diceAmt = 1                                             # how many dice/die will be rolled
total = 0                                               # all rolled dice/die value(s) added together
diesize = 100


# ===============================BEGIN CODE==================================
# Program:   	Dice Roller 9000
# Definition:   A program that simulates the rolling of x amount of die/dice
# Author:  	    Karl Palmer
# History:      4/25/2019 - initial script creation


# 	Function:   	get_image
# 	Definition:  	loads/gets an image from a file and loads it
# 	Author:  		Karl Palmer
# 	History:        4/25/2019 - Initial Function Creation
def get_image(path):
    global _image_library
    image = _image_library.get(path)  # check to see if the image has already been loaded...

    if image == None:                 # ...add image to list if it hasn't
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)

        # error check if the image can be loaded or not
        try:
            image = pygame.image.load(canonicalized_path)
        except:
            print('image: ' + canonicalized_path + ' could not be found/loaded.')

        _image_library[path] = image  # add image to the list

    return image


# 	Procedure:   	button
# 	Definition:  	checks for a click on a button and does an action depending on what button type it is
# 	Author:  		Karl Palmer
# 	History:        4/25/2019 - Initial Function Creation
#                   2/28/2020 - made sure if diceamt is below 1 it will be set to 1
def button(type, img, xmin, xmax, ymin, ymax, diechange=1):
    global diceAmt
    window.blit(get_image(img), (xmin, ymin))  # display the button

    # check to see if the user has clicked the mouse on the button
    if pygame.mouse.get_pressed()[0] and mouseX > xmin and mouseX < xmax and mouseY > ymin and mouseY < ymax:
        if type == 'sub' and diceAmt - diechange >= 1:
            diceAmt -= diechange
        elif type == 'add':
            diceAmt += diechange
        elif type == 'roll':
            roll()


# 	Procedure:   	drawbg
# 	Definition:  	draws the bgcolor, bottom section bg color, buttons, and text
# 	Author:  		Karl Palmer
# 	History:        4/25/2019 - Initial Function Creation
def drawbg():
    # windows and footer bg color
    window.fill(WHITE)
    pygame.draw.rect(window, BLACK, (0, HEIGHT - 70, WIDTH, 70))

    # remove dice buttons
    button('sub', 'images/Sub4.png', 10, 30, HEIGHT - 45, HEIGHT - 25, 1)
    button('sub', 'images/Sub3.png', 25, 55, HEIGHT - 50, HEIGHT - 20, 10)
    button('sub', 'images/Sub2.png', 47, 87, HEIGHT - 55, HEIGHT - 15, 100)
    button('sub', 'images/Sub.png', 76, 126, HEIGHT - 60, HEIGHT - 15, 1000)

    # add dice buttons xmin xmax ymin ymax
    button('add', 'images/Add4.png', 216, 236, HEIGHT - 45, HEIGHT - 25, 1)
    button('add', 'images/Add3.png', 191, 221, HEIGHT - 50, HEIGHT - 20, 10)
    button('add', 'images/Add2.png', 159, 199, HEIGHT - 55, HEIGHT - 15, 100)
    button('add', 'images/Add.png', 120, 170, HEIGHT - 60, HEIGHT - 10, 1000)

    if diceAmt > 1:
        window.blit(diceAmtText.render("{0} dice".format(diceAmt), 1, WHITE), (250, HEIGHT - 43))
    else:
        window.blit(diceAmtText.render("{0} die".format(diceAmt), 1, WHITE), (250, HEIGHT - 43))

    button('roll', 'images/Roll.png', WIDTH - 100, WIDTH - 16, HEIGHT - 60, HEIGHT - 10)
    window.blit(diceAmtText.render("{0}".format(total), 1, WHITE), (WIDTH - 165, HEIGHT - 43))


# 	Procedure:   	roll
# 	Definition:  	generates random die values and displays them all, including the total.
# 	Author:  		Karl Palmer
# 	History:        4/25/2019 - Initial Function Creation
#                   2/28/2020 - Made scaling better and more efficient code wise
def roll():
    global total, diceAmt
    total = 0  # reset the total

    # calculates amount of rows & columns (square root of dice amount)
    rows = round(math.sqrt(diceAmt))
    cols = math.ceil(diceAmt / rows)

    pos = [0, 0]                # coordinate of die instantiation position

    if diceAmt == 1:
        diesize = WIDTH         # die size if only 1 die is being rolled
    else:
        diesize = WIDTH / cols  # divides the width of the screen by number of columns to get the size of each die

    for die in range(1, diceAmt + 1):
        diefacenum = random.randint(0, 5)  # get a random number from 0 to 5
        total += diefacenum + 1            # add the random number (+1 due to 0-5, not 1-6) to total

        # resize and display the die face the corresponds with the random number
        dieface = pygame.transform.scale(get_image(DIEFACES[diefacenum]), (int(diesize), int(diesize)))
        window.blit(dieface, (round(pos[0]), round(pos[1])))

        # move the x and y position for the next die that will be generated
        pos[0] += diesize
        if pos[0] > WIDTH-diesize:
            pos[1] += diesize
            pos[0] = 0

        pygame.display.update()  # update screen
        if (diceAmt < 100000):
            time.sleep(1/diceAmt)    # delay next die generation


try:
    pygame.display.set_caption('Karl\'s Dice Roller 9000')  # initialize the window's title

    # running game loop
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:       # check for quit even
            break                    # leave the game loop
        else:
            # get mouse x and y positions
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            # update the screen
            drawbg()
            pygame.display.update()

finally:  # exit/quit game
    print('\nClosing Karl\'s Dice Roller 9000...')
    pygame.quit()
    sys.exit()
# =================================END CODE==================================
