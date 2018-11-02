import pygame
class Settings():
    def __init__(self,width,high):
        '初始化游戏屏幕的设置'
        self.width=width
        self.high=high
        self.color=(120,230,230)
        self.snake_speed=25
        self.snake_wide=23
        self.snake_high=23
        self.snake_color=(0,0,0)