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
		global soldierMasterImg, enemyMasterImg, clock, bulletMasterImg
		clock = pygame.time.Clock()
		soldierMasterImg = pygame.transform.rotozoom(pygame.image.load('data/soldier.png').convert_alpha(), 10, 0.2)
		enemyMasterImg = pygame.transform.rotozoom(pygame.image.load('data/enemy.png').convert_alpha(), 10, 0.2)
		bulletMasterImg = pygame.transform.rotozoom(pygame.image.load('data/bullet.png').convert_alpha(), 10, 0.1)
		
	def loadSprites(self):
		self.soldier = Soldier(100)
		#self.zombie = Enemy(10, [self.width, self.height], 10)
		self.bullet = 0
		
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
			if keys[pygame.K_SPACE]:
				self.bullet = Bullet(self.soldier.angle, self.soldier.rect)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			self.screen.fill((100,180,180))
			self.screen.blit(self.soldier.image, self.soldier.rect)
			if (self.bullet.has()):
				self.bullet.update()
				self.bullet.draw(self.screen)
			pygame.display.flip()
			clock.tick(60)
					

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
		
	def calcPointList(self, x, y):
		self.points = [[x, y+10],[x-5,y-5],[x+5,y-5]] 
		
	def findVector(self, pos):
		y = (self.pos[1] - pos[1])
		x = (self.pos[0] - pos[0])
		if(y == 0):
			y = .01
		if(x == 0):
			x = .01
		angle = math.atan(x/y)
		if(x>0 and y>0 or x<0 and y>0):
			angle += math.pi
		xDir = x/abs(x) * .5
		yDir = y/abs(y) * .5
		if(y<2 and y>-2):
			yDir = 0
		if(x<2 and x>-2):
			xDir = 0
		return [xDir,yDir,angle]
		#FINISH

		
class Bullet(pygame.sprite.Sprite):
	def __init__(self, angle, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = bulletMasterImg
		self.angle = angle
		self.rect = [pos[0] - math.cos(self.angle*math.pi/180)*25 + 15, pos[1] + math.sin(self.angle*math.pi/180)*25 + 15] # implement circle formula
		
	def updatePos(self):
		self.x = math.cos(self.angle*math.pi/180 + math.pi) * 2.5
		self.y = math.sin(self.angle*math.pi/180 + math.pi) * 2.5
		self.image = pygame.transform.rotozoom(bulletMasterImg, self.angle + 180, 1)
		self.rect = [self.rect[0] + self.x, self.rect[1] - self.y]
		if (self.rect[0] > 640 or self.rect[0] < 0 and self.rect[1] > 480 or self.rect[1] < 0):
			self.kill()
		
if __name__ == "__main__":
	MainWindow = ShooterMain()
	MainWindow.mainLoop()