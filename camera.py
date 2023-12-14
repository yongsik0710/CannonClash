from particle import *
from config import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self, background):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.particle_smoke = Particle.Smoke(self.display_surface)
        self.particle_destroy = Particle.Destroy(self.display_surface)
        self.particle_flame = Particle.Flame(self.display_surface)

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 150, 'right': 150, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # ground
        self.ground_surf = background
        self.ground_surf = pygame.transform.scale(self.ground_surf, (1920 + 1240, 1080 + 460))
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # camera speed
        self.keyboard_speed = 17
        self.mouse_speed = 0.2

        # target
        self.target = None

    def center_target_camera(self):
        self.offset.x = self.target.rect.centerx - self.half_w
        self.offset.y = self.target.rect.centery - self.half_h

    def center_target_camera_align(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.offset.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.offset.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.offset.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.offset.y += self.keyboard_speed

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border

        self.offset.x += mouse_offset_vector[0] * self.mouse_speed
        self.offset.y += mouse_offset_vector[1] * self.mouse_speed

    def out_of_border(self):
        if self.offset.x > 4400 - 1920:
            self.offset.x = 4400 - 1920
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.y > 2000 - 1080:
            self.offset.y = 2000 - 1080
        if self.offset.y < 0:
            self.offset.y = 0

    def custom_draw(self):

        if self.target is not None:
            self.center_target_camera()
        else:
            if option["util"]["keyboard_camera"]:
                self.keyboard_control()
            if option["util"]["mouse_camera"]:
                self.mouse_control()

        self.out_of_border()

        self.display_surface.fill('#000000')

        # ground
        ground_offset = self.ground_rect.topleft - (self.offset / 2)
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.depth):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # particle
        self.particle_smoke.emit(self.offset)
        self.particle_destroy.emit(self.offset)
        self.particle_flame.emit(self.offset)
