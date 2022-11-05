import pygame as pg
import settings
from pathlib import Path
import numpy as np
import definitions
import math

SpritesDir = Path(definitions.ROOT_DIR) / 'resources' / 'sprites'


class SpriteObject:
    def __init__(self, game, path: str | Path, pos: tuple[float, float], scale: float, shift: float):
        self.path = path
        self.pos = pos
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_half_width = self.image.get_width() // 2
        self.image_ratio = self.image_width / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.sprite_scale = scale
        self.sprite_height_shift = shift

    def get_sprite_projection(self):
        proj = settings.SCREEN_DIST / self.norm_dist * self.sprite_scale
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.sprite_height_shift
        pos = self.screen_x - self.sprite_half_width, settings.HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = np.arctan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > np.pi) or (dx < 0 and dy < 0):
            delta += 2 * np.pi

        delta_rays = delta / settings.DELTA_ANGLE
        self.screen_x = (settings.HALF_NUM_RAYS + delta_rays) * settings.SCALE

        self.dist = np.hypot(dx, dy)
        self.norm_dist = self.dist * np.cos(delta)
        if -self.image_half_width < self.screen_x < (settings.WIDTH + self.image_half_width) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class CandleBra(SpriteObject):
    def __init__(self, game):
        super(CandleBra, self).__init__(game=game,
                                        path=SpritesDir / 'static_sprites' / 'candlebra.png',
                                        pos=(10.5, 4.5),
                                        scale=0.7,
                                        shift=0.27)
