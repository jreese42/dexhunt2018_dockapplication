import pygame
import colors

color_green = (0, 255, 0)
class BorderRect:
    def __init__(this, w, h):
        this.w = w
        this.h = h

    def draw(this, screen, x, y, thicc):
        pygame.draw.line(screen, colors.green_fg, [x, y], [x+this.w, y], thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y], [x+this.w, y+this.h], thicc)
        pygame.draw.line(screen, colors.green_fg, [x+this.w, y+this.h], [x, y+this.h], thicc)
        pygame.draw.line(screen, colors.green_fg, [x, y+this.h], [x, y], thicc)