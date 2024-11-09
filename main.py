import pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60
bg = "black"
SCREENWIDTH = 1200
SCREENHEIGHT = 900
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Plat")
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, type):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Assets/" + type + "/Idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.dir = 1
        self.flip = False
    def draw(self): 
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    def move(self, movel, mover):
        moving = 0
        if movel:
            moving = -self.speed
            self.dir = -1
            self.flip = True
        if mover:
            moving = self.speed
            self.dir = 1
            self.flip = False

        self.rect.x += moving

mover = False
movel = False

player = Soldier(200, 200, 3, 8, "player")
enemy = Soldier(300, 200, 3, 8, "enemy")
run = True
while run:
    display.fill(bg)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mover = True
            if event.key == pygame.K_LEFT:
                movel = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                mover = False
            if event.key == pygame.K_LEFT:
                movel = False  
    player.draw()
    player.move(movel, mover)
    enemy.draw()

    clock.tick(fps)

    pygame.display.update()

pygame.quit()
