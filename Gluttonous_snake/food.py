import pygame
import random
class Food():
    def __init__(self,screen,set):
        wide=random.randrange(25,set.width-1,25)
        high=random.randrange(0,set.high-1,25)
        self.screen=screen
        self.rect=pygame.Rect(0,0,set.snake_wide,set.snake_high)
        self.rect.centerx=wide
        self.rect.top=high
        self.color=(255,128,128)
        print(wide,high)
    def blitme(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
