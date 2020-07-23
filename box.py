import pygame
from SUPERMARIO静止画面 import tools
from.import constant as c


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, box_type, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.box_type = box_type
        self.frame_rects = [
            (384, 0, 16, 16),
            (400, 0, 16, 16),
            (416, 0, 16, 16),
            (432, 0, 16, 16),
        ]

        self.frames = []
        for frame_rect in self.frame_rects:
            self.frames.append(tools.load_image('D:\\game\Mario\\resources\\graphics\\tile_set.png', *frame_rect, (0, 0, 0),c.BRICK_SCALE))

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y