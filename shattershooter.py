import pygame
import math
import random

win = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Enemy():
    def __init__(self, x, y, player):
        self.default_image = pygame.transform.scale(pygame.image.load("Lemon.png"), (50, 50))
        self.default_image = pygame.transform.rotate(self.default_image, -90)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        mx, my = player.rect.centerx, player.rect.centery
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.hor = math.cos(math.radians(angle)) * 2
        self.ver = -math.sin(math.radians(angle)) * 2
        

    def update(self):
        self.rect.x += self.hor
        self.rect.y += self.ver



    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet():
    def __init__(self, x, y, angle):
        self.default_image = pygame.transform.scale(pygame.image.load("Bullet.png"),(75, 35))
        self.default_image = pygame.transform.rotate(self.default_image, -90)
        self.image = self.default_image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.xv = math.cos(math.radians(angle)) * 20
        self.yv = -math.sin(math.radians(angle)) * 20
        

    def update(self):
        self.rect.x += self.xv
        self.rect.y += self.yv

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Gun():
    def shoot(self, x, y, angle):
        raise Exception("Gun must have shoot methods")
    
class Laser(Gun):
    def __init__(self):
        self.auto = False
    def shoot(self, x, y, angle):
        return [Bullet(x, y, angle)]

class Bomb(Gun):
    def __init__(self):
        self.auto = False
    def shoot(self, x, y, angle):
        bullets = []
        for i in range(5):
            bullets.append(Bullet(x, y, angle + random.randint(-5, 5)))
        return bullets
    
class Auto(Gun):
    def __init__(self):
        self.auto = True
    def shoot(self, x, y, angle):
        return [Bullet(x, y, angle)]


class Ship():
    def __init__(self, x, y):
        self.default_image = pygame.transform.scale(pygame.image.load("ROCKE.png"), (100, 70))
        self.default_image = pygame.transform.rotate(self.default_image, -90)
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bullets = []
        self.gun = [Laser(), Bomb(), Auto()]
        self.index = 0
        

    def update(self, events, keys):
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        old_x, old_y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(self.default_image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = old_x
        self.rect.centery = old_y
        for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_e:
                        self.index += 1
                        if self.index > 2:
                            self.index = 0
                        print(self.index)

        if not self.gun[self.index].auto:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.bullets += self.gun[self.index].shoot(self.rect.centerx, self.rect.centery, angle)
        else:
            if pygame.mouse.get_pressed()[0]:
                self.bullets += self.gun[self.index].shoot(self.rect.centerx, self.rect.centery, angle)
        
        for b in self.bullets:
            b.update()

        if keys[pygame.K_a]:
            self.rect.x -= 2
        if keys[pygame.K_d]:
            self.rect.x += 2
        if keys[pygame.K_w]:
            self.rect.y -= 2
        if keys[pygame.K_s]:
            self.rect.y += 2


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for b in self.bullets:
            b.draw(surface)

ship = Ship(200, 200)

def Lemon_Spawner():
    location = random.choice(["left", "right"])
    if location == "left":
        return Enemy(-50, random.randint(0, 600), ship)
    if location == "right":
        return Enemy(800, random.randint(0, 600), ship)

enemies = []

Amount_O_Lemon = 1
frames = 0

run = True
while run:
    frames += 1
    if frames >= 50:
        for i in range(Amount_O_Lemon):
            enemies.append(Lemon_Spawner())
        frames = 0
        Amount_O_Lemon += 1

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for e in events:
        if e.type == pygame.QUIT:
            run = False

    ship.update(events, keys)
    for e in enemies:
        e.update()
        for b in ship.bullets:
            if e.rect.colliderect(b.rect):
                ship.bullets.remove(b)
                enemies.remove(e)
                break
    

    win.fill((46, 43, 43))
    ship.draw(win)
    for e in enemies:
        e.draw(win)
    

    pygame.display.update()
    clock.tick(30)
