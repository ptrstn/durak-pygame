import sys

import pygame

from durakui.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    FRAMES_PER_SECOND,
)
from durakui.table import DurakTable


class DurakView:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = False
        self.table = DurakTable()

    def run(self):
        click_counter = 0
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    from durakui.mocks import mock_table_action

                    mock_table_action(self.table, click_counter)
                    click_counter += 1
                if event.type == pygame.MOUSEWHEEL:
                    self.table.reset()
                    click_counter = 0

            self.table.update()
            self.table.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)


def main():
    view = DurakView()
    view.run()


if __name__ == "__main__":
    main()
