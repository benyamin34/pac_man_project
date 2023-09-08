# images of project
import pygame

#import images
red_img = pygame.transform.scale(pygame.image.load(f'char_images/red.png'), (35, 35))
pink_img = pygame.transform.scale(pygame.image.load(f'char_images/pink.png'), (35, 35))
blue_img = pygame.transform.scale(pygame.image.load(f'char_images/blue.png'), (35, 35))
orange_img = pygame.transform.scale(pygame.image.load(f'char_images/orange.png'), (35, 35))
spooked_img = pygame.transform.scale(pygame.image.load(f'char_images/powerup.png'), (35, 35))
dead_img = pygame.transform.scale(pygame.image.load(f'char_images/dead.png'), (35, 35))

pacman_image = []
for i in range(1, 5):
    pacman_image.append(pygame.transform.scale(pygame.image.load(f'char_images/{i}.png'), (35, 35)))
    
    
    
#pacman_image = pygame.image.load(f'char_images/pacman.png')
#pacman_image = pygame.transform.scale(pacman_image, (35, 35))