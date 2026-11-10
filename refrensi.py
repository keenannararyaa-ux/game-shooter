from pygame import *

win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"),(win_width,win_height))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
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
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed     
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 65:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x == 470:
            self.direction = 'right'
        if self.rect.x == win_width - 80:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        if self.direction == 'right':
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self,color,x,y,width,height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface((self.width,self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x,self.rect.y))        


packman = Player('hero.png',5,win_height - 80,4)
monster = Enemy("cyborg.png",win_width - 80,280,2)
final = GameSprite('treasure.png',win_width - 110,win_height- 80,0 )

w1 = Wall((75,255,118),100,20,10,340)
w2 = Wall((75,255,118),100,20,450,10)
w3 = Wall((75,255,118),100,480,450,10)
w4 = Wall((75,255,118),220,120,10,370)
w5 = Wall((75,255,118),350,20,10,370)
w6 = Wall((75,255,118),470,120,10,370)

font.init()
font = font.Font(None, 70)

 

mixer.init()
mixer.music.load('jungles.ogg')
#mixer.music.play()

sound_win = mixer.Sound('money.ogg')
sound_lose = mixer.Sound('kick.ogg')
finish = False
run = True
fps = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if finish != True:
        window.blit(background,(0,0))
        packman.update()
        packman.reset()
        monster.update()
        monster.reset()
        final.reset()
        w1.draw()
        w2.draw()
        w3.draw()
        w4.draw()
        w5.draw()
        w6.draw()

        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(text_win, (200,200))
            sound_win.play()

        if (sprite.collide_rect(packman, monster) or 
            sprite.collide_rect(packman, w1) or 
            sprite.collide_rect(packman, w2) or 
            sprite.collide_rect(packman, w3) or            
            sprite.collide_rect(packman, w4) or 
            sprite.collide_rect(packman, w5) or 
            sprite.collide_rect(packman, w6) ):
            finish = True
            window.blit(text_lose, (200,200))
            sound_lose.play()

    display.update()
    fps.tick(60)