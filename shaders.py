import pygame
import collections

class BlurShader:
    amount = 0

    def __init__(this, amount):
        this.amount = amount

    def apply(this, surface):
        scale = 1.0/float(this.amount)
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
        blurred = pygame.transform.smoothscale(surface, scale_size)
        blurred = pygame.transform.smoothscale(blurred, surf_size)
        blurred.set_alpha(100)
        
        surface.blit(blurred, (0,0))
        return surface

class OverlayShader:

    def __init__(this, tileSurface):
        this.tile = tileSurface

    def apply(this, surface):

        
        tile_size = this.tile.get_size()
        surf_size = surface.get_size()
        x_copies = int(surf_size[0] / tile_size[0])
        y_copies = int(surf_size[1] / tile_size[1])

        tmpSurface = pygame.Surface(surf_size)
        for y_idx in range(y_copies):
            for x_idx in range(x_copies):
                tmpSurface.blit(this.tile, (x_idx * tile_size[0], y_idx * tile_size[1]), special_flags=pygame.BLEND_ADD)
        tmpSurface.set_alpha(7)
        
        surface.blit(tmpSurface, (0,0))
        return surface