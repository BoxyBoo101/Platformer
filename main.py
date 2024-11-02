import pygame
pygame.init()
clock = pygame.time.Clock()
SCREENWIDTH = 1200
SCREENHEIGHT = 900
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Plat")
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Assets/player/Idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def draw(self): 
        display.blit(self.image, self.rect)


player = Soldier(200, 200, 3)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    player.draw()
    pygame.display.update()

pygame.quit()
