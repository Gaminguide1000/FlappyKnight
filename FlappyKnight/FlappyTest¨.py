import pygame
from pygame.locals import *
import random
import time as t
import os
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
#Change directory
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
os.chdir(script_directory)

#Change the Files directory to use the Dependencies
script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)
target_directory = os.path.join(script_directory, 'Dependencies')
os.chdir(target_directory)

file_path = "highscores.txt"

with open("highscores.txt", 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into variable and value
        variable, value = line.strip().split('=')

        # Remove leading and trailing spaces from variable and value
        variable = variable.strip()
        value = value.strip()
        
        # Assign the value to the corresponding variable
        if variable == 'noob_highscore':
            noob_highscore = int(value)
        elif variable == 'experienced_highscore':
            experienced_highscore = int(value)
        elif variable == 'pro_highscore':
            pro_highscore = int(value)
        elif variable == 'harder_noob_highscore':
            harder_noob_highscore = int(value)
        elif variable == 'harder_experienced_highscore':
            harder_experienced_highscore = int(value) 
        elif variable == 'harder_pro_highscore':
            harder_pro_highscore = int(value)
        elif variable == 'first_run':
            if value == 'True':
                webbrowser.open('readme.txt')

# Function to update highscores in the file
def update_highscores_file():
    # Create a string with the new highscore values
    new_highscores = f"noob_highscore = {noob_highscore}\n" \
                     f"experienced_highscore = {experienced_highscore}\n" \
                     f"pro_highscore = {pro_highscore}\n"\
                     f"harder_noob_highscore = {harder_noob_highscore}\n" \
                     f"harder_experienced_highscore = {harder_experienced_highscore}\n" \
                     f"harder_pro_highscore = {harder_pro_highscore}\n"\
                     f"first_run = False"


    # Write the new highscores to the file
    with open(file_path, 'w') as file:
        file.write(new_highscores)

def open_slider_popup():
    def on_window_close():
        pass
    roott = tk.Tk()
    roott.withdraw()  # Hide the main window


    

    #x_coordinate = 440
    #y_coordinate = 280




    popup = tk.Toplevel(roott)
    popup.title("Choose Music Volume")
    popup.geometry(f"{sliderwidth}x{sliderheight}+{x_coordinate}+{y_coordinate}")

    slider = tk.Scale(popup, from_=0, to=100, orient=tk.HORIZONTAL, length=slider_length)
    slider.set(uncalcvolume)
    slider.pack(padx=20, pady=10)

    ok_button = tk.Button(popup, text="OK", command=lambda: on_ok_button(roott, slider.get(), popup))
    ok_button.pack(pady=10)

    popup.grab_set()  # Make the popup grab the focus
    popup.protocol("WM_DELETE_WINDOW", on_window_close)
    popup.mainloop()  # Run the popup's main loop

    return selected_value


def on_ok_button(roott, value, popup):
    global selected_value
    selected_value = value
    popup.destroy()
    roott.quit()

sliderwidth = 300
sliderheight = 200
slider_length = 200
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
time_now_harder = 0
gliding = False
max_pipe_etc = False

pygame.mixer.music.load('bg_music.wav')
pygame.mixer.music.set_volume(0.5)

paused = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FlappyKnight')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colours
white = (14, 27, 173)
black = (0, 0, 0)



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
updated_file = False
volume = 0.5
uncalcvolume = 50

experienced_scroll_speed = 10
experienced_pipe_gap = 300
experienced_pipe_frequency = 1200
experienced_pipe_max = 270
experienced_pipe_min = -270
experienced_bg = pygame.image.load('bg1.png')
experienced_pipe_image = "pipe1.png"
experienced_ground_img = pygame.image.load('ground1.png')


pro_scroll_speed = 15
pro_pipe_gap = 200
pro_pipe_frequency = 700
pro_pipe_max = 320
pro_pipe_min = -320
pro_gravity_strength = 0.75
pro_jump_strength = -15
pro_bg = pygame.image.load('bg2.png')
pro_pipe_image = "pipe2.png"
pro_ground_img = pygame.image.load('ground2.png') 


#noob_highscore = 0
#experienced_highscore = 0
#pro_highscore = 0


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
            if gliding == True:
                self.vel = gliding_gravity
            else:
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
        self.image = pygame.image.load(pipe_image)
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
button = Button(screen_width // 2 - 100, screen_height // 2 - 50, button_img)

run = True
ROOT = tk.Tk()
ROOT.withdraw()
def ask_difficulty():
    global score
    score = 0
    def combobox_ask():

        def on_combobox_change(event):
            global difficulty
            difficulty = combobox.get().upper()
            root.destroy()
            root.quit()
        
        def on_window_close():
            pass
        root = tk.Tk()
        root.title("Difficulty Selection")
        global difficulty
        difficulty = ""

       # Creating a Combobox
        combobox = ttk.Combobox(root, values=["Noob", "Experienced", "Pro"])
        combobox.set("Select Difficulty")
        combobox.pack(padx=10, pady=10)
        window_width = 300
        window_height = 200
        # Binding the event to the function
        combobox.bind("<<ComboboxSelected>>", on_combobox_change)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        global x_coordinate
        global y_coordinate
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the geometry of the window to center it on the screen
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        root.protocol("WM_DELETE_WINDOW", on_window_close)
        root.mainloop()
    combobox_ask()


    def ask_get_harder():
        def on_yes():
            global get_harder
            get_harder = True
            root.destroy()

        def on_no():
            global get_harder 
            get_harder = False
            root.destroy()

    # Initialize Tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the main window

    # Create the messagebox
        result = messagebox.askyesno("Question", "Do you want the game to get harder?")

    # Process the result
        if result:
            on_yes()
        else:
            on_no()
    ask_get_harder()
    global old_difficulty
    old_difficulty = difficulty
    update_physics()
    t.sleep(1)
    pygame.mixer.music.play(-1)


def update_physics():
    global pipe_image
    global ground_scroll
    global scroll_speed
    global pipe_gap
    global pipe_frequency
    global pipe_max
    global pipe_min
    global gravity_strength
    global jump_strength
    global bg
    global ground_img
    global gliding_gravity
    if difficulty == "NOOB" or difficulty == "EXPERIENCED" or difficulty == "PRO":
        if difficulty == "NOOB":
            ground_scroll = 0
            scroll_speed = 5
            pipe_gap = 400
            pipe_frequency = 2000
            pipe_max = 200
            pipe_min = -200
            gravity_strength = 0.25
            jump_strength = -5
            gliding_gravity = 3
            bg = pygame.image.load('bg.png')
            pipe_image = "pipe.png"
            ground_img = pygame.image.load('ground.png') 
        elif difficulty == "EXPERIENCED":
            ground_scroll = 0
            scroll_speed = 10
            pipe_gap = 300
            pipe_frequency = 1500
            pipe_max = 250
            pipe_min = -250
            gravity_strength = 0.5
            jump_strength = -10
            gliding_gravity = 2.5
            bg = pygame.image.load('bg1.png')
            pipe_image = "pipe1.png"
            ground_img = pygame.image.load('ground1.png')
        elif difficulty == "PRO":
            ground_scroll = 0
            scroll_speed = 15
            pipe_gap = 200
            pipe_frequency = 1000
            pipe_max = 300
            pipe_min = -300
            gravity_strength = 0.75
            jump_strength = -15
            gliding_gravity = 2
            bg = pygame.image.load('bg2.png')
            pipe_image = "pipe2.png"
            ground_img = pygame.image.load('ground2.png') 


def update_physics_difficulty(newer_difficulty):
    global pipe_image
    global ground_scroll
    global scroll_speed
    global pipe_gap
    global pipe_frequency
    global pipe_max
    global pipe_min
    global gravity_strength
    global jump_strength
    global bg
    global ground_img
    if newer_difficulty == "EXPERIENCED" or newer_difficulty == "PRO":
        if newer_difficulty == "EXPERIENCED":
            bg = pygame.image.load('bg1.png')
            pipe_image = "pipe1.png"
            ground_img = pygame.image.load('ground1.png')
        elif newer_difficulty == "PRO":
            bg = pygame.image.load('bg2.png')
            pipe_image = "pipe2.png"
            ground_img = pygame.image.load('ground2.png') 


last_time = pygame.time.get_ticks()

ask_difficulty()
new_difficulty = difficulty 
beforestart = True
update_highscores_file()
while run:
    clock.tick(fps)
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - last_time
    if difficulty == "PRO" and get_harder == False:
        if score > pro_highscore:
            pro_highscore = score
    elif difficulty == "EXPERIENCED" and get_harder == False:
        if score > experienced_highscore:
            experienced_highscore = score
    elif difficulty == "NOOB" and get_harder == False:
        if score > noob_highscore:
            noob_highscore = score
    elif difficulty == "PRO" and get_harder == True:
        if score > harder_pro_highscore:
            harder_pro_highscore = score
    elif difficulty == "EXPERIENCED" and get_harder == True:
        if score > harder_experienced_highscore:
            harder_experienced_highscore = score
    elif difficulty == "NOOB" and get_harder == True:
        if score > harder_noob_highscore:
            harder_noob_highscore = score

    if scroll_speed >= experienced_scroll_speed:
        new_difficulty = "EXPERIENCED"
    if scroll_speed >= pro_scroll_speed:
        new_difficulty = "PRO" 
    if  new_difficulty != old_difficulty:
        update_physics_difficulty(new_difficulty)
    #Make game harder
    if gravity_strength == 1:
        max_pipe_etc = True   
    if elapsed_time >= 1000:
        last_time = current_time
        
        if get_harder == True and game_over == False and flying == True:
            if max_pipe_etc == False:
                scroll_speed += 0.05
                pipe_gap -= 1 
                pipe_frequency -= 5
                pipe_max -= 0.5
                pipe_min += 0.5
                gravity_strength += 0.0025
                jump_strength -= 0.05
                gliding_gravity += 0.005
            if max_pipe_etc == True:
                pipe_frequency -= 5
                scroll_speed += 0.05
        
    #if score == 5:
        #pygame.mixer.music.stop()  # Stop the background on reaching score 100
        #pygame.mixer.Sound.play(jumpscare_sound)

        #jumpscare_start_time = pygame.time.get_ticks()

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
    draw_text("Highscore:", font, white, int(100), 20)

    if difficulty == "NOOB" and get_harder == False:
        draw_text(str(noob_highscore), font, white, 400, 20)
    elif difficulty == "EXPERIENCED" and get_harder == False:
        draw_text(str(experienced_highscore), font, white, int(400), 20)
    elif difficulty == "PRO" and get_harder == False:
        draw_text(str(pro_highscore), font, white, int(400), 20)
    elif difficulty == "NOOB" and get_harder == True:
        draw_text(str(harder_noob_highscore), font, white, int(400), 20)
    elif difficulty == "EXPERIENCED" and get_harder == True:
        draw_text(str(harder_experienced_highscore), font, white, int(400), 20)
    elif difficulty == "PRO" and get_harder == True:
        draw_text(str(harder_pro_highscore), font, white, int(400), 20)


    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        update_highscores_file()
        update_physics()
    if flappy.rect.bottom >= 768:
        
        game_over = True
        flying = False

    if flying == True and game_over == False:
        pygame.mouse.set_visible(False)
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.uniform(pipe_min, pipe_max)
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
        if difficulty != new_difficulty:
            new_difficulty = difficulty 
        if testing_score == 0:
            pygame.mixer.Sound.play(death_sound)  # Play the death sound
            testing_score += 1
        pygame.mouse.set_visible(True)
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT and flying == False:
            run = False
    if beforestart == True:
        beforestart = False
    keysw = pygame.key.get_pressed()
    if keysw[pygame.K_SPACE] and flying == False and game_over == False:
        flying = True
    if keysw[pygame.K_0] and  flying == False :
        ask_difficulty()
    if keysw[pygame.K_LCTRL] and flying == True and flappy.vel >= gliding_gravity:
        gliding = True
    else:
        gliding = False
    if keysw[pygame.K_LALT] and flying == False:
        uncalcvolume = open_slider_popup()
        volume = uncalcvolume / 100
        pygame.mixer.music.set_volume(volume)
        death_sound.set_volume(volume)
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
    
    if game_over == True and updated_file == False:
        update_highscores_file()
        updated_file = True
    elif game_over == False and updated_file == True:
        updated_file = False

pygame.quit()

