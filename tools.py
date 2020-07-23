import pygame


class Game:
    def __init__(self, state_dict, state):
        self.state_dict = state_dict
        self.state = self.state_dict[state]
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()  # 初始化时间对象
        self.keys = pygame.key.get_pressed()  # pygame.key.get_pressed()返回一个1-0列表
        pygame.display.set_caption('SUPERMARIO')

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            self.state.finished = False
            next = self.state.next_state
            self.state = self.state_dict[next]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            self.update()
            pygame.display.update()  # 刷新
            self.clock.tick(40)


def load_image(path, x, y, width, height, colorkey, scale, rgb=(0, 0, 0)):
    img = pygame.Surface((width, height))  # 创建一个默认黑色与抠图对象大小相同的surface对象
    img.fill(rgb)
    img.set_colorkey(colorkey)  # 针对colorkey传入色调整
    image = pygame.image.load(path)
    img.blit(image, (0, 0), (x, y, width, height))  # 裁剪

    img = pygame.transform.scale(img, (int(width*scale), int(height*scale)))
    return img