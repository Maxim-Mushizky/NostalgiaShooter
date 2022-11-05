import pygame as pg
import settings
import definitions
from pathlib import Path

TexturesDir = Path(definitions.ROOT_DIR) / 'resources' / 'textures'


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(TexturesDir / 'sky.png', (settings.WIDTH, settings.HALF_HEIGHT))
        self.sky_offset = 0

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        self.sky_offset = (self.sky_offset * 4.5 * self.game.player.rel) % settings.WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset * settings.WIDTH, 0))
        pg.draw.rect(self.screen, settings.FLOOR_COLOR, (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(settings.TEXTURE_SIZE, settings.TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture(TexturesDir / '1.png'),
            2: self.get_texture(TexturesDir / '2.png'),
            3: self.get_texture(TexturesDir / '3.png'),
            4: self.get_texture(TexturesDir / '4.png'),
            5: self.get_texture(TexturesDir / '5.png')
        }
