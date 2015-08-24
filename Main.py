import sys
sys.path.insert(1, "C:\Users\khunyingimig\Downloads\Lib\site-packages")
import pygame

from pygame.locals import *

pygame.init()
from pygame.locals import *
from util import *
import time

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

    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        # need something like this.
        self.height_ratio = 10. / float(height)
        print "self_height_ratio", self.height_ratio
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
        pygame.draw.line(self.screen, (0, 100,100), (0,400), (640, 400), 4)
    def MainLoop(self):
        """Load All of our Sprites"""
        self.LoadSprites();
        """This is the Main Loop of the Game"""
        while 1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if (event.key == K_UP):
                        self.rocket.accel = -3.14
                    if (event.key == K_DOWN):
                        self.rocket.accel = 3.14
                    if (event.key == K_LEFT):
                        self.rocket.image = rot_center(self.rocket.image, -5)
                    if (event.key == K_RIGHT):
                        self.rocket.image = rot_center(self.rocket.image, 5)

                if event.type == KEYUP:
                    self.rocket.accel = 1.62

            self.rocket.fall()
            BLACK = (0,0,0)
            self.screen.fill(BLACK)
            self.rocket_sprites.draw(self.screen)
            pygame.draw.line(self.screen, (0, 100,100), \
                (0, int(7.5/self.height_ratio)), (640, int(7.5/self.height_ratio)), 4)
            pygame.display.flip()

    def LoadSprites(self):
        """Load the sprites that we need"""
        self.rocket = Rocket()
        self.rocket_sprites = pygame.sprite.RenderPlain((self.rocket))

class Rocket(pygame.sprite.Sprite):
    """This is our rocket that will move around the screen"""

    def __init__(self, height_ratio=0.020833):
        pygame.sprite.Sprite.__init__(self)
        self.height_ratio = height_ratio
        self.image, self.rect = load_image('rocketup.jpg',-1)
        width_ratio = 40. / self.image.get_width()
        self.image = pygame.transform.scale(self.image, \
            (int(width_ratio * self.image.get_width()),  \
             int(width_ratio * self.image.get_height())))
        self.rect = self.image.get_rect()
        self.rect.move_ip(300, int(2./self.height_ratio));
        self.height = 10.
        self.time = time.time()
        self.speed = 0.1
        self.accel = 1.62
        print self.rect
        print self.height_ratio
    def fall(self):
        # print self.rect.bottom, 7.5/self.height_ratio
        if self.rect.bottom > 7.5/self.height_ratio:
            if self.speed < 3:
                self.image.fill((0,200,0))
            else:
                self.image.fill((200,0,0))
            return
        curr_time = time.time()
        seconds_elapsed = curr_time - self.time
        self.time = curr_time
        self.height -= self.speed * seconds_elapsed
        self.speed += self.accel * seconds_elapsed
        print seconds_elapsed, self.speed, self.height
        self.rect.move_ip(0, int(self.speed * seconds_elapsed / self.height_ratio))


if __name__ == "__main__":
    print os.getcwd()
    MainWindow = PyManMain()
    MainWindow.MainLoop()
