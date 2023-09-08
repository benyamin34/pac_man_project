import pygame
from mapp import paths
import math
import random
from pygame.locals import Rect
import copy
import imgs

pygame.init()
pygame.mixer.init()

disx = 900
disy = 950
dis = pygame.display.set_mode((disx, disy))
pygame.display.set_caption("Pacman!")
pygame.display.update()

music = pygame.mixer.music.load('pacman_song_theme.mp3')

timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20) 
score = 0
level = copy.deepcopy(paths)
black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
pi = math.pi
pygame.mixer.music.play()

# x , y = 100 , 100
x_change, y_change = 0, 0
s = 10
# pacman_size = 35
pacman_speed = 2
level = paths
hearts = 3

powerup = False
game_won = False
power_counter = 0
powerup = False
flicker = 0
startup_counter = 0    
    
pacman_x , pacman_y = 450, 663
counter = 0
direction = 0
score = 0
direction_command = 0
targets = [(pacman_x, pacman_y), (pacman_x, pacman_y), (pacman_x, pacman_y), (pacman_x, pacman_y)]

red_x = 56
red_y = 58
red_direction = 0
blue_x = 440
blue_y = 388
blue_direction = 2
pink_x = 440
pink_y = 438
pink_direction = 2
orange_x = 440
orange_y = 438
orange_direction = 2

red_ghost_dead = False
blue_ghost_dead = False
orange_ghost_dead = False
pink_ghost_dead = False
red_box = False
blue_box = False
orange_box = False
pink_box = False
moving = False

# center_x = pacman_x + 23
# center_y = pacman_y + 24

pacmanx_change = 0
pacmany_change = 0
eaten_ghost = [False, False, False, False]
turns_allowed = [False, False, False, False]



