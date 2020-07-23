import pygame
from SUPERMARIO静止画面 import tools
from.import constant as c
from SUPERMARIO静止画面 import info


class MainMenu:
    def __init__(self):
        game_info = {
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        }
        self.start(game_info)

    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.setup_player()
        self.setup_cursor()

        self.info = info.Info('main_menu', self.game_info)  # 文字实例化，调用类的方法
        self.finished = False  # main_menu阶段在进行（初始）
        self.next_state = 'load_screen'
        self.reset_game_info()
        self.info.start(self.game_info)

    def setup_background(self):
        self.BG = pygame.image.load('D:\\game\\Mario\\resources\\graphics\\level_1.png')
        w, h = self.BG.get_size()
        self.BG = pygame.transform.scale(self.BG, (int(w*c.BG_SCALE), int(h*c.BG_SCALE)))
        self.viewport = tools.load_image('D:\\game\\Mario\\resources\\graphics\\title_screen.png', 1, 60, 176, 88,
                                                                                            (255, 0, 220),c.BG_SCALE)

    def setup_player(self):
        self.palyer = tools.load_image('D:\\game\\Mario\\resources\\graphics\\mario_bros.png',178,32,12,16,(0,0,0),c.PLAYER_SCALE)

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.load_image('D:\\game\\Mario\\resources\\graphics\\item_objects.png',25,160,8,8,(0,0,0),c.PLAYER_SCALE)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = 220, 360
        self.cursor.rect = rect
        self.cursor.state = '1P'  # 状态机（初始）

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:

            if self.cursor.state == '1P':
                self.finished = True
            elif self.cursor.state == '2P':
                self.finished = True  # 此阶段完结

    def update(self, surface, keys):
        surface.blit(self.BG, (0, 0))
        surface.blit(self.viewport, (170, 100))
        surface.blit(self.palyer, (110, 490))
        surface.blit(self.cursor.image, self.cursor.rect)

        # 先更新后绘图
        self.info.update()
        self.info.draw(surface)

        self.update_cursor(keys)

    def reset_game_info(self):
        self.game_info.update({
            'score': 0,
            'coin': 0,
            'lives': 3,
            'player_state': 'small'
        })