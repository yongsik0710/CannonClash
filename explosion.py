from config import *
from spritesheet import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, group, pos, owner):
        pygame.sprite.Sprite.__init__(self, group)
        self.depth = 4
        self.owner = owner
        self.camera = group
        self.sprites = SpriteSheet(TexturePath.Effects.explosion, 7, 0.125).sprites
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft
        self.animation_speed = 0.3

    def update(self):
        # update explosion animation
        self.image = self.sprites[int(self.current_frame)]
        self.current_frame += self.animation_speed

        # if the animation is complete, reset animation index
        if int(self.current_frame) >= len(self.sprites):
            self.camera.target = None
            self.kill()
            pygame.time.wait(100)
            self.owner.next_turn()
