import pygame

class Agac(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/generic/Other Vegetation/tree01.png')
        self.rect = self.image.get_rect()
        self.speed = 0


    def update(self):
        self.rect = self.rect.move(self.speed, 0)




def main():
    pygame.init()
    surface = pygame.display.set_mode((640, 480))
    background = pygame.image.load('data/bg.png')
    agac=Agac()
    surface.blit(background, (0,0))
    sprites = pygame.sprite.RenderPlain((agac) )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    agac.speed = -5
                elif event.key == pygame.K_RIGHT:
                    agac.speed = 5
            elif event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    agac.speed = 0

        surface.blit(background, (0,0))
        sprites.draw(surface)
        pygame.display.flip()

if __name__=="__main__":
    main()