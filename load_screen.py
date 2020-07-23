import pygame
from SUPERMARIO静止画面 import info
from SUPERMARIO静止画面 import tools
from.import constant as c


class LoadScreen:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next_state = 'level'
        self.timer = 0
        self.duration = 2000
        self.info = info.Info('load_screen', self.game_info)
        self.player()
        self.info.start(self.game_info)

    def player(self):
        self.palyer = tools.load_image('D:\\game\\Mario\\resources\\graphics\\mario_bros.png', 178, 32, 12, 16,
                                       (0, 0, 0), c.PLAYER_SCALE)

    def update(self, surface, keys):
        self.draw(surface)
        self.current_time = pygame.time.get_ticks()
        self.info.update()
        if self.timer == 0:
            self.timer = self.current_time
        if self.current_time - self.timer > self.duration:
            self.finished = True
            self.timer = 0

    def draw(self,surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)
        surface.blit(self.palyer, (300, 270))


class GameOver(LoadScreen):
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next_state = 'main_menu'
        self.duration = 4000
        self.timer = 0
        self.info = info.Info('game_over', self.game_info)
        self.info.start(self.game_info)

    def draw(self,surface):
        surface.fill((0, 0, 0))
        self.info.draw(surface)
