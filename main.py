import time
import os
import random
import pygame
import neat

WIN_WIDTH = 500
WIN_HEIGHT = 800


def get_img_path(img_name):
    return os.path.join("imgs", img_name)


def load_image(img_name):
    pygame.transform.scale2x(pygame.image.load(get_img_path(img_name)))


birds_imgs = ["bird1.png", "bird2.png", "bird3.png"]
base_img_name = "base.png"
bg_img_name = "bg.png"
pipe_img_name = "pipe.png"

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(get_img_path(img))) for img in birds_imgs]
BASE_IMG = load_image(base_img_name)
BG_IMG = pygame.transform.scale2x(pygame.image.load(get_img_path(bg_img_name)))
# BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")))
PIPE_IMG = load_image(pipe_img_name)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_cnt = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16
        if (d < 0):
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt >= -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_cnt += 1
        if self.img_cnt < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_cnt < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_cnt < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_cnt < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_cnt == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_cnt = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_cnt = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win=win, bird=bird)

    pygame.quit()
    quit()


main()