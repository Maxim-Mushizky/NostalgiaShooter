import pygame as pg
import sys
import settings
from nostalgic_shooter.maps import map_creator, level_one, secret_level
from nostalgic_shooter.player import Player
import nostalgic_shooter.game_engine as ge
from nostalgic_shooter.object_renderer import ObjectRenderer
from nostalgic_shooter.sprite_objects import CandleBra


def quit_requested(event):
    return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(settings.RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.player = None
        self.map = None
        self.new_game()

    def new_game(self):
        self.map = map_creator.MapCreator(self, level_one.mini_map)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = ge.RayCasting(self)
        self.candle_bra = CandleBra(self)

    def update(self):
        """
        Update Screen and display current no' of FPS
        """
        self.player.update()
        self.raycasting.update()
        self.candle_bra.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(settings.FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if quit_requested(event):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
