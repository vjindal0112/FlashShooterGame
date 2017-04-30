import os, sys
import pygame
from pygame.locals import *
import math
import random
from itertools import chain
#from helpers import *

class ShooterMain:
	def __init__(self, width=640,height=480):
		pygame.init()
		"""Set the window Size"""
		self.width = width
		self.height = height
		"""Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))
		global soldierMasterImg, enemyMasterImg, clock, bulletMasterImg, myfont
		clock = pygame.time.Clock()
		myfont = pygame.font.SysFont("monospace", 15)
		soldierMasterImg = pygame.transform.rotozoom(pygame.image.load('data/soldier.png').convert_alpha(), 10, 0.2)
		enemyMasterImg = pygame.transform.rotozoom(pygame.image.load('data/enemy.png').convert_alpha(), 10, 0.2)
		bulletMasterImg = pygame.transform.rotozoom(pygame.image.load('data/bullet.png').convert_alpha(), 10, 0.1)
		
	def loadSprites(self):
		self.soldier = Soldier(100)
		self.enemy = Enemy(10, [self.width, self.height], 10)
		self.bullet = pygame.sprite.Group()
		
	def mainLoop(self):
		self.loadSprites()
		while 1:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				self.soldier.rotate(-2)
			if keys[pygame.K_RIGHT]:
				self.soldier.rotate(2)
			if keys[pygame.K_UP]:
				self.soldier.moveForward(2)
			if keys[pygame.K_DOWN]:
				self.soldier.moveBackward(.8)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == K_SPACE:
						self.bullet.add(Bullet(self.soldier.angle, self.soldier.rect))
				if event.type == pygame.QUIT:
					sys.exit()
			self.screen.fill((100,180,180))
			self.screen.blit(self.soldier.image, self.soldier.rect)
			self.enemy.updatePos(self.soldier.findVector(self.enemy.enemyPos))
			self.screen.blit(self.enemy.image, self.enemy.rect)
			#if(self.bullet.has()):
			self.bullet.update()
			self.bullet.draw(self.screen)
			label = myfont.render("HELLO", 1, (255,255,0))
			self.screen.blit(label, (100, 100))
			pygame.display.flip()
			clock.tick(70)
					

class Soldier(pygame.sprite.Sprite):
	def __init__(self, health):
		pygame.sprite.Sprite.__init__(self)
		self.pos = [200,200]
		self.points = [[10,20],[5,10],[15,10]]
		self.health = health
		self.angle = 180
		self.image = soldierMasterImg
		self.rect = self.pos
		
	def wasShot(self, healthSubtraction):
		self.health -= healthSubtraction
	
	def getHealth(self):
		return self.health
		
	def rotate(self, speed):
		self.angle -= speed
		self.image = pygame.transform.rotozoom(soldierMasterImg, self.angle - 180, 1)
		
	def moveForward(self, forwardDiff):
		self.pos = [self.pos[0] - (math.cos(self.angle*math.pi/180) * forwardDiff), self.pos[1] + (math.sin(self.angle*math.pi/180) * forwardDiff)]
		self.rect = self.pos
		
	def moveBackward(self, forwardDiff):
		self.pos = [self.pos[0] + (math.cos(self.angle*math.pi/180) * forwardDiff), self.pos[1] - (math.sin(self.angle*math.pi/180) * forwardDiff)]
		self.rect = self.pos
		
	def calcPointList(self, x, y):
		self.points = [[x, y+10],[x-5,y-5],[x+5,y-5]] 
		
	def findVector(self, pos):
		ydiff = (self.pos[1] - pos[1])
		xdiff = (self.pos[0] - pos[0])
		if(ydiff == 0):
			ydiff = .01
		if(xdiff == 0):
			xdiff = .01
		angle = math.atan(xdiff/ydiff)
		if(xdiff>0 and ydiff>0 or xdiff<0 and ydiff>0):
			angle += math.pi
		xDir = xdiff/abs(xdiff) * .5
		yDir = ydiff/abs(ydiff) * .5
		if(ydiff<2 and ydiff>-2):
			yDir = 0
		if(xdiff<2 and xdiff>-2):
			xDir = 0
		return [xDir,yDir,angle]
		#FINISH
	
class Enemy(pygame.sprite.Sprite):
	def __init__(self, health, screenDim, angle):
		pygame.sprite.Sprite.__init__(self)
		self.angle = angle
		self.image = enemyMasterImg
		self.health = health
		self.screenDim = screenDim
		xrange = [i for j in (range(-10,0), range(self.screenDim[0],self.screenDim[0]+10)) for i in j]
		yrange = [i for j in (range(-10,0), range(self.screenDim[1],self.screenDim[1]+10)) for i in j]
		self.enemyPos = [random.choice(xrange), random.choice(yrange)] 
		self.rect = self.enemyPos
	
	def updatePos(self, vector):
		self.enemyPos = [self.enemyPos[0] + vector[0] * 1.3, self.enemyPos[1] + vector[1] * 1.3]
		self.angle = vector[2]*180/math.pi
		self.image = pygame.transform.rotozoom(enemyMasterImg, self.angle + 45, 1)
		self.rect = self.enemyPos
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self, angle, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bulletMasterImg
		self.angle = angle
		self.rect = [pos[0] - math.cos(self.angle*math.pi/180)*30 + 12, pos[1] + math.sin(self.angle*math.pi/180)*25 + 10] # implemented circle formula
		
	def update(self):
		self.x = math.cos((self.angle+6)*math.pi/180 + math.pi) * 2.5
		self.y = math.sin((self.angle+6)*math.pi/180 + math.pi) * 2.5
		self.image = pygame.transform.rotozoom(bulletMasterImg, self.angle + 180, 1)
		self.rect = [self.rect[0] + self.x, self.rect[1] - self.y]
		if (self.rect[0] > 640 or self.rect[0] < 0 or self.rect[1] > 480 or self.rect[1] < 0):
			self.kill()
		
if __name__ == "__main__":
	MainWindow = ShooterMain()
	MainWindow.mainLoop()