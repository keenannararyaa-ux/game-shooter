#Create your own shooter
from pygame import *
from random import *
import time as tm

win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 85 :
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0

ship = Player('rocket.png',5,win_height - 100,80,100,10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(80,win_width-80),-40,80,50,randint(1,2))
    asteroids.add(asteroid)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
#mixer_music.play()

sound_fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)

text_win = font2.render( 'YOU WIN!', True,(0,255,0))
text_lose = font2.render('YOU LOSE!', True,(255,0,0))

score = 0
lost = 0
lives = 3
color_live = (0,255,0)
num_fire = 0
rel_time = False

finish = False
run = True
fps = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    sound_fire.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False: 
                    last_time = tm.time()
                    rel_time = True
                    
    if finish != True:
        window.blit(background,(0,0))    
        text_score = font1.render('Score: '+ str(score),True,(255,255,255))
        text_miss = font1.render('Missed: '+ str(lost),True,(255,255,255))

        if rel_time == True:
            now_time = tm.time()

            if now_time - last_time < 1:
                reload = font2.render('Wait, reload...',1,(150,0,0))
                window.blit(reload,(200,400))
            else:
                num_fire = 0
                rel_time = False

        window.blit(text_score,(10,20))
        window.blit(text_miss,(10,50))

        collides = sprite.groupcollide(monsters, bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80,win_width - 80),-40,80,50,randint(1,5))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets,False,True)

        if score == 10:
            finish = True
            window.blit(text_win,(225,200))
        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            lives -= 1

        text_lives = font2.render(str(lives),True,color_live)
        window.blit(text_lives,(650,10))     

        if lost >= 3 or lives == 0:
            finish = True
            window.blit(text_lose,(225,200))

        if lives >= 3:
            color_live = (0,255,0)
        if lives == 2:
            color_live = (186, 177, 177)
        if lives == 1:
            color_live = (255,0,0)

        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
    else:
        score = 0
        lost = 0
        lives = 3
        for b in bullets:
            b.kill()
        for b in monsters:
            b.kill()
        for b in asteroids:
            b.kill()        
        finish = False
        tm.sleep(3)  
        for i in range(5):
            monster = Enemy('ufo.png',randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)    
        for i in range(3):
            asteroid = Asteroid('asteroid.png',randint(80,win_width-80),-40,80,50,randint(1,2))
            asteroids.add(asteroid)
        
    display.update()
    fps.tick(60)
