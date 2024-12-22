import pygame
import os 
import random
import time
#add health bar
pygame.init()
clock = pygame.time.Clock()
fps = int(input("How many frames per second do you want to play in? (Playing in less than 60fps will cause issues, but play at 60fps for the most stable game.) "))
speed = 60 / fps
bg = "black"
red = "red"
mode = input("Which mode will you play? (S = Sniper, A = Assult)")
if mode == "S":
    firesfx = pygame.mixer.Sound("Assets/bfg.mp3")
    gundam = 90
    rpm = 18 * speed
    edodgechance = round(3 / speed)
    eburst = 1
    eshotchance = round(100 / speed)
    faceplayer = 1
    bulletspeed = 30
elif mode == "A":
    rpm = 600 * speed
    firesfx = pygame.mixer.Sound("Assets/ak.mp3")
    gundam = 5
    edodgechance = round(50 / speed)
    eburst = 20
    faceplayer = round(3 / speed)
    bulletspeed = 25
    eshotchance = round(40 / speed)

SCREENWIDTH = 1200
SCREENHEIGHT = 900
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Plat")
GRAVITY = 0.6 * speed
bulletimg = pygame.image.load("Assets/icons/bullet.png")
curburst = 0


def drawbg():
    display.fill(bg)
    pygame.draw.line(display, red, (0, 700), (SCREENWIDTH, 700))
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, type, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.health = 100
        self.basehealth = self.health
        self.type = type
        self.speed = speed
        self.ammo = ammo
        self.startammo = ammo
        self.shotcool = 0
        self.dir = 1
        self.flip = False
        self.animlist = []
        animation_types = ["Idle", "Run", "Jump", "Death"]
        self.action = 0
        self.frameindex = 0
        self.updatetime = pygame.time.get_ticks()
        self.jump = False
        self.air = False
        self.vel_y = 0
        for animation in animation_types:
            temp_list = []
            framenum = len(os.listdir(f"Assets/{self.type}/{animation}"))
            for i in range(framenum):
                img = pygame.image.load(f"Assets/{self.type}/{animation}/{i}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animlist.append(temp_list)

        self.image = self.animlist[self.action][self.frameindex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def draw(self): 
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    def update(self):
        self.checkalive()
        self.updateanim()
        if self.shotcool > 0:
            self.shotcool -= 1

    def move(self, movel, mover):
        movinglr = 0
        movey = 0
        if movel:
            movinglr = -self.speed
            self.dir = -1
            self.flip = True
        if mover:
            movinglr = self.speed
            self.dir = 1
            self.flip = False
        if self.jump == True and self.air == False:
            self.vel_y = -12
            self.air = True
            self.jump = False
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        movey += self.vel_y

        if self.rect.bottom + movey > 700:
            movey = 700 - self.rect.bottom
            self.air = False
        if self.rect.left < 20:
            self.rect.left = 20
        if self.rect.right > SCREENWIDTH - 20:
            self.rect.right = SCREENWIDTH - 20
        self.rect.x += movinglr
        self.rect.y += movey * speed


    def updateanim(self):
        animcool = 100

        self.image = self.animlist[self.action][self.frameindex]
        if pygame.time.get_ticks() - self.updatetime > animcool:
            self.updatetime = pygame.time.get_ticks()
            self.frameindex += 1
        
        if self.frameindex >= len(self.animlist[self.action]):
            if self.action == 3:
                self.frameindex = len(self.animlist[self.action]) - 1
            else:
                self.frameindex = 0
    def updateaction(self, newAction):
        if newAction != self.action:
            self.action = newAction
            self.frameindex = 0
            self.updatetime = pygame.time.get_ticks()
    def shoot(self):
        if self.shotcool < 1 and self.ammo > 0:
            self.shotcool = 3600 / rpm
            bullet = Bullet(self.rect.centerx + (0.65 * self.rect.size[0] * self.dir), self.rect.centery, self.dir)
            bulletgroup.add(bullet)
            firesfx.play()
    def checkalive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.speed = 0
            self.updateaction(3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.speed = bulletspeed * speed
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = dir
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < -10 or self.rect.left > SCREENWIDTH + 10:
            
            self.kill()
        if pygame.sprite.spritecollide(player, bulletgroup, False):
            if player.alive:
                player.health -= gundam
                self.kill()
        if pygame.sprite.spritecollide(enemy, bulletgroup, False):
            if enemy.alive:
                enemy.health -= gundam
                self.kill()

bulletgroup = pygame.sprite.Group()


mover = False
movel = False
shoot = False
emover = False
emovel = False
player = Soldier(100, 200, 3, 8 * speed, "player", 20)
enemy = Soldier(1100, 200, 3, 8 * speed, "enemy", 20)


run = True


while run:

    enemy.move(emovel, emover)


    if player.alive:
        if shoot:
            player.shoot()
        if player.air:
            player.updateaction(2)
        elif movel or mover:
            player.updateaction(1) #run
        else:
            player.updateaction(0) #idle
        player.move(movel, mover)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                mover = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                movel = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                mover = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                movel = False  
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            shoot = False


    #Enemy AI
    if enemy.alive:
        curburst -= 1
        if emover or emovel:
            enemy.updateaction(1)
        else:
            enemy.updateaction(0)
        if enemy.jump:
            enemy.updateaction(2)

        #Random movement
        if random.randint(1, round(20 / speed)) == 1:
            if random.randint(1, round(2 / speed)) == 1:
                if enemy.rect.left > 900 and random.randint(1, round(10 / speed)) == 1:
                    emover = False
                    emovel = True
                else:
                    emover = not emover
                
            else:
                if enemy.rect.right < 300 and random.randint(1, round(10 / speed)) == 1:
                    emovel = False
                    emover = True
                else:
                    emovel = not emovel
        #Enemy Jumping
        if shoot:
            if random.randint(1, round(10 / speed)) == 1:
                enemy.jump = True
        if random.randint(1, round(500 / speed)) == 1:
            enemy.jump = True

        #Enemy Shooting
        if random.randint(1, eshotchance) == 2 or curburst > 0:
            if player.rect.left < enemy.rect.left:
                if curburst < 1:
                    if random.randint(1, faceplayer) == 1:
                        enemy.dir = -1
                        emover = False
                        emovel = True
                    enemy.shoot()
                    curburst = eburst
                else:
                    enemy.shoot()
            else:
                if curburst < 1:
                    if random.randint(1, faceplayer) == 1:
                        enemy.dir = 1
                        emover = True
                        emovel = False
                    enemy.shoot()
                    curburst = eburst
                else:
                    enemy.shoot


    drawbg()

    player.update()
    enemy.update()
    player.draw()
    enemy.draw()
    bulletgroup.update()
    bulletgroup.draw(display)
    clock.tick(fps)
    pygame.display.update()

pygame.quit()
