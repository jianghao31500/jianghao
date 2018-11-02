import pygame
class Snake():
    def __init__(self,screen,set,high,wide):
        self.screen=screen
        self.rect=pygame.Rect(0,0,set.snake_wide,set.snake_high)
        self.rect.centerx=high
        self.rect.top=wide
        self.color=set.snake_color
    def blitme(self):
        pygame.draw.rect(self.screen,self.color,self.rect)


