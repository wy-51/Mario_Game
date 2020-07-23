import pygame
from SUPERMARIO静止画面 import constant as c
from SUPERMARIO静止画面 import coin
pygame.font.init()


class Info:
    def __init__(self, state, game_info):
        self.flash_coin = coin.Flashingcoin()
        self.state = state


    def start(self, game_info):
        self.game_info = game_info
        self.creat_state_labels()
        self.creat_info_labels()

    def creat_state_labels(self):
        self.state_labels = []
        if self.state == 'main_menu':
            self.state_labels.append((self.creat_label('1 PLAYER GAME', 25), (272, 360)))
            self.state_labels.append((self.creat_label('2 PLAYER GAME', 25), (272, 405)))
            self.state_labels.append((self.creat_label('TOP - ', 25), (290, 445)))
            self.state_labels.append((self.creat_label('000000', 25), (430, 445)))
        elif self.state == 'load_screen':
            self.state_labels.append((self.creat_label('WORLD', 25), (280, 220)))
            self.state_labels.append((self.creat_label('1 - 1', 25), (430, 220)))
            self.state_labels.append((self.creat_label('×   {}'.format(self.game_info['lives']), 30), (380, 280)))

        elif self.state == 'game_over':
            self.state_labels.append((self.creat_label('GAME OVER', 30), (280, 300)))

    def creat_info_labels(self):
        self.info_labels = []
        self.info_labels.append((self.creat_label('MARIO'), (75, 30)))
        self.info_labels.append((self.creat_label('WORLD'), (450, 30)))
        self.info_labels.append((self.creat_label('TIME'), (640, 30)))
        self.info_labels.append((self.creat_label('000000'), (75, 55)))
        self.info_labels.append((self.creat_label('×{}'.format(self.game_info['coin'])), (300, 55)))
        self.info_labels.append((self.creat_label('1 - 1'), (480, 55)))

    def creat_label(self, label, size=30, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(c.FONT, size)
        label_image = font.render(label, 1, (255, 255, 255))
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image,(int(rect.width*width_scale), int(rect.height*height_scale)))
        return label_image

    def update(self):
        self.flash_coin.update()

    def draw(self,surface):

        for label in self.state_labels:
            surface.blit(label[0], label[1])
        for label in self.info_labels:
            surface.blit(label[0], label[1])
        surface.blit(self.flash_coin.image, self.flash_coin.rect)

