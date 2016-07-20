from __future__ import print_function

import os, sys, random          # for join: creates system-independent paths
import pygame
from pygame.locals import *

FPS = 40

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

WIDTH  = 1000
HEIGHT = 600
SPACESHIP_VELOCITY = 5
ASTEROID_VELOCITY = 5
BULLET_VELOCITY = 7
SMALL_ASTEROID_RELOAD   = 12
SMALL_ASTEROID_ODDS     = 22
MEDIUM_ASTEROID_RELOAD   = 18
MEDIUM_ASTEROID_ODDS     = 30
LARGE_ASTEROID_RELOAD   = 30
LARGE_ASTEROID_ODDS     = 44
COIN_RELOAD   = 12
COIN_ODDS     = 22
FIRE_RELOAD   = 100
FIRE_ODDS     = 100


def load_background(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

class SmallAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidsmall.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class MediumAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidmedium.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class LargeAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidlarge.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('coin.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fireball.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('laser2.png', WHITE)
        self.vx = BULLET_VELOCITY
        self.rect.x = xpos
        self.rect.y = ypos
    def update(self):
        self.rect.x = self.rect.x + self.vx
        if self.rect.left >= WIDTH:
            self.kill()
class Strength(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
        


# Loads an image from a named file,
# returning a pair of type (image, rect).
def load_image(name, colorkey=None):
    path = os.path.join('data',  name)
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print('Cannot load image: {}'.format(path))
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at( (0, 0) )
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    path = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error, message:
        print('Cannot load sound: {}', path)
        raise SystemExit, message
    return sound





def main():
    pygame.init()
    window = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption('Avoid Asteroid')

    # Clock: used for creating delays in our game
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    #Background
    space_img, space_rect = load_image('space.png', RED)
    space_rect.center = (WIDTH / 2, HEIGHT / 2)
    space_vy = 0
    

    #Spaceship
    spaceship_img, spaceship_rect = load_image('spaceship.png', WHITE)
    spaceship_rect.center = (75, HEIGHT / 2)
    spaceship_vy = 0

    #Starting values
    smallasteroidreload = SMALL_ASTEROID_RELOAD
    mediumasteroidreload = MEDIUM_ASTEROID_RELOAD
    largeasteroidreload = LARGE_ASTEROID_RELOAD
    coinreload = COIN_RELOAD
    firereload = FIRE_RELOAD
    spaceshipvelocity = SPACESHIP_VELOCITY
    asteroidvelocity = ASTEROID_VELOCITY
    counter = 0

    #Background image Start Page
    start_img, start_rect = load_image('asteroid4.png', RED)
    start_rect.center = (WIDTH / 2, HEIGHT / 2)
    start_vy = 0

    #Explosion
    explosion_img, explosion_rect= load_image('explosion.png', WHITE) 
    #explosion_rect.center = (xpos, ypos)
    explosion_vy = 0

    #Load Sound
    boom = load_sound('boom.wav')
    bgmusic = load_sound('music.wav')
    
    



    gameover = False
    sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    power = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    strengths = pygame.sprite.Group()
    start = True
    highscorewritten = False

    while start == True:
        window.fill(BLACK)
        window.blit(start_img, start_rect.topleft)
        (x,y) = pygame.mouse.get_pos()
        text = font.render('Click One player to start', False, RED)
        text_rect = text.get_rect()
        text_rect.center= (WIDTH -150, 30)
        window.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif x > 340 and x < 660 and y > 200 and y < 400:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = False
                    break
        pygame.display.flip()
        clock.tick(FPS)
        if start == False:
            break
        
    



    
    while True:
        # 1. Render the world
        bgmusic.play()
        #Random int
        y = random.randint(0, 600)
        y2 = random.randint(0, 600)
        y3 = random.randint(0, 600)
        y4 = random.randint(0, 600)
        y5 = random.randint(0, 600)
        y6 = random.randint(0, 600)
        #Positioning
        xpos = spaceship_rect.x
        ypos = spaceship_rect.y
        explosion_rect.center = (xpos, ypos)
        window.fill(BLACK)
        window.blit( space_img, space_rect.topleft )
        smallasteroid = SmallAsteroid(1000, y)
        mediumasteroid = MediumAsteroid(1000, y2)
        largeasteroid = LargeAsteroid(1000, y3)
        coin = Coin(1000, y4)
        fire = Fire(1000, y5)
        strength = Strength(1000, y6)
        bullet = Bullet(xpos, ypos + 18)
        bullet2 = Bullet(xpos, ypos)
        bullet3 = Bullet(xpos, ypos + 30)
        # Randomly generate asteroids of three different sizes/ coins
        if smallasteroidreload:
            smallasteroidreload = smallasteroidreload - 1
        elif not int(random.random() * SMALL_ASTEROID_ODDS):
            sprites.add(smallasteroid)
            smallasteroidreload = SMALL_ASTEROID_RELOAD

        if mediumasteroidreload:
            mediumasteroidreload = mediumasteroidreload - 1
        elif not int(random.random() * MEDIUM_ASTEROID_ODDS):
            sprites.add(mediumasteroid)
            mediumasteroidreload = MEDIUM_ASTEROID_RELOAD

        if largeasteroidreload:
            largeasteroidreload = largeasteroidreload - 1
        elif not int(random.random() * LARGE_ASTEROID_ODDS):
            sprites.add(largeasteroid)
            largeasteroidreload = LARGE_ASTEROID_RELOAD

        if coinreload:
            coinreload = coinreload - 1
        elif not int(random.random() * COIN_ODDS):
            coins.add(coin)
            coinreload = COIN_RELOAD
        if firereload:
            firereload = firereload - 1
        elif not int(random.random() * FIRE_ODDS):
            power.add(fire)
            firereload = FIRE_RELOAD
        if firereload:
            firereload = firereload - 1
        elif not int(random.random() * FIRE_ODDS):
            strengths.add(strength)
            firereload = FIRE_RELOAD

        coins.draw(window)
        sprites.draw(window)
        power.draw(window)
        strengths.draw(window)
        if not gameover:
            bullets.draw(window)
            window.blit( spaceship_img, spaceship_rect.topleft )
        #Create small asteroids at time interval

        #Create score
    
        if gameover==False:
            for i in sprites:
                counter = float(counter + .1)
            text = font.render('Score: {}'.format(int(counter)), False, RED)
            text_rect = text.get_rect()
            text_rect.center= (WIDTH -100, 30)
            window.blit(text, text_rect)
            text2 = font.render('Press space to shoot', False, RED)
            text2_rect = text.get_rect()
            text2_rect.center= (WIDTH -200, 570)
            window.blit(text2, text2_rect)

        if gameover:
            text = font.render('You Died!', False, RED)
            text2 = font.render('Score: {}'.format(int(counter)), False, RED)
            text3 = font.render('Press R to Restart', False, RED)
            text_rect = text.get_rect()
            text2_rect = text.get_rect()
            text3_rect = text.get_rect()
            text_rect.center= (WIDTH/2, HEIGHT/2)
            text2_rect.center= (WIDTH/2 - 6, HEIGHT/2 + 30)
            text3_rect.center= (WIDTH/2 - 50, HEIGHT/2 + 60)
            window.blit(text, text_rect)
            window.blit(text2, text2_rect)
            window.blit(text3, text3_rect)
            if highscorewritten == False:
                with open('highscores.txt', 'a') as f:
                     f.write(str(counter))
                     highscorewritten = True
        #Update spaceship rect

    # 2. Update the world
    # Detect collision
        spaceship_rect.y = spaceship_rect.y + spaceship_vy
        sprites.update()
        coins.update()
        power.update()
        bullets.update()
        strengths.update()
        for sprite in sprites:
            if sprite.rect.colliderect(spaceship_rect):
                if gameover == False:
                    window.blit( explosion_img, explosion_rect.topleft )
                    bgmusic.stop()
                    boom.play()
                gameover = True

        for coin in coins:
            if coin.rect.colliderect(spaceship_rect):
                coin.kill()
                counter += 1000.
        for powe in power:
            if powe.rect.colliderect(spaceship_rect):
                powe.kill()
                spaceshipvelocity = 10
        for bullet in bullets:
            for sprite in sprites:
                if bullet.rect.colliderect(sprite.rect):
                    bullet.kill()
                    sprite.kill()
            if bullet.rect.x == WIDTH:
                bullet.kill()
        for strength in strengths:
            if strength.rect.colliderect(spaceship_rect):
                strength.kill()
                bullets.add(bullet2)
                bullets.add(bullet3)




        ##### Detect Wall Collisions #####
        if spaceship_rect.y <= 0:
           spaceship_rect.y = spaceship_rect.y + 5
        if spaceship_rect.y >=550:
            spaceship_rect.y = spaceship_rect.y - 5

        # 3. Process user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            ##### Processing User Input #####
            elif event.type == KEYDOWN and event.key == K_UP or \
                 event.type == KEYUP   and event.key == K_DOWN:
                spaceship_vy = spaceship_vy - spaceshipvelocity
            elif event.type == KEYDOWN and event.key == K_DOWN or \
                 event.type == KEYUP   and event.key == K_UP:
                spaceship_vy = spaceship_vy + spaceshipvelocity
            elif event.type == KEYDOWN and event.key == K_r:
                gameover == False
                main()
            elif event.type == KEYDOWN and event.key == K_SPACE:
		while True:
                    bullets.add(Bullet(xpos, ypos + 18))
        # 4. Delay (for a fixed time)
        pygame.display.flip()
        clock.tick(FPS)
        pass
if __name__ == '__main__':
    main()


#When right side of asteroid comes in contact with left axis, make it disappear

    
###### ####### ########
    
