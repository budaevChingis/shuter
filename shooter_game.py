#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer 
font.init()

font1 = font.SysFont('Times New Roman', 24)
font2 = font.SysFont('Courier New', 60)
win = font2.render('YOU WIN', True, (255, 255, 0))
lose = font2.render('YOU LOSE', True, (255, 0, 0))

times = font1.render('перезарядка', True, (255, 0, 0))

scor = 0

window = display.set_mode((700, 500))
display.set_caption('ШУТЕР')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
    def resat(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def update(self):
        kays = key.get_pressed()
        if kays[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if kays[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 5, 15)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 630)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y < 0:
            self.kill()

class Asteroids(GameSprite):
     def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 630)


monsters = sprite.Group()
bullets = sprite.Group()
asterods = sprite.Group()


hero = Player('rocket.png', 300, 400, 10, 60, 100)
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 630), 0, randint(1,2), 70, 50 )
    monsters.add(enemy)

for i in range(2):
    asteroid = Asteroids('asteroid.png', randint(0, 630), 0, 3, 50, 50)
    asterods.add(asteroid)

num_fire = 0

health = 0

rel_time = False
finish = False
game = True
while game :
    for e in event.get():
        if e.type == QUIT:
            game = False
       
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time != True:
                    hero.fire()
                    num_fire += 1
                if num_fire >= 5:
                    rel_time = True
                    time1 = timer()
                   
    if finish != True:
        window.blit(background, (0, 0))
        hero.update()
        hero.resat()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asterods.update()
        asterods.draw(window)
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))
        text_scor= font1.render('Счет: ' + str(scor) , 1, (255, 255, 255))
        window.blit(text_scor, (10, 10))

    

        sprites_list = sprite.spritecollide(hero, monsters, False)
        asteroids = 0
        asteroids = sprite.spritecollide(hero, asterods, False)
        if len(asteroids) >0:
            finish = True
            window.blit(lose, (235, 200))


        if rel_time == True:
            time2 = timer()
            if time2 - time1 > 3:        
                num_fire = 0
                rel_time = False
            else:
                window.blit(times, (300, 400))

        if len(sprites_list) > 0 or lost > 10:
            finish = True
            window.blit(lose, (235, 200))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            scor = scor + 1
            enemy = Enemy('ufo.png', randint(0, 630), 0, randint(2, 4), 70, 50 ) 
            monsters.add(enemy)
        if scor > 9:
            finish = True
            window.blit(win, (235, 200))
        



           
           
            

    
    
    

    clock.tick(FPS)
    display.update()
