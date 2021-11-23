from time import sleep, perf_counter
import sys
import pygame
import numpy as np
from gol import Evolution

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


def make_empty_grid(x, y):
    grid = []
    for r in range(x):
        row = []
        for c in range(y):
            row.append(0)
        grid.append(row)
    return np.array(grid)

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
def handleInputEvents():
    reinitialize = False
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button==1): #left click
                reinitialize = True
        if(event.type == pygame.KEYDOWN):
            sys.exit(0) #quit on any key
        if (event.type == pygame.QUIT):  #pygame issues a quit event, for e.g. by closing the window
            print("quitting")
            sys.exit(0)
    return reinitialize
            
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
    #global world
    buf1 = make_empty_grid(xlen, ylen)
    buf2 = make_empty_grid(xlen, ylen)
    first_buf = True
    e = Evolution(world_size)
    e.initialize(buf1)
    duration = 0
    i = 0
    while True:
            i+=1
            if handleInputEvents():
                buf1 = make_empty_grid(xlen, ylen)
                buf2 = make_empty_grid(xlen, ylen)
                e.initialize(buf1)
                first_buf = True

            if first_buf:
                world = buf1
                buf = buf2
            else:
                world = buf2
                buf = buf1

            alive_w = np.argwhere(world > 0)
            screen.fill((BLACK))
            for x,y in alive_w:
                draw_block(x, y, alive_color, cell_size)

            pygame.display.flip()

            h = (h + 2) % 360
            alive_color.hsva = (h, 100, 100)
            
            start = perf_counter()
            e.evolve(world, buf)
                
            duration += perf_counter() - start
            print("Perf:", duration / i)
            first_buf = not first_buf
            clock.tick(40)

if __name__ == '__main__':
    main()
