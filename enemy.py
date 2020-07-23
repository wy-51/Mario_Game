import pygame
from SUPERMARIO静止画面 import tools, setup
from.import constant as c

def create_enemy(enemy_data):
    enemy_type = enemy_data['type']
    x, y_bottom, direction, color = enemy_data['x'], enemy_data['y'], enemy_data['direction'], enemy_data['color']
    if enemy_type == 0:
        enemy = Goomba(x, y_bottom, direction, 'goomba', color)
    elif enemy_type == 1:
        enemy = Koopa(x, y_bottom, direction, 'koopa', color)

    return enemy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y_bottom, direction, name, frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.name = name
        self.frame_index = 0
        self.left_frames = []
        self.right_frames = []

        self.load_frames(frame_rects)
        self.frames = self.left_frames if self.direction == 0 else self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y_bottom

        self.timer = 0
        self.x_vel = -1*c.ENEMY_SPEED if self.direction == 0 else c.ENEMY_SPEED
        self.y_vel = 0
        self.gravity = c.GRAVITY
        self.state = 'walk'

    def load_frames(self, frame_rects):
        for frame_rect in frame_rects:
            left_frame = tools.load_image('D:\\game\Mario\\resources\\graphics\\enemies.png', *frame_rect, (220, 0, 255), c.ENEMY_SCALE, rgb = (220, 0, 255))
            right_frame = pygame.transform.flip(left_frame, True, False)
            self.left_frames.append(left_frame)
            self.right_frames.append(right_frame)

    def update(self, level):
        self.current_time = pygame.time.get_ticks()
        self.handle_states()
        self.update_position(level)

    def handle_states(self):
        if self.state == 'walk':
            self.walk()

        elif self.state == 'fall':
            self.fall()
        elif self.state == 'die':
            self.die()

        elif self.state == 'trampled':
            self.trampled()

        if self.direction:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def walk(self):
        if self.current_time - self.timer > 125:
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time

    def fall(self):
        if self.y_vel < 10:
            self.y_vel += self.gravity

    def die(self):
        self.rect.x += self.x_vel
        self.y_vel += self.gravity
        self.rect.y += self.y_vel
        if self.rect.y > c.SCREEN_H:
            self.kill()

    def trampled(self):
        self.x_vel = 0
        self.frame_index = 2
        if self.death_timer == 0:
            self.death_timer = self.current_time
        if self.current_time - self.death_timer > 1000:
            self.kill()

    def update_position(self, level):
        self.rect.x += self.x_vel
        self.check_x_collision(level)
        self.rect.y += self.y_vel
        if self.state != 'die':
            self.check_y_collision(level)

    def check_x_collision(self, level):
        sprite = pygame.sprite.spritecollideany(self, level.ground_items_group)
        if sprite:
            self.direction = 1 if self.direction == 0 else 0
            self.x_vel *= -1

    def check_y_collision(self, level):
        check_group = pygame.sprite.Group(level.ground_items_group, level.box_group, level.brick_group)
        sprite = pygame.sprite.spritecollideany(self, check_group)
        if sprite:
            if self.rect.top < sprite.rect.top:
                self.rect.bottom = sprite.rect.top
                self.y_vel = 0
                self.state = 'walk'

        level.check_will_fall(self)

    def go_die(self, how):
        self.death_timer = self.current_time
        # 顶起即死亡
        if how == 'bumped':
            self.y_vel = -8
            self.gravity = 0.6
            self.state = 'die'
            self.frame_index = 0

        elif how == 'trampled':
            self.state = 'trampled'

class Goomba(Enemy):
    def __init__(self, x, y_bottom, direction, name, color):
        bright_rect_frames = [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)]
        dark_rect_frames = [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 16)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = dark_rect_frames

        Enemy.__init__(self, x, y_bottom, direction, name, frame_rects)


class Koopa(Enemy):
    def __init__(self, x, y_bottom, direction, name, color):
        bright_rect_frames = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
        dark_rect_frames = [(96, 72, 16, 22), (112, 72, 16, 22), (160, 72, 16, 22)]

        if not color:
            frame_rects = bright_rect_frames
        else:
            frame_rects = dark_rect_frames

        Enemy.__init__(self, x, y_bottom, direction, name, frame_rects)