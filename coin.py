import pygame
from SUPERMARIO静止画面 import tools
from.import constant as c


class Flashingcoin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []  # 空图片列表？
        self.frame_index = 0
        frame_rects = [(1, 160, 5, 8), (9, 160, 5, 8), (17, 160, 5, 8), (9, 160, 5, 8)]
        self.load_frames(frame_rects)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 58
        self.timer = 0

    def load_frames(self, frame_rects):
        for frame_rect in frame_rects:
            self.frames.append(tools.load_image('D:\\game\\Mario\\resources\\graphics\\item_objects.png',*frame_rect,(0,0,0),c.PLAYER_SCALE))  # *解包

    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_durations = [375, 125, 125, 125]
        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= 4  # 不能超过索引范围
            self.timer = self.current_time

        self.image = self.frames[self.frame_index]  # 绘制


class Levelcoin(Flashingcoin):
    def __init__(self, x, y):
        Flashingcoin.__init__(self)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