def draw_board():
    number1 = ((disy - 50) // 32)
    number2 = (disx // 30)    
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(dis, white, (j * number2 + (0.5*number2), i * number1 + (0.5 * number1)), 4)
                
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(dis, white, (j * number2 + (0.5*number2), i * number1 + (0.5 * number1)), 10)
                
            if level [i][j] == 3:
                pygame.draw.line(dis, blue, (j * number2 + (0.5 * number2), i * number1),
                                 (j * number2 + (0.5 * number2), i * number1 + number1), 3)
                
            if level [i][j] == 4:
                pygame.draw.line(dis, blue, (j * number2, i * number1 + (0.5 * number1)),
                                 (j * number2 + number2, i * number1 + (0.5 * number1)), 3)    
            
            if level [i][j] == 5:
                pygame.draw.arc(dis, blue, [(j * number2 - (number2* 0.5)), (i * number1 + (0.5 * number1)), number2, number1], 0 , pi/2, 3)
            
            if level[i][j] == 6:
                pygame.draw.arc(dis, blue,
                                [(j * number2 + (number2 * 0.5)), (i * number1 + (0.5 * number1)), number2, number1], pi / 2, pi, 3)
            
            if level[i][j] == 7:
                pygame.draw.arc(dis, blue, [(j * number2 + (number2 * 0.5)), (i * number1 - (0.4 * number1)), number2, number1], pi,
                                3 * pi / 2, 3)
            
            if level[i][j] == 8:
                pygame.draw.arc(dis, blue,
                                [(j * number2 - (number2 * 0.4)) - 2, (i * number1 - (0.4 * number1)), number2, number1], 3 * pi / 2,
                                2 * pi, 3)
            
            if level [i][j] == 9:
                pygame.draw.line(dis, white, (j * number2, i * number1 + (0.5 * number1)),
                                 (j * number2 + number2, i * number1 + (0.5 * number1)), 3)
                       
            
# pacman design
def draw_pacman():
    if direction == 0:
        dis.blit(imgs.pacman_image[counter // 5], (pacman_x, pacman_y))
    elif direction == 1:
        dis.blit(pygame.transform.flip(imgs.pacman_image[counter // 5], True, False), (pacman_x, pacman_y))
    elif direction == 2:
        dis.blit(pygame.transform.rotate(imgs.pacman_image[counter // 5], 90), (pacman_x, pacman_y))
    elif direction == 3:
        dis.blit(pygame.transform.rotate(imgs.pacman_image[counter // 5], 270), (pacman_x, pacman_y))



#Movement
def movement(event, pacmanx_change, pacmany_change):
    
    if event.type == pygame.KEYDOWN: # event: key press
        if event.key == pygame.K_LEFT:
            pacmanx_change = -5
            pacmany_change = 0
        elif event.key == pygame.K_RIGHT:
            pacmanx_change = 5
            pacmany_change = 0
        elif event.key == pygame.K_UP:
            pacmanx_change = 0
            pacmany_change = -5
        elif event.key == pygame.K_DOWN:
            pacmanx_change = 0
            pacmany_change = 5    
    return pacmanx_change, pacmany_change   


    
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            dis.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            dis.blit(imgs.spooked_img, (self.x_pos, self.y_pos))
        else:
            dis.blit(imgs.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((disy - 50) // 32)
        num2 = (disx // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_orange(self):
        # r, l, u, d
        # orange_ghost is going to turn ....
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_red(self):
        # red ghost is going to turn ....
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blue(self):
        # blue_ghost turns up .....
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pink(self):
        # blue_ghost is going to turn ....
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
    
    
    
def draw_scoreboard():
    score_text = font.render(f'Score: {score}', True, 'white')
    dis.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(dis, 'blue', (140, 930), 15)
    for i in range(hearts):
        dis.blit(pygame.transform.scale(imgs.pacman_image[0], (35, 35)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(dis, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(dis, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        dis.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(dis, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(dis, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        dis.blit(gameover_text, (100, 300))
    
def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (disy - 50) // 32
    num2 = disx // 30
    if 0 < pacman_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts
  

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (disy - 50) // 32
    num2 = (disx // 30)
    num3 = 15
    # check masir ha
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):

    if direction == 0 and turns_allowed[0]:
        play_x += pacman_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= pacman_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= pacman_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += pacman_speed
    return play_x, play_y

def get_targets(redd_x, redd_y, bluee_x, bluee_y, pinkk_x, pinkk_y, org_x, org_y):
    if pacman_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if pacman_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not red_ghost.dead and not eaten_ghost[0]:
            redd_target = (runaway_x, runaway_y)
        elif not red_ghost.dead and eaten_ghost[0]:
            if 340 < redd_x < 560 and 340 < redd_y < 500:
                redd_target = (400, 100)
            else:
                redd_target = (pacman_x, pacman_y)
        else:
            redd_target = return_target
        if not blue_ghost.dead and not eaten_ghost[1]:
            bluee_target = (runaway_x, pacman_y)
        elif not blue_ghost.dead and eaten_ghost[1]:
            if 340 < bluee_x < 560 and 340 < bluee_y < 500:
                bluee_target = (400, 100)
            else:
                bluee_target = (pacman_x, pacman_y)
        else:
            bluee_target = return_target
        if not pink_ghost.dead:
            pinkk_target = (pacman_x, runaway_y)
        elif not pink_ghost.dead and eaten_ghost[2]: 
            if 340 < pinkk_x < 560 and 340 < pinkk_y < 500:
                pinkk_target = (400, 100)
            else:
                pinkk_target = (pacman_x, pacman_y)
        else:
            pinkk_target = return_target
        if not orange_ghost.dead and not eaten_ghost[3]:
            org_target = (450, 450)
        elif not orange_ghost.dead and eaten_ghost[3]:
            if 340 < org_x < 560 and 340 < org_y < 500:
                org_target = (400, 100)
            else:
                org_target = (pacman_x, pacman_y)
        else:
            org_target = return_target
    else:
        if not red_ghost.dead:
            if 340 < redd_x < 560 and 340 < redd_y < 500:
                redd_target = (400, 100)
            else:
                redd_target = (pacman_x, pacman_y)
        else:
            redd_target = return_target
        if not blue_ghost.dead:
            if 340 < bluee_x < 560 and 340 < bluee_y < 500:
                bluee_target = (400, 100)
            else:
                bluee_target = (pacman_x, pacman_y)
        else:
            bluee_target = return_target
        if not pink_ghost.dead:
            if 340 < pinkk_x < 560 and 340 < pinkk_y < 500:
                pinkk_target = (400, 100)
            else:
                pinkk_target = (pacman_x, pacman_y)
        else:
            pinkk_target = return_target
        if not orange_ghost.dead:
            if 340 < org_x < 560 and 340 < org_y < 500:
                org_target = (400, 100)
            else:
                org_target = (pacman_x, pacman_y)
        else:
            org_target = return_target
    return [redd_target, bluee_target, pinkk_target, org_target]


game_over = False
while not game_over:
    dis.fill(black) 
    draw_board()
    draw_scoreboard()
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    dis.fill(black)
    draw_board()
    center_x = pacman_x + 23
    center_y = pacman_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if red_ghost_dead:
        ghost_speeds[0] = 4
    if blue_ghost_dead:
        ghost_speeds[1] = 4
    if pink_ghost_dead:
        ghost_speeds[2] = 4
    if orange_ghost_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    
    
    
      
        
        
    player_circle = pygame.draw.circle(dis, black, (center_x, center_y), 20, 2)
    draw_pacman() 
    red_ghost = Ghost(red_x, red_y, targets[0], ghost_speeds[0], imgs.red_img, red_direction, red_ghost_dead,
                   red_box, 0)
    blue_ghost = Ghost(blue_x, blue_y, targets[1], ghost_speeds[1], imgs.blue_img, blue_direction, blue_ghost_dead,
                 blue_box, 1)
    pink_ghost = Ghost(pink_x, pink_y, targets[2], ghost_speeds[2], imgs.pink_img, pink_direction, pink_ghost_dead,
                  pink_box, 2)
    orange_ghost = Ghost(orange_x, orange_y, targets[3], ghost_speeds[3], imgs.orange_img, orange_direction, orange_ghost_dead,
                  orange_box, 3)
    
    targets = get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y, orange_x, orange_y)
    #dis.blit(imgs.pacman_image, (pacman_x, pacman_y))
    
    turns_allowed = check_position(center_x, center_y)
    if moving:
        pacman_x, pacman_y = move_player(pacman_x, pacman_y)
        if not red_ghost_dead and not red_ghost.in_box:
            red_x, red_y, red_direction = red_ghost.move_red()
        else:
            red_x, red_y, red_direction = red_ghost.move_orange()
        if not pink_ghost_dead and not pink_ghost.in_box:
            pink_x, pink_y, pink_direction = pink_ghost.move_pink()
        else:
            pink_x, pink_y, pink_direction = pink_ghost .move_orange()
        if not blue_ghost_dead and not blue_ghost.in_box:
            blue_x, blue_y, blue_direction = blue_ghost.move_blue()
        else:
            blue_x, blue_y, blue_direction = blue_ghost.move_orange()
        orange_x, orange_y, orange_direction = orange_ghost.move_orange()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    
    if not powerup:
        if (player_circle.colliderect(red_ghost.rect) and not red_ghost.dead) or \
                (player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead) or \
                (player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead) or \
                (player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead):
            if hearts > 0:
                hearts -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                pink_x = 440
                pink_y = 438
                pink_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_ghost_dead = False
                blue_ghost_dead = False
                orange_ghost_dead = False
                pink_ghost_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(red_ghost.rect) and eaten_ghost[0] and not red_ghost.dead:
        if hearts > 0:
            powerup = False
            power_counter = 0
            hearts -= 1
            startup_counter = 0
            pacman_x = 450
            pacman_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_ghost_dead = False
            blue_ghost_dead = False
            orange_ghost_dead = False
            pink_ghost_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blue_ghost.rect) and eaten_ghost[1] and not blue_ghost.dead:
        if hearts > 0:
            powerup = False
            power_counter = 0
            hearts -= 1
            startup_counter = 0
            pacman_x = 450
            pacman_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_ghost_dead = False
            blue_ghost_dead = False
            orange_ghost_dead = False
            pink_ghost_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pink_ghost.rect) and eaten_ghost[2] and not pink_ghost.dead:
        if hearts > 0:
            powerup = False
            power_counter = 0
            hearts -= 1
            startup_counter = 0
            pacman_x = 450
            pacman_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_ghost_dead = False
            blue_ghost_dead = False
            orange_ghost_dead = False
            pink_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(orange_ghost.rect) and eaten_ghost[3] and not orange_ghost.dead:
        if hearts > 0:
            powerup = False
            power_counter = 0
            hearts -= 1
            startup_counter = 0
            pacman_x = 450
            pacman_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            pink_x = 440
            pink_y = 438
            pink_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_ghost_dead = False
            blue_ghost_dead = False
            orange_ghost_dead = False
            pink_ghost_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(red_ghost.rect) and not red_ghost.dead and not eaten_ghost[0]:
        red_ghost_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(blue_ghost.rect) and not blue_ghost.dead and not eaten_ghost[1]:
        blue_ghost_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pink_ghost.rect) and not pink_ghost.dead and not eaten_ghost[2]:
        pink_ghost_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(orange_ghost.rect) and not orange_ghost.dead and not eaten_ghost[3]:
        orange_ghost_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                pacman_x = 450
                pacman_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                pink_x = 440
                pink_y = 438
                pink_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_ghost_dead = False
                blue_ghost_dead = False
                orange_ghost_dead = False
                pink_ghost_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(paths)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
    
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
        
    if pacman_x > 900:
        pacman_x = -47
    elif pacman_x < -50:
        pacman_x = 897

    if red_ghost.in_box and red_ghost_dead:
        red_ghost_dead = False
    if blue_ghost.in_box and blue_ghost_dead:
        blue_ghost_dead = False
    if pink_ghost.in_box and pink_ghost_dead:
        pink_ghost_dead = False
    if orange_ghost.in_box and orange_ghost_dead:
        orange_ghost_dead = False    
            
                
                
                
    # pygame.display.update()
           
    timer.tick(fps)
    pygame.display.flip()
    
pygame.quit()
    
    
