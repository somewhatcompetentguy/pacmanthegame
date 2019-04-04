import pygame
pygame.init()

SIZE = 30
WIDTH, HEIGHT = SIZE*28,SIZE*31

BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (25,25,166)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 5

walls = pygame.sprite.Group()
objects = pygame.sprite.Group()

class GameObject(pygame.sprite.Sprite):
    def __init__(self, start, speed, colour):
        super().__init__()
        self.image = pygame.Surface((SIZE,SIZE))
        self.rect = self.image.get_rect()
        self.image.fill(colour)
        self.rect.x = start[0]
        self.rect.y = start[1]
        self.velx = 0
        self.vely = 0
        self.speed = speed
        objects.add(self)

    def update(self):
        self.rect.x += self.velx*self.speed
        hit_list = pygame.sprite.spritecollide(self,walls,False)
        for block in hit_list:
            if self.velx > 0:
                self.rect.right = block.rect.left
            elif self.velx < 0:
                self.rect.left = block.rect.right
            self.velx = 0
        
        self.rect.y += self.vely
        hit_list = pygame.sprite.spritecollide(self,walls,False)
        for block in hit_list:
            if self.vely > 0 :
                self.rect.bottom = block.rect.top
            elif self.vely < 0:
                self.rect.top = block.rect.bottom
            self.vely = 0

pacImages = [pygame.image.load("pacclosed.png"),
             pygame.image.load("pacup.png"),
             pygame.image.load("pacdown.png"),
             pygame.image.load("pacleft.png"),
             pygame.image.load("pacright.png")
             ]

class Pacman(pygame.sprite.Sprite):
    def __init__(self, start, speed):
        super().__init__()
        self.image = pacImages[0]
        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.x = start[0]
        self.rect.y = start[1]
        self.velx = 0
        self.vely = 0
        self.speed = speed
        objects.add(self)
        self.direction = 0

    def update(self):
        self.rect.x += self.velx*self.speed
        hit_list = pygame.sprite.spritecollide(self,walls,False)
        for block in hit_list:
            if self.velx > 0:
                self.rect.right = block.rect.left
            elif self.velx < 0:
                self.rect.left = block.rect.right
            self.velx = 0
        
        self.rect.y += self.vely*self.speed
        hit_list = pygame.sprite.spritecollide(self,walls,False)
        for block in hit_list:
            if self.vely > 0 :
                self.rect.bottom = block.rect.top
            elif self.vely < 0:
                self.rect.top = block.rect.bottom
            self.vely = 0

        self.currentImage += 1
        self.currentImage %= 2
        if self.currentImage == 0:
            self.image = pacImages[0]
        else:
            self.image = pacImages[self.direction]
            
class Wall(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface((rect[2]*SIZE, rect[3]*SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = [rect[1]*SIZE, rect[0]*SIZE]
        walls.add(self)


wallCoords = [[0,0,28,1],
              [0,30,28,1],
              [0,0,1,10],
              [0,27,1,10],
              [0,13,2,5],
              [2,2,4,3],
              [2,7,5,3],
              [2,16,5,3],
              [2,22,4,3],
              [6,2,4,2],
              [6,22,4,2],
              [6,7,2,8],
              [6,19,2,8],
              [6,10,8,2],
              [9,0,6,1],
              [9,9,3,2],
              [9,16,3,2],
              [9,22,5,1],
              [8,13,2,3],
              [9,5,1,5],
              [9,22,1,5],
              [13,0,6,1],
              [13,22,6,1]]

def initWalls():
    for wall in wallCoords:
        Wall(wall)

player = Pacman((400,400), 15)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.vely = -1
                player.velx = 0
                player.direction = 1
            elif event.key == pygame.K_DOWN:
                player.vely = 1
                player.velx = 0
                player.direction = 2
            if event.key == pygame.K_LEFT:
                player.velx = -1
                player.vely = 0
                player.direction = 3
            elif event.key == pygame.K_RIGHT:
                player.velx = 1
                player.vely = 0
                player.direction = 4
                
##        if event.type == pygame.KEYUP:
##            if event.key == pygame.K_UP and player.vely == -1:
##                player.vely = 0
##            elif event.key == pygame.K_DOWN and player.vely == 1:
##                player.vely = 0
##            if event.key == pygame.K_LEFT and player.velx == -1:
##                player.velx = 0
##            elif event.key == pygame.K_RIGHT and player.velx == 1:
##                player.velx = 0

initWalls()

def update():
    objects.update()

def render():
    screen.fill(BLACK)
    objects.draw(screen)
    walls.draw(screen)
    pygame.display.update()

while True:
    events()
    update()
    render()
    clock.tick(FPS)

