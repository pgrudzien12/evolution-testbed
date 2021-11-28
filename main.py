from time import perf_counter
import sys
import pygame
import numpy as np
from gol import Evolution

# started from this gist: https://gist.github.com/bennuttall/6952575
# big thanks for the original author: Ben Nuttall

def createScreen():
    screen_width, screen_height = (800,800)
    options = pygame.HWSURFACE | pygame.DOUBLEBUF        
  
    screen = pygame.display.set_mode(
        (screen_width, screen_height), options)
    print("screen created, size is:", screen.get_size())
    return screen


def make_empty_grid(x, y):
    return np.zeros(shape=(x,y), dtype=np.int)

BLACK = (0, 0, 0)

def draw_block(screen, x, y, XY, alive_color, size):
    center_point = (XY[0][x], XY[1][y])
    pygame.draw.circle(screen, alive_color, center_point, size)


def handleInputEvents():
    reinitialize = False
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):  #pygame issues a quit event, for e.g. by closing the window
            print("quitting")
            sys.exit(0)
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(event.button==1): #left click
                reinitialize = True
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
    world_size = (200,200)
    pygame.init()
    clock = pygame.time.Clock()
    screen = createScreen()
    (xmax,ymax)= screen.get_size()
    h = 0
    alive_color = pygame.Color(0,0,0)
    alive_color.hsva = [h, 100, 100]
    cell_size = np.array((xmax // world_size[0], ymax // world_size[1]))
    XY = precompute_centers(cell_size, world_size)
    xored = make_empty_grid(*world_size)
    buf1 = make_empty_grid(*world_size)
    buf2 = make_empty_grid(*world_size)
    first_buf = True
    e = Evolution(world_size)
    e.initialize(buf1)
    i = 0
    need_full_redraw = True
    
    csize = min(cell_size) / 2
    while True:
        start = perf_counter()

        i+=1
        if handleInputEvents():
            buf1 = make_empty_grid(*world_size)
            buf2 = make_empty_grid(*world_size)
            e.initialize(buf1)
            first_buf = True
            screen.fill((BLACK))

        handle = perf_counter()

        if first_buf:
            world = buf1
            buf = buf2
        else:
            world = buf2
            buf = buf1
        no_shift = (pygame.key.get_mods() & pygame.KMOD_LSHIFT) == 0
        draw_start = perf_counter()
        if no_shift:
            if need_full_redraw:
                need_full_redraw = False
                screen.fill((BLACK))
                
                change = np.argwhere(world > 0)
            else:
                np.logical_xor(world, buf, out=xored)
                change = np.argwhere(xored > 0)

            for x,y in change:
                if world[x,y] > 0: #born
                    draw_block(screen, x, y, XY, alive_color, csize)
                else: # died
                    draw_block(screen, x, y, XY, BLACK, csize)
        else:
            need_full_redraw = True

        draw_end = perf_counter()
        
        if no_shift:
            pygame.display.flip()

        flip_end = perf_counter()
        h = (h + 2) % 360
        alive_color.hsva = (h, 100, 100)
        
        evolve_start = perf_counter()
        e.evolve(world, buf)

        evolve_end = perf_counter()

        first_buf = not first_buf
        
        if no_shift:
            clock.tick(20)

        end = perf_counter()
        print(f"Perf {(end-start):.4f}: handleInput {(handle-start):.4f} draw:{(draw_end-draw_start):.4f} flip:{(flip_end-draw_end):.4f} evolution:{(evolve_end-evolve_start):.4f} filler:{(end-evolve_end):.4f} ")
        #print(f"Perf:{(end-start):.4f} handleInput {(handle-start):.4f},draw:{(draw_end-start):.4f} evolution:{(evolve_end-start):.4f} ")

if __name__ == '__main__':
    main()
    print("done")
