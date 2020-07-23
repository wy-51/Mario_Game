import pygame
from SUPERMARIO静止画面 import tools, setup, stuff, brick, box, enemy, coin
from SUPERMARIO静止画面 import info
from.import constant as c
from SUPERMARIO静止画面 import player_2
import json
import os


class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next_state = 'game_over'
        self.setup_background()
        self.info = info.Info('level', game_info)
        self.load_map_data()
        self.set_position()
        self.setup_player()  # 关卡中玩家初始化
        self.setup_ground_items()
        self.setup_bricks_and_boxes()
        self.setup_enemies()
        self.setup_checkpoints()
        self.setup_coin()

    def setup_background(self):
        self.BG = pygame.image.load('D:\\game\\Mario\\resources\\graphics\\level_1.png')
        w, h = self.BG.get_size()
        self.BG = pygame.transform.scale(self.BG, (int(w*c.BG_SCALE), int(h*c.BG_SCALE)))
        self.viewport = tools.load_image('D:\\game\\Mario\\resources\\graphics\\title_screen.png', 1, 60, 176, 88,
                                                                                          (255, 0, 220),c.BG_SCALE)
        self.BG_rect = self.BG.get_rect()
        self.game_window = setup.SCREEN.get_rect()
        self.bg = pygame.Surface((self.BG_rect.width, self.BG_rect.height))  # 创建一个大小和游戏背景图一致的黑色对象

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('D:\game\Mario\source\data\maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def set_position(self):
        self.position = []
        for data in self.map_data['maps']:
            self.position.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.position[0]


    def setup_player(self):  # 定义方法
        self.player = player_2.Player('mario')
        self.player.rect.x = self.player_x
        self.player.rect.bottom = self.player_y

    def setup_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def setup_bricks_and_boxes(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()

        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x,y = brick_data['x'],brick_data['y']
                brick_type = brick_data['type']
                if 'brick_num' in brick_data:
                    # TODO batch bricks
                    pass
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_type = box_data['type']
                self.box_group.add(box.Box(x, y, box_type))

    def setup_enemies(self):
        self.dying_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        # 创建存放敌人的空字典，键：组数；值：存放所有野怪的精灵组
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def setup_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h, checkpoint_type = item['x'], item['y'], item['width'], item['height'], item['type']
            enemy_groupid = item.get('enemy_groupid')
            check_point = stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid)
            self.checkpoint_group.add(check_point)

    def setup_coin(self):
        self.coin_group = pygame.sprite.Group()
        for coin_data in self.map_data['coin']:
            x, y = coin_data['x'], coin_data['y']
            self.coin_group.add(coin.Levelcoin(x, y))

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)
        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                self.finished = True
                self.update_game_info()

        else:
            self.update_player_position()
            self.check_checkpoint()
            self.check_if_go_die()
            self.update_window_position()
            self.brick_group.update()
            self.box_group.update()
            self.enemy_group.update(self)
            self.dying_group.update(self)
            self.coin_group.update()
        self.draw(surface)

    def check_if_go_die(self):
        if self.player.rect.y > c.SCREEN_H:
            self.player.go_die()

    def update_player_position(self):  # 利用当前玩家速度更新位置的方法
        self.player.rect.x += self.player.x_vel
        if self.player.rect.x < self.start_x:
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x

        # x方向
        self.check_x_collision()
        self.player.rect.y += self.player.y_vel
        # y方向
        if not self.player.dead:
            self.player.rect.y += self.player.y_vel
            self.check_y_collision()

    def check_x_collision(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)
        if ground_item:
            self.adjust_player_x(ground_item)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            # self.player.go_die()
            pass

        coin = pygame.sprite.spritecollideany(self.player, self.coin_group)
        if coin:
            coin.kill()
            self.game_info['coin'] += 1

    def check_y_collision(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, check_group)

        if ground_item:
            self.adjust_player_y(ground_item)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.enemy_group.remove(enemy)
            self.dying_group.add(enemy)
            # 从下往上顶敌人
            if self.player.y_vel < 0:
                how = 'bumped'
            # 从上往下压敌人
            else:
                how = 'trampled'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.y_vel = self.player.jump_vel*0.8
            enemy.go_die(how)

        self.check_will_fall(self.player)

        coin = pygame.sprite.spritecollideany(self.player, self.coin_group)
        if coin:
            coin.kill()
            self.game_info['coin'] += 1

    def adjust_player_x(self, sprite):
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            self.player.rect.left = sprite.rect.right
        self.player.x_vel = 0

    def adjust_player_y(self, sprite):
        # 从下往上
        if self.player.rect.bottom >= sprite.rect.bottom:
            self.player.y_vel = 7
            self.player.rect.top = sprite.rect.bottom 
            self.player.state = 'fall'

        # 从上往下
        else:
            self.player.y_vel = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'

    def check_will_fall(self, sprite):
        sprite.rect.y += 1
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        m = pygame.sprite.spritecollideany(sprite, check_group)
        if not m and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -=1

    def update_window_position(self):  # 窗口滑动代替主角移动
        third = self.game_window.x + self.game_window.width*1/3
        if self.player.rect.right > third and self.player.x_vel > 0 and self.game_window.right < self.end_x:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def draw(self, surface):
        self.bg.blit(self.BG, self.game_window, self.game_window)  # （目标图层，目标图层的左上角放到原图层的位置，特定部分）
        self.bg.blit(self.player.image, self.player.rect)
        self.brick_group.draw(self.bg)
        self.box_group.draw(self.bg)
        self.enemy_group.draw(self.bg)
        self.dying_group.draw(self.bg)
        self.coin_group.draw(self.bg)

        surface.blit(self.bg, (0, 0),self.game_window)

        self.info.start(self.game_info)
        self.info.update()
        self.info.draw(surface)

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next_state = 'game_over'
        else:
            self.next_state = 'load_screen'

    def check_checkpoint(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill()