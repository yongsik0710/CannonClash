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
    def __init__(self, group, pos, image, frame, scale, speed, owner):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 4
        self.owner = owner
        self.sprite_sheet = SpriteSheet(image, frame)
        self.current_frame = 0
        self.animation_speed = speed
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


class Fire(Effect):
    def __init__(self, group, cannon, pos, image, frame, scale, speed, loop=False):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 4
        self.cannon = cannon
        self.sprite_sheet = SpriteSheet(image, frame)
        self.current_frame = 0
        self.animation_speed = speed
        self.scale = scale
        self.loop = loop

        image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.image = pygame.transform.rotate(image, -90)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

    def update(self):
        self.rect.center = self.cannon.rect.center
        self.rect = self.rect.move(0, -25)
        image = self.sprite_sheet.get_image(int(self.current_frame), self.scale)
        self.image = pygame.transform.rotate(image, -90)
        self.current_frame += self.animation_speed

        if int(self.current_frame) >= self.sprite_sheet.frame:
            if self.loop: self.current_frame = 0
            else: self.kill()


class Damage(Effect):
    def __init__(self, group, pos, lifetime, font_path, font_size, text="", text_color="#ffffff"):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 5
        self.lifetime = lifetime
        self.font = pygame.font.Font(font_path, int(font_size))

        self.image = self.font.render(text, True, text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

    def update(self):
        self.lifetime -= 1
        self.rect.y -= 1.2

        if self.lifetime <= 0:
            self.kill()
