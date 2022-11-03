import settings
import pygame as pg
import numpy as np


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = settings.PLAYER_POS
        self.angle = settings.PLAYER_ANGLE

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_post(self):
        """ Get tile of the map"""
        return int(self.x), int(self.y)

    def movement(self):
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)
        speed = settings.PLAYER_SPEED * self.game.delta_time
        self._move_by_key_press(
            dx=0,
            dy=0,
            speed_sin=speed * sin_a,
            speed_cos=speed * cos_a
        )

    def _move_by_key_press(self, dx, dy, speed_sin, speed_cos):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= settings.PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += settings.PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= np.pi * 2  # rotation

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 * settings.WIDTH * np.cos(self.angle),
                      (self.y * 100 * settings.WIDTH * np.sin(self.angle))))
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy
