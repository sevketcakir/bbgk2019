import pygame

class Agac(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/generic/Other Vegetation/tree01.png')
        self.rect = self.image.get_rect()
        self.speed = [0, 0]

    def update(self):
        if self.rect.left+self.speed[0]>0 and self.rect.right+self.speed[0]<640:
            self.rect = self.rect.move(self.speed[0], 0)
        if self.rect.top+self.speed[1]>0 and self.rect.bottom+self.speed[1]<480:
            self.rect = self.rect.move(0, self.speed[1])

class SpaceMan(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.framecount = 0

    def update(self, *args):
        self.framecount += 1
        self.image = self.images[(self.framecount//10)%len(self.images)]

    def load_images(self):
        data = "data/spaceman/Idle_00"
        images = []
        for i in range(6):
            images.append(pygame.image.load(data+str(i)+".png"))
        return images



def main():
    pygame.init()
    surface = pygame.display.set_mode((640, 480))
    background = pygame.image.load('data/bg.png')
    agac=Agac()
    adam = SpaceMan()
    surface.blit(background, (0,0))
    sprites = pygame.sprite.RenderPlain((agac, adam) )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    agac.speed[0] = -5
                elif event.key == pygame.K_RIGHT:
                    agac.speed[0] = 5
                elif event.key == pygame.K_UP:
                    agac.speed[1] = -5
                elif event.key == pygame.K_DOWN:
                    agac.speed[1] = 5
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: #==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    agac.speed[0] = 0
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    agac.speed[1] = 0

        sprites.update()
        surface.blit(background, (0,0))
        sprites.draw(surface)
        pygame.display.flip()

if __name__=="__main__":
    main()