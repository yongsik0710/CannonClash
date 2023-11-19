import pygame


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# class Button:
#     def __init__(self, surface, x, y, width, height, font, buttonText='Button', onclickFunction=None, onePress=True):
#         self.surface = surface
#         self.x = x - int(width / 2)
#         self.y = y - int(height / 2)
#         self.width = width
#         self.height = height
#         self.font = font
#         self.onclickFunction = onclickFunction
#         self.onePress = onePress
#         self.alreadyPressed = False
#
#         self.fillColors = {
#             'normal': '#ffffff',
#             'hover': '#666666',
#             'pressed': '#333333',
#         }
#         self.buttonSurface = pygame.Surface((self.width, self.height))
#         self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
#
#         self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
#
#         # objects.append(self)
#
#     def process(self):
#         mousePos = pygame.mouse.get_pos()
#         self.buttonSurface.fill(self.fillColors['normal'])
#         if self.buttonRect.collidepoint(mousePos):
#             self.buttonSurface.fill(self.fillColors['hover'])
#             if pygame.mouse.get_pressed(num_buttons=3)[0]:
#                 self.buttonSurface.fill(self.fillColors['pressed'])
#                 if self.onePress:
#                     self.onclickFunction()
#                 elif not self.alreadyPressed:
#                     self.onclickFunction()
#                     self.alreadyPressed = True
#             else:
#                 self.alreadyPressed = False
#
#         self.buttonSurface.blit(self.buttonSurf, [
#             self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
#             self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
#         ])
#         self.surface.blit(self.buttonSurface, self.buttonRect)