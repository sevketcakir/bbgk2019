import pygame
from pygame.locals import *
import numpy as np
from pygame import surfarray
import time
from numba import jit

@jit
def mandelbrot(creal,cimag,maxiter):
    real = creal
    imag = cimag
    for n in range(maxiter):
        real2 = real*real
        imag2 = imag*imag
        if real2 + imag2 > 4.0:
            return n
        imag = 2* real*imag + cimag
        real = real2 - imag2 + creal
    return 0


@jit
def mandelbrot_set4(xmin,xmax,ymin,ymax,width,height,maxiter,n3):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    #n3 = np.empty((width,height,3))
    for i in range(width):
        for j in range(height):
            it = mandelbrot(r1[i],r2[j],maxiter)
            n3[i,j] = (it,0,0)
    return (r1,r2,n3)

def zoomin(x1,x2,y1,y2,mx,my,ratio):
    dx=x2-x1
    dy=y2-y1
    x1 = x1 + mx*dx*(1-ratio)
    x2 = x2 - (1-mx)*dx*(1-ratio)
    y1 = y1 + my*dy*(1-ratio)
    y2 = y2 - (1-my)*dy*(1-ratio)
    return (x1,x2,y1,y2)

def zoomout(x1,x2,y1,y2,mx,my,ratio):
    dx=x2-x1
    dy=y2-y1
    x1 = x1 - mx*dx*(1-ratio)
    x2 = x2 + (1-mx)*dx*(1-ratio)
    y1 = y1 - my*dy*(1-ratio)
    y2 = y2 + (1-my)*dy*(1-ratio)
    return (x1,x2,y1,y2)

def main():
    start = time.time()
    pygame.init()
    font = pygame.font.Font(None, 20)
    clock = pygame.time.Clock()
    size = (700,700)
    area =(-2.0,0.5,-1.25,1.25)
    newarea=area[:]
    matrix = np.zeros(size+(3,))
    matrix = mandelbrot_set4(area[0], area[1], area[2], area[3], size[0], size[1], 255, matrix)[2]
    # matrix += 127
    # mandelbrot(matrix)
    print(f"Hesaplama süresi: {time.time()-start} sn")
    yuzey = pygame.display.set_mode(size, pygame.FULLSCREEN)
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
            break
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            mx/=size[0]
            my/=size[1]
            if ev.button == 4:
                newarea = zoomin(*area, mx, my, 0.9)
            elif ev.button == 5:
                newarea = zoomout(*area, mx, my, 0.9)
        #yuzey.fill((0,255,128))
        if newarea != area:
            matrix = mandelbrot_set4(area[0], area[1], area[2], area[3], size[0], size[1], 255, matrix)[2]
        area=newarea
        surfarray.blit_array(yuzey, matrix)
        fps = font.render(str(int(clock.get_fps()))+' FPS', True, pygame.Color('green'))
        yuzey.blit(fps, (50, 50))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
    main()