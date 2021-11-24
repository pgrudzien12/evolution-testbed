from time import sleep, perf_counter
import sys
import pygame
import numpy as np
from gol import Evolution

def createScreen():
    print('available resolutions', pygame.display.list_modes(0))
    #@todo make this a command line switch
    #the next two lines set up full screen options, to run in a window see below
    screen_width, screen_height = (800,600)# pygame.display.list_modes(0)[0] 
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
    return np.zeros(shape=(x,y), dtype=np.int)

BLACK = (0, 0, 0)

def draw_block(x, y, XY, alive_color, size):
    #cell_size=(2,2)
    center_point = (XY[0][x], XY[1][y])
    #u = x * cell_size[0] + (cell_size[0] // 2)
    #w = x * cell_size[0] + (cell_size[0] // 2)
    pygame.draw.circle(screen, alive_color, center_point, size)

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

def precompute_centers(cell_size, world_size):
    X = np.zeros(shape=(world_size[0],))
    Y = np.zeros(shape=(world_size[1],))

    for x in range(world_size[0]):
        X[x] = x * cell_size[0] + (cell_size[0] // 2)
    
    for y in range(world_size[1]):
        Y[y] = y * cell_size[1] + (cell_size[1] // 2)
    return [X,Y]

def main():
    world_size = (300,300)
    pygame.init()
    clock = pygame.time.Clock()
    global screen 
    screen = createScreen()
    (xmax,ymax)= screen.get_size()
    h = 0
    cell_number = 0
    alive_color = pygame.Color(0,0,0)
    alive_color.hsva = [h, 100, 100]
    cell_size = np.array((xmax // world_size[0], ymax // world_size[1]))
    XY = precompute_centers(cell_size, world_size)
    #xlen = xmax // cell_size[0]
    #ylen = ymax // cell_size[1]
    #global world
    xored = make_empty_grid(*world_size)
    buf1 = make_empty_grid(*world_size)
    buf2 = make_empty_grid(*world_size)
    first_buf = True
    e = Evolution(world_size)
    e.initialize(buf1)
    duration = 0
    i = 0
    while True:
        start = perf_counter()

        i+=1
        if handleInputEvents():
            buf1 = make_empty_grid(*world_size)
            buf2 = make_empty_grid(*world_size)
            e.initialize(buf1)
            first_buf = True

        handle = perf_counter()

        if first_buf:
            world = buf1
            buf = buf2
        else:
            world = buf2
            buf = buf1

        draw_start = perf_counter()
        alive_w = np.argwhere(world > 0)
        # np.logical_xor(world, buf, out=xored)
        # change = np.argwhere(xored > 0)

        screen.fill((BLACK))
        csize = min(cell_size) / 2
        for x,y in alive_w:
            draw_block(x, y, XY, alive_color, csize)

        draw_end = perf_counter()
        pygame.display.flip()

        flip_end = perf_counter()
        h = (h + 2) % 360
        alive_color.hsva = (h, 100, 100)
        
        evolve_start = perf_counter()
        e.evolve(world, buf)

        evolve_end = perf_counter()

        first_buf = not first_buf
        clock.tick(40)

        end = perf_counter()
        duration += end - start
        print(f"Perf:{(duration / i):.4f} last {(end-start):.4f}, handleInput {(handle-start):.4f},draw:{(draw_end-draw_start):.4f} flip:{(flip_end-draw_end):.4f} evolution:{(evolve_end-evolve_start):.4f} rest:{(end-evolve_end):.4f} ")
        #print(f"Perf:{(end-start):.4f} handleInput {(handle-start):.4f},draw:{(draw_end-start):.4f} evolution:{(evolve_end-start):.4f} ")

if __name__ == '__main__':
    main()
