import pygame
from pygame.locals import *
from pygame import surfarray
import numpy as np
from numba import jit

@jit
def mandelbrot(creal, cimag, maxiter):
    real = creal
    imag = cimag
    for i in range(maxiter):
        real2 = real*real
        imag2 = imag*imag
        if real2+imag2 > 4.0:
            return i
        imag = 2*real*imag + cimag
        real = real2 - imag2 + creal
    return 0

@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter, matrix):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    for i in range(width):
        for j in range(height):
            it = mandelbrot(r1[i], r2[j], maxiter)
            matrix[i,j] = (it, it, it)
    return (r1, r2, matrix)

def main():
    pygame.init()
    size = (640,480)
    area = (-2.0, 0.5, -1.25, 1.25)
    matrix = np.zeros(size+(3,))
    matrix = mandelbrot_set(area[0], area[1], area[2], area[3], size[0], size[1], 10000, matrix)[2]
    yuzey = pygame.display.set_mode(size, pygame.FULLSCREEN)
    while True:
        ev =pygame.event.poll()
        if ev.type == pygame.QUIT or ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE:
            break
        surfarray.blit_array(yuzey, matrix)
        pygame.display.flip()
    pygame.quit()

if __name__=='__main__':
    main()