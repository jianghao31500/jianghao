import pygame
import sys
import tkinter as tk
from tkinter import messagebox

def run_snake(a):
    def Right():
        a.append((a[x-1][0]+25,a[x-1][1]))
        del a[0]
        return a
    def Left():
        a.append((a[x-1][0]-25,a[x-1][1]))
        del a[0]
        return a
    def Down():
        a.append((a[x-1][0],a[x-1][1]+25))
        del a[0]
        return a
    def Up():
        a.append((a[x-1][0],a[x-1][1]-25))
        del a[0]
        return a
    x=len(a)
    direction="down"
    if a[x-1][0]-a[x-2][0]==25:
        direction="right"
    elif a[x-1][0]-a[x-2][0]==-25:
        direction="left"
    elif a[x-1][1]-a[x-2][1]==25:
        direction="down"
    elif a[x-1][1]-a[x-2][1]==-25:
        direction="up"
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            x=tk.messagebox.askyesno("退出",'你确定退出游戏吗？')
            if x:
                sys.exit()
            else:
                break
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT and direction!="life" and direction!="right":
                return  Right()
            elif event.key==pygame.K_LEFT and direction!="right" and direction!="life":
                return Left()
            elif event.key==pygame.K_UP and direction!="down" and direction!="up":
                return Up()
            elif event.key==pygame.K_DOWN and direction!="up" and direction!="down":
                return Down()
    else :
        if direction=="right":
            return Right()
        elif direction=="left":
            return Left()
        elif direction=="down":
            return Down()
        elif direction=="up":
            return Up()
