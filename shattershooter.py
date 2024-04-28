import pygame

pygame.init()

win = pygame.display.set_mode((500, 400))
clock = pygame.time.Clock()

class GameS(pygame.sprite.Sprite):
    def __init__(self, image, x, y, acc):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.speed = acc
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameS):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

player = Player("ROCKE.png", 350, 0, 1)
background = pygame.transform.scale(pygame.image.load("bgb.png"), (500, 400))

run = True
finish = False

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    if not finish:
        win.blit(background, (0, 0))
        player.update()
        player.reset()

    
    pygame.display.update()
    clock.tick(120)

