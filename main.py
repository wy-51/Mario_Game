from SUPERMARIO静止画面 import main_menu
from SUPERMARIO静止画面 import tools, setup, load_screen, level


def main():
    state_dict = {'main_menu': main_menu.MainMenu(), 'load_screen': load_screen.LoadScreen(), 'level': level.Level(), 'game_over': load_screen.GameOver()}
    # state = level.Level()
    # state = main_menu.MainMenu()
    # state = load_screen.LoadScreen()
    game = tools.Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()