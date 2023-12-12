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
            if self.loop:
                self.current_frame = 0
            else:
                self.kill()


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
            if self.loop:
                self.current_frame = 0
            else:
                self.kill()


class Damage(Effect):
    def __init__(self, group, pos, lifetime, font_path, font_size, text="", text_color="#ffffff"):
        pygame.sprite.Sprite.__init__(self, group)
        self.camera = group
        self.depth = 5
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.font = pygame.font.Font(font_path, int(font_size))

        _circle_cache = {}

        def _circlepoints(r):
            r = int(round(r))
            if r in _circle_cache:
                return _circle_cache[r]
            x, y, e = r, 0, 1 - r
            _circle_cache[r] = points = []
            while x >= y:
                points.append((x, y))
                y += 1
                if e < 0:
                    e += 2 * y - 1
                else:
                    x -= 1
                    e += 2 * (y - x) - 1
            points += [(y, x) for x, y in points if x > y]
            points += [(-x, y) for x, y in points if x]
            points += [(x, -y) for x, y in points if y]
            points.sort()
            return points

        def render(text, font, gfcolor="#ffffff", ocolor="#000000", opx=1):
            textsurface = font.render(text, True, gfcolor).convert_alpha()
            w = textsurface.get_width() + 2 * opx
            h = font.get_height()

            osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
            osurf.fill((0, 0, 0, 0))

            surf = osurf.copy()

            osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

            for dx, dy in _circlepoints(opx):
                surf.blit(osurf, (dx + opx, dy + opx))

            surf.blit(textsurface, (opx, opx))
            return surf

        self.image = render(text, self.font, text_color, "#222222", 2)
        self.rect = self.image.get_rect()
        self.rect.center = self.rect.move(pos).topleft

    def update(self):
        if self.lifetime <= self.max_lifetime / 2:
            self.image.set_alpha(255 * (self.lifetime / (self.max_lifetime / 2)))
        self.lifetime -= 1
        self.rect.y -= 1.2

        if self.lifetime <= 0:
            self.kill()
