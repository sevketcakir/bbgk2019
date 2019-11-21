import pygame, sys
from pygame.locals import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.states={'right':{}, 'left':{}}
        self.direction='right'
        self.state='idle'
        self.stateidx = 0

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,value): self.rect.topleft = value
    position = property(_getpos,_setpos)
    
    def next_state(self):
        if self.stateidx == len(self.states[self.direction])-1:
            self.stateidx = 0
            print('Direction change')
            if self.direction == 'right':
                self.direction = 'left'
            else:
                self.direction = 'right'
        else:
            self.stateidx = (self.stateidx+1) % len(self.states[self.direction])
        self.state = list(self.states[self.direction].keys())[self.stateidx]
    
    def load(self, filename, width, height, columns, animations):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.state = animations[0][0]
        for state, start, end, handle in animations:
            self.states['right'][state]={'images':[], 'handle': handle}
            for i in range(start, end):
                frx = (i%columns)*width
                fry = (i//columns)*height
                img = self.master_image.subsurface(Rect(frx,fry,width,height))
                self.rect = img.get_rect()
                self.states['right'][state]['images'].append(img)
        for state in self.states['right']:
            self.states['left'][state]={'images':[], 'handle': handle}
            for img in self.states['right'][state]['images']:
                self.states['left'][state]['images'].append(pygame.transform.flip(img,1,0))
            
    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            #if self.frame > self.last_frame:
            #    self.frame = self.first_frame
            self.last_time = current_time
            #print(self.last_frame)

        #build current frame only if it changed
        if self.frame != self.old_frame:
            imglist = self.states[self.direction][self.state]['images']
            self.image = imglist[(self.frame)%len(imglist)]
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((320,240), FULLSCREEN)
    framerate = pygame.time.Clock()
    bg = pygame.image.load("data/bg.png").convert_alpha()
    
    player = MySprite()
    animations = [('idle', 0, 4, None),
                  ('crouch', 4, 8, None),
                  ('run', 8, 14, None),
                  ('takla', 14, 24, None),
                  ('kayma', 24, 29, None),
                  ('grab',29,33,None),
                  ('climb',33,38,None),
                  ('idle2',38,42,None),
                  ('attack1',42,47,None),
                  ('attack2',47,53,None),
                  ('attack3',53,59,None),
                  ('hurt',59,62,None),
                  ('die',62,69,None),
                  ('draw',69,73,None),
                  ('ensheathe',73,77,None),
                  ('jump',77,79,None),
                  ('slide',79,81,None),
                  ('tread',81,87,None),
                  ('swim',87,91,None),
                  ('ladderclimb',91,95,None)]
    player.load('data/adventurer2/adventurer-1.3-Sheet.png', 50, 37, 8, animations)
    
    group = pygame.sprite.Group()
    group.add(player)

    while True:
        framerate.tick(60)
        ticks = pygame.time.get_ticks()
    
        for event in pygame.event.get():
            if event.type == QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_SPACE:
                    player.next_state()                    
        
        screen.blit(bg, (0,0))
        group.update(ticks, 150)
        group.draw(screen)
        pygame.display.update()
            
    
    
    
if __name__ == '__main__':
    main()