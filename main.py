from contextlib import nullcontext
from email.headerregistry import Group
from tokenize import group
import pygame
import pygame.gfxdraw
import random
import os

# constant
FPS = 60
BGCOLOR = (156, 194, 255)
WIDTH = 600
HEIGHT = 550
SPRITECOLOR = (0,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (105,105,105)

# file loaded from local computer
icon = pygame.image.load(os.path.join("img","icon.png"))
icon.set_colorkey(WHITE)

# game initiation and game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("P0NG")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# load music and bgm
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.1)
bounce_sound = pygame.mixer.Sound(os.path.join("sound","bounce.wav"))

# score system
font_name = pygame.font.match_font('Maiandra GD')
def draw_text(surf,text,size,color,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# init function
def draw_init():
    screen.fill(BGCOLOR)
    draw_text(screen,"PONG!",64,WHITE,WIDTH/2,HEIGHT/4)
    draw_text(screen,"P1 uses W and S to move, P2 uses up and down arrow to move.",20,WHITE,WIDTH/2,HEIGHT/2)
    draw_text(screen,"Press any button to start the game!",18,WHITE,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # receive input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYUP:
                waiting = False
                return False

# sprite
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,90))
        self.image.fill(SPRITECOLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT/2 - self.rect.height/2
        self.speedr = 7.5
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedr
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedr
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,90))
        self.image.fill(SPRITECOLOR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.rect.width - 10
        self.rect.y = HEIGHT/2 - self.rect.height/2
        self.speedr = 7.5
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedr
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedr
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ballf = pygame.Surface((14,14),pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(ballf, 7, 7, 6, SPRITECOLOR)
        pygame.gfxdraw.filled_circle(ballf, 7, 7, 6, SPRITECOLOR)
        self.image = ballf
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speedx = random.randrange(-4,4)
        self.speedy = random.randrange(-2,2)
        while self.speedx == 0 or self.speedy == 0:
            self.speedx = random.randrange(-4,4)
            self.speedy = random.randrange(-2,2)
    def update(self):
        global scoreP1
        global scoreP2
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x <= 0:
            scoreP2 += 1
            self.kill()
            self.rect.center = (WIDTH/2, HEIGHT/2)
            self.speedx = random.randrange(-4,0)
            while self.speedx == 0:
                self.speedx = random.randrange(-4,0)
            self.speedy = random.randrange(-2,2)
            while self.speedy == 0:
                self.speedy = random.randrange(-2,2)
            all_sprites.add(ball)
        elif self.rect.x >= WIDTH:
            scoreP1 += 1
            self.kill()
            self.rect.center = (WIDTH/2, HEIGHT/2)
            self.speedx = random.randrange(0,4)
            while self.speedx == 0:
                self.speedx = random.randrange(0,4)
            self.speedy = random.randrange(-2,2)
            while self.speedy == 0:
                self.speedy = random.randrange(-2,2)
            all_sprites.add(ball)
    def bounce(self):
        self.yacceleration = 0.5
        if self.rect.y < 0 or self.rect.bottom > HEIGHT:
            self.speedy = -self.speedy
            if self.speedy < 0:
                self.speedy = self.speedy - self.yacceleration
            else:
                self.speedy = self.speedy + self.yacceleration
            bounce_sound.play()
        hitsP1 = self.rect.colliderect(player1)
        hitsP2 = self.rect.colliderect(player2)
        if (hitsP1 or hitsP2):
            self.xacceleration = 0.3
            bounce_sound.play()
            if self.speedx < 0:
                self.speedx = -self.speedx + self.xacceleration
            else:
                self.speedx = -self.speedx - self.xacceleration


pygame.mixer.music.play(-1)

# game loop
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        # adding sprites to list
        all_sprites = pygame.sprite.Group()
        player1 = Player1()
        all_sprites.add(player1)
        ball = Ball()
        all_sprites.add(ball)
        player2 = Player2()
        all_sprites.add(player2)
        # score mark
        scoreP1 = 0
        scoreP2 = 0
    clock.tick(FPS)
    # receive input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update game / rendering
    all_sprites.update()
    ball.bounce()
    if scoreP1 == 11 or scoreP2 == 11:
        show_init = True
    # output screen
    screen.fill(BGCOLOR)
    all_sprites.draw(screen)
    draw_text(screen,str(scoreP1),18,BLACK,WIDTH/2 - WIDTH/4,10)
    draw_text(screen,str(scoreP2),18,BLACK,WIDTH/2 + WIDTH/4,10)
    pygame.draw.line(screen,GREY,(WIDTH/2,0),(WIDTH/2,HEIGHT),1)
    pygame.display.update()

# quit game
pygame.quit()