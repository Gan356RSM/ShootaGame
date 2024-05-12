import pygame
from random import randint

pygame.init()

# pygame.mixer.init()
# pygame.music.load("fire.egg")
# pygame.mixer.music.play()
# watever = pygame.mixer.Sound("???")

sh = 550
sw = 750

win = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()

class GameS(pygame.sprite.Sprite):
    def __init__(self, image, x, y, acc):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (100, 65))
        self.speed = acc
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Lemon():
    def __init__(self, x, y, w, h, xs, ys, pic):
        self.image = pygame.transform.scale(pygame.image.load(pic),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xs  = xs
        self.ys = ys

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.xs
        self.rect.y += self.ys
        if self.rect.x > sw + 100:
            self.rect.x = 0
        if self.rect.x < -100:
            self.rect.x = sw

        if self.rect.y > sh + 100:
            self.rect.y = 0
        if self.rect.y < -100:
            self.rect.y = sh

class Bullet():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("bullet.png"),(75, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x + 12   
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= 10

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(GameS):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

player = Player("ROCKE.png", 350, 470, 4)
lemons = []
bullets = []

run = True
finish = False

f = pygame.font.Font("font.ttf", 48)
lose_msg = f.render("You Lose!", True, (0, 0, 0))
final_msg = None
  
while run:
    if len(lemons) < 5:
        lemons.append(Lemon(randint(0 ,750), 0, 200, 140, 0, 1, "lemon.png"))
    


    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.x, player.rect.y))
        if e.type == pygame.QUIT:
            run = False

    for l in lemons:
        for b in bullets:
            if l.rect.colliderect(b.rect):
                if l.rect.w == 200:
                    for i in range(3):
                        lemons.append(Lemon(l.rect.x,
                                               l.rect.y,
                                               100,
                                               70,
                                               randint(-2, 2),
                                               randint(-2, 2),
                                               "lemon.png"))
                if l.rect.w == 100:
                    for i in range(7):
                        lemons.append(Lemon(l.rect.x,
                                               l.rect.y,
                                               35,
                                               25,
                                               randint(-4, 4),
                                               randint(-4, 4),
                                               "lemon.png"))
                lemons.remove(l)
                bullets.remove(b)


    win.fill((46, 43, 43))
    for lime in lemons:
        lime.draw(win)
        lime.update()
        if player.rect.colliderect(lime):
            final_msg = lose_msg
    
    for b in bullets:
        b.draw(win)
        b.update()
        if b.rect.y < 0:
            bullets.remove(b)
    


    if final_msg != None:
        win.blit(final_msg, (375, 275))


    player.update()
    player.reset()

    
    pygame.display.update()
    clock.tick(30)



