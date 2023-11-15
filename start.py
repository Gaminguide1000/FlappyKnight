import pygame
from pygame.locals import *
import random
import math
import ctypes
import os
import tkinter as tk
from tkinter import simpledialog

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1280
screen_height = 760
jumpscare_img = pygame.image.load('jumpscare.png')
jumpscare_sound = pygame.mixer.Sound('jumpscare.wav')
death_sound = pygame.mixer.Sound('death.wav')
jumpscare_start_time = 0
pipe_max = 300
pipe_min = -300
gravity_strength = 0.5
jump_strength = -10
testing_score = 0

pygame.mixer.music.load('bg_music.wav')
pygame.mixer.music.set_volume(0.5)

paused = False

print(screen_height, "fortnite", screen_width)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DDD')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 10
flying = False
game_over = False
pipe_gap = 250
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# load images
bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pygame.mixer.music.play(-1)  # Restart the background music
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"skin.png")
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # apply gravity
            self.vel += gravity_strength
            if self.vel > 100:
                self.vel = 100
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.vel = jump_strength
            # handle the animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                    self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(
                self.images[self.index], self.vel * -2)
        else:
            # point the bird at the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                global testing_score
                testing_score = 0
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
ROOT = tk.Tk()
ROOT.withdraw()

difficulty = str(simpledialog.askstring(title="Choose difficulty", prompt="How hard should the game be (Noob, Experienced, Pro)?:"))

if difficulty == "Noob" or difficulty == "Experienced" or difficulty == "Pro":
    if difficulty == "Noob":
        ground_scroll = 0
        scroll_speed = 6
        pipe_gap = 400
        pipe_frequency = 2000
        pipe_max = 200
        pipe_min = -200
        gravity_strength = 0.25
        jump_strength = -5
    if difficulty == "Experienced":
        ground_scroll = 0
        scroll_speed = 10
        pipe_gap = 300
        pipe_frequency = 1200
        pipe_max = 270
        pipe_min = -270
    if difficulty == "Pro":
        ground_scroll = 0
        scroll_speed = 15
        pipe_gap = 200
        pipe_frequency = 700
        pipe_max = 320
        pipe_min = -320
        gravity_strength = 0.75
        jump_strength = -15
else:
    run = False
print(difficulty)
pygame.mixer.music.play(-1)


while run:
    clock.tick(fps)

    if score == 5:
        pygame.mixer.music.stop()  # Stop the background music on reaching score 100
        pygame.mixer.Sound.play(jumpscare_sound)

        jumpscare_start_time = pygame.time.get_ticks()

    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground_img, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(pipe_min, pipe_max)
            btm_pipe = Pipe(
                screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(
                screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    if game_over == True:
        pygame.mixer.music.stop()
        if testing_score == 0:
            pygame.mixer.Sound.play(death_sound)  # Play the death sound
            testing_score += 1
        print(testing_score)
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keysw = pygame.key.get_pressed()
        if keysw[pygame.K_SPACE] and flying == False and game_over == False:
            flying = True

    pygame.display.update()

    if jumpscare_start_time > 0:
        current_time = pygame.time.get_ticks()
        jumpscare_duration = 2000

        if current_time - jumpscare_start_time < jumpscare_duration:
            screen.blit(jumpscare_img, (0, 0))
            pygame.display.flip()
            paused = True
            pygame.time.delay(20)
        else:
            jumpscare_start_time = 0
        pygame.mixer.music.play(-1)

pygame.quit()
