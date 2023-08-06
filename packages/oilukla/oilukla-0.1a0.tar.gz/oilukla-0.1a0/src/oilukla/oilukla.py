import pygame
import keyboard
import sys

una_w = 0
una_h = 0
running = True

key_put = keyboard.is_pressed

loc_ver = '0.1_a'
w_window = pygame.display.set_mode

class window():
    def __init__(self, width, height, title, bg_color, fps, icon):
        global una_w, una_h

        pygame.init()

        self.fps = fps

        self.bg_color = bg_color

        self.w = width
        self.h = height
        self.title = title
        self.icon = icon
        
        una_w = self.w
        una_h = self.h

        self.clocker = pygame.time.Clock()
        self.window = w_window((self.w, self.h))

        self.window.fill(self.bg_color)

        if self.title == '':
            pygame.display.set_caption('Oilukla2D - ' + loc_ver)
        else:
            pygame.display.set_caption(self.title)

        if self.icon != None:
            w_icon = pygame.image.load(self.icon)
            pygame.display.set_icon(w_icon)

        pygame.display.flip()

    def w_name(self, nname):
        pygame.display.set_caption(nname)

    def w_update(self):
        pygame.display.update()
        self.clocker.tick(self.fps)

    def w_clear(self):
        self.window((self.w, self.h)).fill(self.bg_color)

    def w_close(self):
        global running

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

class entity():
    def __init__(self, sprite):
        self.sprite = sprite
        self.spr_surf = pygame.image.load(self.sprite)

    def transform(self, x, y):
        w_window((una_w, una_h)).blit(self.spr_surf, (x ,y))

    def scale_up(self, nx, ny):
        self.spr_surf = pygame.transform.scale(self.spr_surf, (nx, ny))

