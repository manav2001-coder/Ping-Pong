import pygame
import random
import time
import math
from pygame.locals import (
KEYDOWN,
QUIT,
K_UP,
K_DOWN,
K_RIGHT,
K_LEFT,
K_ESCAPE
)
from random import *
class Game:
    def __init__(self):
        pygame.init()
        self.SCORE_FONT = pygame.font.SysFont("comicsans", 50)
        self.screen=pygame.display.set_mode((400,400))
        self.pedal_one=Pedal(0,160,self.screen)
        self.pedal_two=Pedal(380,160,self.screen)
        self.ball=Ball(self.screen)
        self.left_score=0
        self.right_score=0
    def draw(self):
        self.screen.fill((0,0,0))
        left_score_text=self.SCORE_FONT.render(f"{self.left_score}",1,(255,255,255))
        right_score_text=self.SCORE_FONT.render(f"{self.right_score}",1,(255,255,255))
        self.screen.blit(left_score_text,(400 // 4 -left_score_text.get_width(),20))
        self.screen.blit(right_score_text,(3*400 // 4 - right_score_text.get_width(),20))
        self.pedal_one.draw()
        self.pedal_two.draw()
        pygame.draw.rect(self.screen,(255,255,255),(200,0,1,400))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.ball.x, self.ball.y), self.ball.rad)
        pygame.display.flip()

    def run(self):
        running=True
        while(running):
            keys=pygame.key.get_pressed()
            selected_pedal = self.pedal_two if (self.ball.vel_x > 0) else self.pedal_one
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if keys[pygame.K_UP]:
                    selected_pedal.move_up()
                if keys[pygame.K_DOWN]:
                    selected_pedal.move_down()
            if self.ball.y-self.ball.rad<=0:
                self.ball.vel_y*=-1
            if self.ball.y+self.ball.rad>=400:
                self.ball.vel_y*=-1
            if self.ball.vel_x<0:
                if self.ball.y-self.ball.rad>=selected_pedal.y and self.ball.y<=selected_pedal.y+100:
                    if self.ball.x-self.ball.rad<=selected_pedal.x+20:
                        self.ball.vel_x*=-1
                        diff = selected_pedal.y + 100 / 2 - self.ball.y
                        reduction_factor = (100 / 2) / 8
                        y_vel = diff / reduction_factor
                        self.ball.vel_y = -1 * y_vel
            else:
                if self.ball.y >= selected_pedal.y and self.ball.y <= selected_pedal.y + 100:
                    if self.ball.x+self.ball.rad>=selected_pedal.x:
                        self.ball.vel_x*=-1
                        diff = selected_pedal.y + 100/2 - self.ball.y
                        reduction_factor=(100 / 2) / 15
                        y_vel=diff / reduction_factor
                        self.ball.vel_y = -1*y_vel
            if self.ball.x<0:
              self.right_score+=1
              self.ball.reset()
              self.pedal_two.reset()
              self.pedal_one.reset()
            elif self.ball.x>400:
              self.left_score+=1
              self.ball.reset()
              self.pedal_two.reset()
              self.pedal_one.reset()

            if self.left_score>=10:
                self.ball.reset()
                self.pedal_one.reset()
                self.pedal_two.reset()
                self.left_score=self.right_score=0
            elif self.right_score>=10:
                self.ball.reset()
                self.pedal_one.reset()
                self.pedal_two.reset()
                self.right_score=self.left_score=0
            self.ball.move()
            self.draw()
class Pedal:
    def __init__(self,x,y,screen):
        self.x=self.orignal_x=x
        self.y=self.orignal_y=y
        self.screen=screen
    def draw(self):
        pygame.draw.rect(self.screen,(255,255,255),(self.x,self.y,20,100))
    def move_up(self):
        self.y-=40
        self.draw()
    def move_down(self):
        self.y+=40
        self.draw()
    def reset(self):
        self.x=self.orignal_x
        self.y=self.orignal_y
class Ball:
    def __init__(self,screen):
        self.x=self.orignal_x=200
        self.y=self.orignal_y=200
        self.rad=10
        self.screen=screen
        self.vel_x=20
        self.vel_y=0
    def move(self):
        self.x+=self.vel_x
        self.y+=self.vel_y
        time.sleep(0.1)
    def reset(self):
        self.x=self.orignal_x
        self.y=self.orignal_y
        self.vel_y=0
        self.vel_x*=-1

if __name__ == '__main__':
    game=Game()
    game.run()