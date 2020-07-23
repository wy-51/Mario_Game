import pygame
from SUPERMARIO静止画面 import tools, setup
from.import constant as c
import json
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def setup_states(self):
        self.face_right = True
        self.dead = False
        self.big = False

    def setup_velocities(self):
        self.x_vel = 0
        self.y_vel = 0

    def setup_timers(self):
        self.walking_timer = 0
        self.transition_time = 0

    def load_images(self):
        self.right_frames = []
        self.left_frames = []
        self.up_frames = []
        self.down_frames = []

        frame_rects = [(178,32,12,16),(80,32,15,16),(96,32,16,16),(112,32,16,16)]
        for frame_rect in frame_rects:
            right_image = tools.load_image('D:\\game\\Mario\\resources\\graphics\\mario_bros.png', *frame_rect,(0,0,0),c.PLAYER_SCALE)
            left_image = pygame.transform.flip(right_image,True,False)
            # pygame.transform.flip(反转对象，左右是否反转，上下是否反转)
            up_image = pygame.transform.rotate(right_image,90)
            down_image = pygame.transform.rotate(right_image,-90)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)
            self.up_frames.append(up_image)
            self.down_frames.append(down_image)

        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self,keys):
        self.current_time = pygame.time.get_ticks()  # 设置计时器实现帧的循环
        if keys[pygame.K_RIGHT]:
            self.x_vel = 1
            self.y_vel = 0
            self.frames = self.right_frames  # 换掉帧对应的库
        if keys[pygame.K_LEFT]:
            self.x_vel = -1
            self.y_vel = 0
            self.frames = self.left_frames
        if keys[pygame.K_UP]:
            self.x_vel = 0
            self.y_vel = -1
            self.frames = self.up_frames
        if keys[pygame.K_DOWN]:
            self.x_vel = 0
            self.y_vel = 1
            self.frames = self.down_frames
        if self.current_time - self.walking_timer > 100:
            self.walking_timer = self.current_time
            self.frame_index += 1
            self.frame_index %= 4
        self.image = self.frames[self.frame_index]