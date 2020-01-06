import time
import os
import random
import pygame
import neat

# initialization
pygame.font.init()

# helper functions
def get_img_path(img_name):
    return os.path.join("imgs", img_name)

def load_img(img):
    return pygame.transform.scale2x(pygame.image.load(get_img_path(img)))

# graphics parameters
WIN_WIDTH = 500
WIN_HEIGHT = 800

# images (raw_names)
birds_imgs = ["bird1.png", "bird2.png", "bird3.png"]
base_img_name = "base.png"
bg_img_name = "bg.png"
pipe_img_name = "pipe.png"

# images
BIRD_IMGS = [load_img(img) for img in birds_imgs]
BASE_IMG = load_img(base_img_name)
BG_IMG = load_img(bg_img_name)
PIPE_IMG = load_img(pipe_img_name)

# font
STAT_FONT = pygame.font.SysFont('comicsans', 50)

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
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return t_point or b_point


class Base:
    IMG = BASE_IMG
    VEL = 5
    WIDTH = IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = {Pipe(700)}
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    score = 0
    while run:
        clock.tick(40)
        add_pipe = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        rem = list()
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.add(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_width() >= 730:
            # hitted the ground
            pass

        base.move()
        draw_window(win=win, bird=bird, pipes=pipes, base=base, score=score)

    pygame.quit()
    quit()


main()
