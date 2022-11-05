import pygame as pg
import numpy as np

_ = False


class MapCreator:
    def __init__(self, game, mini_map):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        """
        Create mini map dictionary with keys being coordinates of none False values
        :return:
        """
        self.world_map = {(j, i): np.array(self.mini_map)[i, j] for i, j in
                          zip(*np.where(np.array(self.mini_map) != False))}

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgrey', (pos[0] * 100, pos[1] * 100, 100, 100), 2) for pos in
         self.world_map]
