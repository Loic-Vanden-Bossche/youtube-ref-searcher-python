import sys

import pygame


from src.main_menu import MainMenu


class Game(MainMenu):
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        super().__init__()

        self.level = Level(1, ['bernard', 'francois', 'vincent'])

    def run(self):
        # channel_id = 'UCQVaKQcp4OxSg1eC6SF3NTw'
        # loader.loading_loop(channel_id)
        # loader.channel_menu_loop(channel_id)

        while True:
            time_delta = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.level.input(event)

            self.screen.fill('black')
            self.level.run(time_delta)
            pygame.display.update()


def main():
    # Palmashow : UCoZoRz4-y6r87ptDp4Jk74g
    # Les kassos : UCv88958LRDfndKV_Y7XmAnA
    # Wankil Studio : UCYGjxo5ifuhnmvhPvCc3DJQ
    # JDG : UC_yP2DpIgs5Y1uWC0T03Chw

    Game().run()


if __name__ == "__main__":
    main()
