import pygame

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
        pass

class Player(GameS):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

bullet = Bullet("Bullet.png", 0, 0, 0)
player = Player("ROCKE.png", 350, 470, 4)
L1 = Lemon(0, 0, 100, 70, 0, 2, "Lemon.png")
L2 = Lemon(200, 0, 100, 70, 0, 2, "Lemon.png")
L3 = Lemon(400, 0, 35, 23, 0, 4, "Lemon.png")
L4 = Lemon(600, 0, 200, 140, 0, 1, "Lemon.png")
lemons = [L1, L2, L3, L4]


run = True
finish = False

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    win.fill((46, 43, 43))
    for lime in lemons:
        lime.draw(win)
        lime.update()


    player.update()
    player.reset()

    
    pygame.display.update()
    clock.tick(30)

