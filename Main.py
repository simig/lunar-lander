import sys
sys.path.insert(1, "C:\Users\khunyingimig\Downloads\Lib\site-packages")
import pygame
import math
import string

from pygame.locals import *

pygame.init()
from pygame.locals import *
from util import *
import time

#pygame.mixer.init()
#pygame.mixer.music.load("data\music.mp3")
#pygame.mixer.music.play()

GROUND_COLLISION_TOLERANCE = 5

ACCELERATION_DUE_TO_THRUST = -3.07
ACCELERATION_DUE_TO_GRAVITY = 1.6
INITIAL_VERTICAL_SPEED = 3
INITIAL_HORIZONTAL_SPEED = 0.01
HORIZONTAL_SPEED_MULTIPLIER = 0.01

INITIAL_SCREEN_WIDTH = 1024
INITIAL_SCREEN_HEIGHT = int(1024 / 1.62) # Golden mean

INITIAL_FUEL = 100

MAX_HEIGHT = 10.

LH_ALTITUDE = 120
RH_ALTITUDE = 90

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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

#BEGINNER
        #self.ground = [(100, 200, 30), (540, 640, 90), (700, 850, 40), (900,1000, 20)]
        #self.ground = [(100, 200, 180), (540, 640, 0), (700, 850, 120), (900,1000, 100)]
        self.ground =[(200, 200, 550), (400, 480, 20), (900, 900, 550)]
    def MainLoop(self):
        """Load All of our Sprites"""
        self.LoadSprites();
        """This is the Main Loop of the Game"""

        cyan_landing_value = 200
        min_value_for_landing_cyan = 200
        max_value_for_landing_cyan = 255
        cyan_change = 10

        while 1:
            keys = pygame.key.get_pressed()

            if (keys[113]):
                        sys.exit()
            if (keys[114] and self.rocket.landed):
                        self.LoadSprites()
                        continue
            if (keys[K_UP] and self.rocket.fuel > 0):
                        self.rocket.fuel -= 1
                        if self.rocket.fuel < 0:
                                self.rocket.fuel = 0
                        else:

				self.rocket.thrust_level += 1
				if self.rocket.thrust_level > 3:
					self.rocket.thrust_level = 3
                                if self.rocket.xaccel == 0:
                                        self.rocket.accel = self.rocket.thrust_level * ACCELERATION_DUE_TO_THRUST
                                self.rocket.xspeed += self.rocket.thrust_level * self.rocket.xaccel * HORIZONTAL_SPEED_MULTIPLIER
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RIGHT:
                        if self.rocket.rotation < 90:
                                self.rocket.rotation += 90
                                self.rocket.xaccel += 1
                                print "self.rocket.rotation", self.rocket.rotation
                    if event.key == K_LEFT:
                        if self.rocket.rotation > -90:
                                self.rocket.rotation -= 90
                                self.rocket.xaccel -= 1
                                print "self.rocket.rotation", self.rocket.rotation
                if event.type == pygame.KEYUP:
                    #self.rocket.xaccel = 0.
                    self.rocket.thrust_level = 0
                    self.rocket.accel = ACCELERATION_DUE_TO_GRAVITY

            self.rocket.fall()
            COLOR = (25,120,120)
            self.screen.fill(COLOR)
            self.rocket_sprites.draw(self.screen)
            # Start drawing line
            curr = (0, self.height - LH_ALTITUDE)


            cyan_landing_value += cyan_change
            if cyan_landing_value > max_value_for_landing_cyan \
                or cyan_landing_value < min_value_for_landing_cyan:
                cyan_change = - cyan_change
                cyan_landing_value += cyan_change
            cyan = (0, 100, 100)
            cyan2 = (0, cyan_landing_value, cyan_landing_value)
            
		for t in self.ground:
                pygame.draw.line(self.screen, cyan, \
                    curr, (t[0], self.height - t[2]), 4)
                pygame.draw.line(self.screen, cyan2, \
                    (t[0], self.height - t[2]), (t[1], self.height - t[2]), 4)
                curr = (t[1], self.height - t[2])
            pygame.draw.line(self.screen, cyan, curr, (self.width, self.height - RH_ALTITUDE))

            font = pygame.font.Font(None, 36)
            text = font.render("Fuel: " + str(self.rocket.fuel), 1, (0, 255, 128))

            textpos = text.get_rect()
            textpos.topleft = self.screen.get_rect().topleft
            self.screen.blit(text, textpos)

            text = font.render("Height: " + "{:.2f}".format(self.rocket.height), 1, (0, 255, 128))
            textpos.topleft = self.screen.get_rect().topleft
            textpos.top += 20
            self.screen.blit(text, textpos)

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
        self.xpos = height_ratio * 300.
        self.height = MAX_HEIGHT
        self.time = time.time()
        self.speed = INITIAL_VERTICAL_SPEED
	self.xspeed = INITIAL_HORIZONTAL_SPEED
        self.accel = ACCELERATION_DUE_TO_GRAVITY
        self.rotation = 0
        self.xaccel = 0
        self.ground = ground
        self.landed = False
        self.fuel = INITIAL_FUEL
	self.thrust_level = 0

    def point_below_line(self,pointx, pointy, ax, ay, bx, by):
        slope = float(by - ay) / float(bx - ax)
        intercept = ay - ax * slope

        if (pointx < ax or pointx > bx):
             #print ax, pointx, bx, "not in interval"
            return False
        ret = pointx * slope + intercept > pointy
        #print pointx, pointy, (pointx * slope + intercept), ret
        return ret

    def fall(self):
        #print self.rect.bottom
        altitude = INITIAL_SCREEN_HEIGHT - self.rect.bottom


        curr = (0, LH_ALTITUDE)
        x1 = self.rect.left
        y1 = altitude
        x2 = self.rect.right
        y2 = altitude

        #print x1, y1, x2, y2, self.ground


        #TODO: HANDLE CASE WHERE ROCKET IS HALF-ON A PLATFORM.

        for t in self.ground:
                if self.point_below_line(x1, y1 + GROUND_COLLISION_TOLERANCE, curr[0], curr[1], t[0], t[2]) \
                    or self.point_below_line(x2, y2 + GROUND_COLLISION_TOLERANCE, curr[0], curr[1], t[0], t[2]):
                        self.image = load_image('Crashed.png', -1)[0]
                        self.landed = True
                        return
                if x1 > t[0] and x2 < t[1] \
                    and self.point_below_line(x1, y1, t[0], t[2], t[1], t[2]):

                    if self.speed < 3 and self.rotation == 0:
                        self.image.fill((0,200,0))
                        self.landed = True
                    else:
                        self.image = load_image('Crashed.png', -1)[0]
                        self.landed = True
                    return
                curr = (t[1], t[2])


        # TODO: Handle final hill on right of screen.




        curr_time = time.time()
        seconds_elapsed = curr_time - self.time
        self.time = curr_time
        self.height -= self.speed * seconds_elapsed
        if self.height > MAX_HEIGHT:
            self.height = MAX_HEIGHT
            self.speed = -self.speed
            self.accel = ACCELERATION_DUE_TO_GRAVITY
        if self.xpos <= 0:
            self.xpos = 0
            self.xspeed = -self.xspeed
        if self.xpos >= INITIAL_SCREEN_WIDTH * self.height_ratio:
            print "boundary", self.xpos
            self.xpos = (INITIAL_SCREEN_WIDTH ) * self.height_ratio
            self.xspeed = -self.xspeed
        self.speed += self.accel * seconds_elapsed
        self.xpos += self.xspeed
        #print "xpos", self.xpos


	t = "" if self.thrust_level == 0 else "thrust" + str(self.thrust_level)

        if self.rotation == -90:
            self.image = load_image('rocketleft' + t + '.png', -1)[0]

        elif self.rotation == 0:
            self.image = load_image('rocketup' + t + '.png', -1)[0]
        elif self.rotation == 90:
            self.image = load_image('rocketright' + t + '.png', -1)[0]
        # TODO: Remove INITIAL_SCREEN_HEIGHT
        self.rect.top = INITIAL_SCREEN_HEIGHT - self.height / self.height_ratio
        self.rect.left = self.xpos / self.height_ratio
        #print self.height, self.rect.bottom, self.height / self.height_ratio
        #self.rect.move_ip(int(self.xspeed * seconds_elapsed / self.height_ratio), 0)

if __name__ == "__main__":
    print os.getcwd()
    MainWindow = PyManMain()
    MainWindow.MainLoop()
