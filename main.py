import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

run_ani_R = [pygame.image.load("img/Player_Sprite_R.png"), pygame.image.load("img/Player_Sprite2_R.png"),
             pygame.image.load("img/Player_Sprite3_R.png"),pygame.image.load("img/Player_Sprite4_R.png"),
             pygame.image.load("img/Player_Sprite5_R.png"),pygame.image.load("img/Player_Sprite6_R.png"),
             pygame.image.load("img/Player_Sprite_R.png")]
 
# Run animation for the LEFT
run_ani_L = [pygame.image.load("img/Player_Sprite_L.png"), pygame.image.load("img/Player_Sprite2_L.png"),
             pygame.image.load("img/Player_Sprite3_L.png"),pygame.image.load("img/Player_Sprite4_L.png"),
             pygame.image.load("img/Player_Sprite5_L.png"),pygame.image.load("img/Player_Sprite6_L.png"),
             pygame.image.load("img/Player_Sprite_L.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("img/Player_Sprite_R.png"), pygame.image.load("img/Player_Attack_R.png"),
                pygame.image.load("img/Player_Attack2_R.png"),pygame.image.load("img/Player_Attack2_R.png"),
                pygame.image.load("img/Player_Attack3_R.png"),pygame.image.load("img/Player_Attack3_R.png"),
                pygame.image.load("img/Player_Attack4_R.png"),pygame.image.load("img/Player_Attack4_R.png"),
                pygame.image.load("img/Player_Attack5_R.png"),pygame.image.load("img/Player_Attack5_R.png"),
                pygame.image.load("img/Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("img/Player_Sprite_L.png"), pygame.image.load("img/Player_Attack_L.png"),
                pygame.image.load("img/Player_Attack2_L.png"),pygame.image.load("img/Player_Attack2_L.png"),
                pygame.image.load("img/Player_Attack3_L.png"),pygame.image.load("img/Player_Attack3_L.png"),
                pygame.image.load("img/Player_Attack4_L.png"),pygame.image.load("img/Player_Attack4_L.png"),
                pygame.image.load("img/Player_Attack5_L.png"),pygame.image.load("img/Player_Attack5_L.png"),
                pygame.image.load("img/Player_Sprite_L.png")]

class Background(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.bg = pygame.image.load('img/Background.png')
    self.bgY = 0
    self.bgX = 0

  def render(self):
    screen.blit(self.bg, (self.bgX, self.bgY))

class Ground(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load('img/Ground.png')
    self.rect = self.image.get_rect(center = (350, 350))
  
  def render(self):
    screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load('img/Player_Sprite_R.png')
    self.rect = self.image.get_rect()
    self.jumping = False
    self.running = False
    self.move_frame = 0
    self.attacking = False
    self.attack_frame = 0

      # position and direction
    self.vx = 0
    self.pos = vec((340, 240))
    self.vel = vec(0,0)
    self.acc = vec(0,0)
    self.direction = "RIGHT"

  def move(self):
    self.acc = vec(0, 0.5)

    if abs(self.vel.x) > 0.3:
      self.running = True
    else:
      self.running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
      self.acc.x = -ACC
    elif keys[pygame.K_RIGHT]:
      self.acc.x = ACC

    # formula for calculation velocity while accounting for friction
    self.acc.x += self.vel.x * FRIC
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc # updates positions with new values

    if self.pos.x > WIDTH:
      self.pos.x = 0
    if self.pos.x < 0:
      self.pos.x = WIDTH

    self.rect.midbottom = self.pos # update rect with new position

  def gravity_check(self):
    hits = pygame.sprite.spritecollide(player, ground_group, False)
    if self.vel.y > 0:
      if hits:
        lowest = hits[0]
        if self.pos.y < lowest.rect.bottom:
          self.pos.y = lowest.rect.top + 1
          self.vel.y = 0
          self.jumping = False
          

  def update(self):
    if self.move_frame > 6:
      self.move_frame = 0
      return

    if self.jumping == False and self.running == True:
      if self.vel.x > 0:
        self.image = run_ani_R[self.move_frame]
        self.direction = 'RIGHT'
      else:
        self.image = run_ani_L[self.move_frame]
        self.direction = 'LEFT'
      self.move_frame += 1

      if abs(self.vel.x) < 0.2 and self.move_frame != 0:
        self.move_frame = 0
        if self.direction == 'RIGHT':
          self.image = run_ani_R[self.move_frame]
        elif self.direction == 'LEFT':
          self.image = run_ani_L[self.move_frame]

  def attack(self):
    if self.attack_frame > 10:
      self.attack_frame = 0
      self.attacking = False

    if self.direction == 'RIGHT':
      self.image = attack_ani_R[self.attack_frame]
    elif self.direction == 'LEFT':
      self.correction()
      self.image = attack_ani_L[self.attack_frame]
    
    self.attack_frame += 1

  def jump(self):
    # self.rect.x += 1
    self.rect.x += 1
 
    # Check to see if payer is in contact with the ground
    hits = pygame.sprite.spritecollide(self, ground_group, False)
         
    self.rect.x -= 1
 
    # If touching the ground, and not currently jumping, cause the player to jump.
    if hits and not self.jumping:
      self.jumping = True
      self.vel.y = -12

  def correction(self):
    if self.attack_frame == 1:
      self.pos.x -= 20
    if self.attack_frame == 10:
      self.pos.x += 20

class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load('img/Enemy.png')
    self.rect = self.image.get_rect()
    self.pos = vec(0,0)
    self.vel = vec(0,0)

    self.direction = random.randint(0,1)
    self.vel.x = random.randint(2,6) / 2

    if self.direction == 0:
      self.pos.x = 0
      self.pos.y = 235
    if self.direction == 1:
      self.pos.x = 700
      self.pos.y = 235
  
  def move(self):
    if self.pos.x >= (WIDTH-20):
      self.direction = 1
    elif self.pos.x <= 0:
      self.direction = 0

    if self.direction == 0:
      self.pos.x += self.vel.x
    if self.direction == 1:
      self.pos.x -= self.vel.x

    self.rect.center = self.pos
  
  def render(self):
    screen.blit(self.image, (self.pos.x, self.pos.y))

pygame.init()

# main game logic variables
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.7
FRIC = -0.10
FPS = 60
clock = pygame.time.Clock()
COUNT = 0

# creating the screen and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mini RPG by Jameson Creevey')

# instatiating all classes
background = Background()

ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

player = Player()
enemy = Enemy()

while True:
  player.gravity_check()  

  # if user clicks the X, close window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
      pass

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        player.jump()
      if event.key == pygame.K_RETURN:
        if player.attacking == False:
          player.attack()
          player.attacking = True

  player.update()
  if player.attacking == True:
    player.attack()
  player.move()

  # rendering everything on screen
  background.render()
  ground.render()

  screen.blit(player.image, player.rect)
  enemy.render()

  pygame.display.flip()
  clock.tick(FPS)