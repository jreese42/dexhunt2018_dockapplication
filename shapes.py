import pygame
import colors

color_green = (0, 255, 0)
class BorderRect:
    def __init__(this, w, h, thicc):
        this.w = w
        this.h = h
        this.thicc = thicc

    def draw(this, screen, x, y):
        pygame.draw.line(screen, colors.green_fg, [x, y], [x+this.w, y], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y], [x+this.w, y+this.h], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y+this.h], [x, y+this.h], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x, y+this.h], [x, y], this.thicc)

class SolidRect:
    def __init__(this, w, h, thicc):
        this.w = w
        this.h = h
        this.thicc = thicc

    def draw(this, screen, x, y):
        rect = pygame.Rect(x, y, this.w, this.h)
        pygame.draw.rect(screen, colors.green_bg, rect)
        pygame.draw.line(screen, colors.green_fg, [x, y], [x+this.w, y], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y], [x+this.w, y+this.h], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y+this.h], [x, y+this.h], this.thicc)
        pygame.draw.line(screen, colors.green_fg, [x, y+this.h], [x, y], this.thicc)