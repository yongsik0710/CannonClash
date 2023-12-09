from spritesheet import *


class Effect(pygame.sprite.Sprite):
    def __init__(self, group, pos, image, frame, scale, speed, loop=False):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 4
        self.sprite_sheet = SpriteSheet(image, frame)
        self.current_frame = 0
        self.animation_speed = speed
        self.scale = scale
        self.loop = loop

        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

    def update(self):
        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.current_frame += self.animation_speed

        if int(self.current_frame) >= self.sprite_sheet.frame:
            if self.loop: self.current_frame = 0
            else: self.kill()


class Explosion(Effect):
    def __init__(self, group, pos, image, scale, owner):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 4
        self.owner = owner
        self.sprite_sheet = SpriteSheet(image, 7)
        self.current_frame = 0
        self.animation_speed = 0.3
        self.scale = scale

        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

    def update(self):
        self.image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.current_frame += self.animation_speed

        if int(self.current_frame) >= self.sprite_sheet.frame:
            self.kill()
            pygame.time.wait(100)
            self.camera.target = None
            self.owner.next_turn()
