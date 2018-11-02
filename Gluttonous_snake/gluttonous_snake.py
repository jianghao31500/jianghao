from Gluttonous_snake.setting import Settings
import sys
import pygame
import tkinter as tk
from tkinter import messagebox
from Gluttonous_snake.food import Food
from Gluttonous_snake.response import run_snake
from Gluttonous_snake.Snake import Snake
import time
def Run_snake():
    pygame.init()
    set =Settings(400,300)
    a=[(set.width//2,set.high//2),(set.width//2,set.high//2+25)]
    sn=[]
    screen=pygame.display.set_mode((set.width,set.high))
    pygame.display.set_caption("贪吃蛇")
    fd=Food(screen,set)
    while True:
            fd=Food(screen,set)
            if (fd.rect.centerx,fd.rect.top) not in a:
                break
    while True:
        time.sleep(0.2)
        print(a)
        a1=a[:]
        a=run_snake(a)
        print(a)
        sn.clear()
        for i in a:
            sn.append(Snake(screen,set,i[0],i[1]))
        screen.fill(set.color)
        if a[len(a)-1] == (fd.rect.centerx,fd.rect.top):
            while True:
                fd=Food(screen,set)
                if (fd.rect.centerx,fd.rect.top) not in a:
                    fd.blitme()
                    break
            a.insert(0,a[0])
        fd.blitme()
        for j in sn:
            j.blitme()
        if a[len(a)-1][0]<=0 or a[len(a)-1][0]>=set.width or a[len(a)-1][1]<0 or a[len(a)-1][1]>set.high-25 or a[len(a)-1] in a1:
            tk.messagebox.showerror("你输了""退出游戏")
            sys.exit()
        pygame.display.update()
Run_snake()