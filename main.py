from time import sleep
from random import randint
import sys
import pygame
from gol import evolve

def createScreen():
    print('available resolutions', pygame.display.list_modes(0))
    #@todo make this a command line switch
    #the next two lines set up full screen options, to run in a window see below
    screen_width, screen_height = (640,480)# pygame.display.list_modes(0)[0] 
    # we use the 1st resolution which is the largest, and ought to give us the full multi-monitor
    options = pygame.HWSURFACE | pygame.DOUBLEBUF        
    
    #the next two lines set up windowed options - swap these with above to run full screen instead
    #screen_width, screen_height = (600,600)
    #options=0
    
    #create the screen with the options
    screen = pygame.display.set_mode(
        (screen_width, screen_height), options)
    print("screen created, size is:", screen.get_size())
    return screen
    


def make_random_grid(x, y):
        grid = []
        for r in range(int(x)):
            row = []
            for c in range(int(y)):
                row.append(randint(0,1))
            grid.append(row)
        return grid

BLACK = (0, 0, 0)

def draw_block(x, y, alive_color, cell_size):
    block_size = 9
    x *= cell_size[0]
    y *= cell_size[1]
    center_point = ((x + (cell_size[0] // 2)), (y + (cell_size[1] // 2)))
    pygame.draw.circle(screen, alive_color, center_point, min(cell_size) / 2,0)

#this is where we register our event listeners
#yes, we're just calling methods
#@todo create proper event listeners
def handleInputEvents(xlen, ylen):
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button==1): #left click
                global world
                world = make_random_grid(xlen, ylen)
        if(event.type == pygame.KEYDOWN):
            sys.exit(0) #quit on any key
        if (event.type == pygame.QUIT):  #pygame issues a quit event, for e.g. by closing the window
            print("quitting")
            sys.exit(0)
            
            
def main():
    world_size = (100,100)
    pygame.init()
    clock = pygame.time.Clock()
    global screen 
    screen = createScreen()
    (xmax,ymax)= screen.get_size()
    h = 0
    cell_number = 0
    alive_color = pygame.Color(0,0,0)
    alive_color.hsva = [h, 100, 100]
    cell_size = (xmax // world_size[0], ymax // world_size[1])
    xlen = xmax // cell_size[0]
    ylen = ymax // cell_size[1]
    global world
    world = make_random_grid(xlen, ylen)
    while True:
            handleInputEvents(xlen, ylen)
            clock.tick(40)
            for x in range(xlen):
                for y in range(ylen):
                    alive = world[x][y]
                    cell_number += 1
                    cell_color = alive_color if alive else BLACK
                    draw_block(x, y, cell_color, cell_size)
            pygame.display.flip()
            h = (h + 2) % 360
            alive_color.hsva = (h, 100, 100)
            world = evolve(world)
            cell_number = 0

if __name__ == '__main__':
    main()
