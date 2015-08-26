import sys
sys.path.insert(1, "C:\Users\khunyingimig\Downloads\Lib\site-packages")
import pygame
import math

from pygame.locals import *

pygame.init()
from pygame.locals import *
from util import *
import time

ACCELERATION_DUE_TO_THRUST = -3.07
ACCELERATION_DUE_TO_GRAVITY = 0.35
INITIAL_VERTICAL_SPEED = 3
HORIZONTAL_SPEED_MULTIPLIER = 1.

INITIAL_SCREEN_WIDTH = 1024
INITIAL_SCREEN_HEIGHT = int(1024 / 1.62) # Golden mean

MAX_HEIGHT = 10.

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self, width=INITIAL_SCREEN_WIDTH,height=INITIAL_SCREEN_HEIGHT):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        # need something like this.
        self.height_ratio = MAX_HEIGHT / float(height)
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
	self.ground = self.height - 20
        pygame.draw.line(self.screen, (0, 100,100), (0, self.ground), (height, self.ground), 4)

    def MainLoop(self):
        """Load All of our Sprites"""
        self.LoadSprites();
        """This is the Main Loop of the Game"""
        while 1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
		    print event.key
		    if (event.key == 114 and self.rocket.landed):
			self.LoadSprites()
			continue
                    if (event.key == K_UP):
                        if self.rocket.xaccel == 0:
				self.rocket.accel = ACCELERATION_DUE_TO_THRUST
                        self.rocket.xspeed += self.rocket.xaccel * HORIZONTAL_SPEED_MULTIPLIER
                        print "xspeed", self.rocket.xspeed
                    if (event.key == K_DOWN):
                        self.rocket.accel = ACCELERATION_DUE_TO_GRAVITY
                    if (event.key == K_LEFT):
			if self.rocket.rotation > -90:
				self.rocket.rotation -= 90
				self.rocket.xaccel -= 1
                    if (event.key == K_RIGHT):
                        if self.rocket.rotation < 90:
				self.rocket.rotation += 90
                        	self.rocket.xaccel += 1
                if event.type == KEYUP:
                    self.rocket.accel = ACCELERATION_DUE_TO_GRAVITY

            self.rocket.fall()
            BLACK = (0,0,0)
            self.screen.fill(BLACK)
            self.rocket_sprites.draw(self.screen)
            pygame.draw.line(self.screen, (0, 100,100), \
                (0, self.height - 40), (self.width, self.height - 40), 4)
            pygame.display.flip()

    def LoadSprites(self):
        """Load the sprites that we need"""
        self.rocket = Rocket(self.ground, self.height_ratio)
        self.rocket_sprites = pygame.sprite.RenderPlain((self.rocket))

class Rocket(pygame.sprite.Sprite):
    """This is our rocket that will move around the screen"""

    def __init__(self, ground = 462, height_ratio=1):
        pygame.sprite.Sprite.__init__(self)
        self.height_ratio = height_ratio
        self.image, self.rect = load_image('rocketup.png',-1)
        #width_ratio = 40. / self.image.get_width()
        #self.image = pygame.transform.scale(self.image, \
        #    (int(width_ratio * self.image.get_width()),  \
        #     int(width_ratio * self.image.get_height())))
        self.rect = self.image.get_rect()
        self.rect.move_ip(300, int(2./self.height_ratio));
        self.height = MAX_HEIGHT
        self.time = time.time()
        self.speed = INITIAL_VERTICAL_SPEED
        self.accel = ACCELERATION_DUE_TO_GRAVITY
        self.rotation = 0
        self.xaccel = 0
        self.xspeed = 0
	self.ground = ground
        print self.rect
        print self.height_ratio
	self.landed = False

    def fall(self):
        # print self.rect.bottom, 7.5/self.height_ratio
        if self.rect.bottom > self.ground:
            if self.speed < 3:
                self.image.fill((0,200,0))
		self.landed = True
            else:
                self.image.fill((200,0,0))
		self.landed = True
            return

        curr_time = time.time()
        seconds_elapsed = curr_time - self.time
        self.time = curr_time
        self.height -= self.speed * seconds_elapsed
	if self.height > MAX_HEIGHT:
		self.height = MAX_HEIGHT
        self.speed += self.accel * seconds_elapsed

	if self.rotation == -90:
		self.image = load_image('rocketleft.png', -1)[0]

	elif self.rotation == 0:
		self.image = load_image('rocketup.png', -1)[0]
	elif self.rotation == 90:
		self.image = load_image('rocketright.png', -1)[0]
        self.rect.move_ip(0, int(self.speed * seconds_elapsed / self.height_ratio))
        self.rect.move_ip(int(self.xspeed * seconds_elapsed / self.height_ratio), 0)

if __name__ == "__main__":
    print os.getcwd()
    MainWindow = PyManMain()
    MainWindow.MainLoop()
