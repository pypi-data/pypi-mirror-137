#!/usr/bin/env python3

from typing import Optional

import pygame

from .color import calc_alpha
from .constants import ODD_CIRCLE_CACHE, EVEN_CIRCLE_CACHE, RECT_CACHE, ALL_CACHES
from .mathf import get_i, Pos
from .type_hints import _pos, _col_type

pygame.init()

even_circle_cache = {}
odd_circle_cache = {}
rect_cache = {}


def clear_cache(caches: int = ALL_CACHES) -> None:
    """
    clear_cache(caches: int)

    Type: function

    Description: empties the caches of the draw functions, aa_line
        not included

    Args:
        'cashes' (int) specify what caches should be cleared, you can
            pass any combination of RECT_CACHE, EVEN_CIRCLE_CACHE and
            ODD_CIRCLE_CACHE separated by `|`

    Return type: None
    """
    if caches & ODD_CIRCLE_CACHE:
        odd_circle_cache.clear()
    if caches & EVEN_CIRCLE_CACHE:
        even_circle_cache.clear()
    if caches & RECT_CACHE:
        rect_cache.clear()


def even_circle(surface: Optional[pygame.Surface],
                center: _pos,
                radius: int,
                color: _col_type,
                border: int = 0,
                border_color: Optional[_col_type] = None) -> pygame.Surface:
    """
    even_circle(surface: pygame.Surface,
                center: _pos,
                radius: int,
                color: _col_type,
                border: int,
                border_color: Optional[_col_type])

    Type: function

    Description: draws a circle with a 2x2 center and returns a surface
        containing it, the same surface is blit onto the target surface
        if given

    Args:
        'surface' (pygame.Surface?): where the circle should be drawn
        'center' (pgt.Pos): where the top-left pixel of the center should
            be on the surface
        'radius' (int): radius of the circle
        'color' (tuple, list): the color of the circle
        'border' (int): the thickness of the border, if 0 the border
            is not drawn
        'border_color' (tuple, list): the color of the border, can be
            omitted if border == 0

    Return type: pygame.Surface
    """

    blit_pos = (center[0] - radius, center[1] - radius)
    radius = round(radius)
    if radius - border < 0: border = radius

    key = (radius, color, border, border_color)

    surf = even_circle_cache.get(key, None)
    if surface is not None and surf is not None:
        surface.blit(surf, blit_pos)
        return surf

    new_surf = pygame.Surface((radius*2, radius*2), flags=pygame.SRCALPHA)
    new_surf.set_colorkey((0, 0, 0))
    alpha_col = len(color) == 4
    alpha_b_col = border_color and len(border_color) == 4
    inner_radius = radius - border

    for x in range(radius):
        for y in range(radius):
            inv_x = radius*2 - x - 1
            inv_y = radius*2 - y - 1

            distance = get_i(x - radius, y - radius)

            if distance < inner_radius:
                new_surf.set_at((x, y), color)
                new_surf.set_at((inv_x, y), color)
                new_surf.set_at((x, inv_y), color)
                new_surf.set_at((inv_x, inv_y), color)

            elif border and distance < inner_radius + 1:
                alpha = 1 - (distance-inner_radius)
                new_color = calc_alpha(color, border_color, alpha)
                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

            elif distance < radius:
                new_surf.set_at((x, y), border_color)
                new_surf.set_at((inv_x, y), border_color)
                new_surf.set_at((x, inv_y), border_color)
                new_surf.set_at((inv_x, inv_y), border_color)

            elif distance < radius + 1:
                if border:
                    alpha = (border_color[3] if alpha_b_col else 255) * (1 - (distance - radius))
                    new_color = list(border_color[:3])
                else:
                    alpha = (color[3] if alpha_col else 255) * (1 - (distance - radius))
                    new_color = list(color[:3])
                new_color.append(alpha)

                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

    if surface is not None: surface.blit(new_surf, blit_pos)
    even_circle_cache[key] = new_surf
    return new_surf


def odd_circle(surface: Optional[pygame.Surface],
               center: _pos,
               radius: int,
               color: _col_type,
               border: int = 0,
               border_color: Optional[_col_type] = None) -> pygame.Surface:
    """
    odd_circle(surface: pygame.Surface,
               center: _pos,
               radius: int,
               color: _col_type,
               border: int,
               border_color: Optional[_col_type])

    Type: function

    Description: draws a circle with a 1x1 center and returns a surface
        containing it, the same surface is blit onto the target surface
        if given

    Args:
        'surface' (pygame.Surface?): where the circle should be drawn
        'center' (pgt.Pos): where the center should be on the surface
        'radius' (int): radius of the circle
        'color' (tuple, list): the color of the circle
        'border' (int): the thickness of the border, if 0 the border
            is not drawn
        'border_color' (tuple, list): the color of the border, can be
            omitted if border == 0

    Return type: pygame.Surface
    """
    blit_pos = (center[0] - radius, center[1] - radius)
    radius = round(radius)
    if radius - border < 0: border = radius

    key = (radius, color, border, border_color)

    surf = odd_circle_cache.get(key, None)
    if surface is not None and surf is not None:
        surface.blit(surf, blit_pos)
        return surf

    size = ((radius+1)*2, (radius+1)*2)

    new_surf = pygame.Surface(size, flags=pygame.SRCALPHA)
    new_surf.set_colorkey((0, 0, 0))
    alpha_col = len(color) == 4
    alpha_b_col = border_color and len(border_color) == 4
    inner_radius = radius - border

    for x in range(radius):
        for y in range(radius):
            inv_x = radius*2 - x
            inv_y = radius*2 - y

            distance = get_i(x - radius, y - radius)

            if distance < inner_radius:
                new_surf.set_at((x, y), color)
                new_surf.set_at((inv_x, y), color)
                new_surf.set_at((x, inv_y), color)
                new_surf.set_at((inv_x, inv_y), color)

            elif border and distance < inner_radius + 1:
                alpha = 1 - (distance-inner_radius)
                new_color = calc_alpha(color, border_color, alpha)
                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

            elif distance < radius:
                new_surf.set_at((x, y), border_color)
                new_surf.set_at((inv_x, y), border_color)
                new_surf.set_at((x, inv_y), border_color)
                new_surf.set_at((inv_x, inv_y), border_color)

            elif distance < radius + 1:
                if border:
                    alpha = (border_color[3] if alpha_b_col else 255) * (1 - (distance - radius))
                    new_color = list(border_color[:3])
                else:
                    alpha = (color[3] if alpha_col else 255) * (1 - (distance - radius))
                    new_color = list(color[:3])
                new_color.append(alpha)

                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

    if border:
        pygame.draw.line(new_surf, border_color, (radius, 0), (radius, radius*2))
        pygame.draw.line(new_surf, border_color, (0, radius), (radius*2, radius))
    pygame.draw.line(new_surf, color, (radius, border), (radius, radius*2 - border))
    pygame.draw.line(new_surf, color, (border, radius), (radius*2 - border, radius))

    if surface is not None: surface.blit(new_surf, blit_pos)
    odd_circle_cache[key] = new_surf
    return new_surf


def aa_rect(surface: Optional[pygame.Surface],
            rect: pygame.Rect,
            color: _col_type,
            corner_radius: int = 0,
            border: int = 0,
            border_color: Optional[_col_type] = None) -> pygame.Surface:
    """
    aa_rect(surface: pygame.Surface,
            rect: pygame.Rect,
            color: _col_type,
            corner_radius: int,
            border: int,
            border_color: Optional[_col_type])

    Type: function

    Description: draws a rect like pygame.draw.rect but anti-aliasing
        the corners and returns a surface containing it, the same
        surface is blit onto the target surface if given

    Args:
        'surface' (pygame.Surface?): where the rect should be drawn
        'rect' (pygame.Rect): the rectangle to draw
        'color' (list, tuple): the color of the rectangle
        'corner_radius' (int): the radius of the curvature of the
            corners
        'border' (int): the thickness of the border, if 0 the border
            is not drawn
        'border_color' (tuple, list): the color of the border, can be
            omitted if border == 0

    Return type: pygame.Surface
    """
    corner_radius = round(corner_radius)
    if corner_radius > min(rect.width, rect.height) / 2:
        corner_radius = int(min(rect.width, rect.height) / 2)

    if border > min(rect.width, rect.height) / 2:
        border = int(min(rect.width, rect.height) / 2)

    key = (rect.size, color, corner_radius, border, border_color)

    surf = rect_cache.get(key, None)
    if surface is not None and surf is not None:
        surface.blit(surf, rect.topleft)
        return surf

    new_surf = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
    new_surf.set_colorkey((0, 0, 0))
    alpha_col = len(color) == 4
    alpha_b_col = border_color and len(border_color) == 4
    line_rect = pygame.Rect(0, 0, rect.w, rect.h)
    inner_rect = pygame.Rect(border, border, rect.w - border*2, rect.h - border*2)

    inner_radius = corner_radius - border

    if border:
        pygame.draw.rect(new_surf, border_color, line_rect, 0, corner_radius)
    pygame.draw.rect(new_surf, color, inner_rect, 0, inner_radius)

    for x in range(corner_radius):
        for y in range(corner_radius):
            inv_x = rect.w - x - 1
            inv_y = rect.h - y - 1

            distance = get_i(x - corner_radius, y - corner_radius)

            if distance < inner_radius:
                new_surf.set_at((x, y), color)
                new_surf.set_at((inv_x, y), color)
                new_surf.set_at((x, inv_y), color)
                new_surf.set_at((inv_x, inv_y), color)

            elif border and distance < inner_radius + 1:
                alpha = 1 - (distance-inner_radius)
                new_color = calc_alpha(color, border_color, alpha)
                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

            elif distance < corner_radius:
                new_surf.set_at((x, y), border_color)
                new_surf.set_at((inv_x, y), border_color)
                new_surf.set_at((x, inv_y), border_color)
                new_surf.set_at((inv_x, inv_y), border_color)

            elif distance < corner_radius + 1:
                if border:
                    alpha = (border_color[3] if alpha_b_col else 255) * (1 - (distance - corner_radius))
                    new_color = list(border_color[:3])
                else:
                    alpha = (color[3] if alpha_col else 255) * (1 - (distance - corner_radius))
                    new_color = list(color[:3])
                new_color.append(alpha)

                new_surf.set_at((x, y), new_color)
                new_surf.set_at((inv_x, y), new_color)
                new_surf.set_at((x, inv_y), new_color)
                new_surf.set_at((inv_x, inv_y), new_color)

    if surface is not None: surface.blit(new_surf, rect.topleft)
    rect_cache[key] = new_surf
    return new_surf


def aa_line(surface: pygame.Surface,
            color: _col_type,
            start_pos: _pos,
            end_pos: _pos,
            width: int = 1) -> None:
    """
    aa_line(surface: pygame.Surface,
            color: _col_type,
            start_pos: _pos,
            end_pos: _pos,
            width: int)

    Type: function

    Description: draws an anti-aliased line that can be thicker than
        one pixel

    Args:
        'surface' (pygame.Surface): the surface where to draw the line
        'color' (list, tuple): the color of the line
        'start_pos' (pgt.Pos): the position of the first point
        'end_pos' (pgt.Pos): the position of the second point
        'width' (int): the width of the line (can only be an odd number)

    Return type: None
    """
    if width <= 0: return
    # The line doesn't look good with an even width
    if not width % 2: width += 1

    start_pos = Pos(start_pos)
    end_pos = Pos(end_pos)
    horizontal = abs(start_pos.x - end_pos.x) <= abs(start_pos.y - end_pos.y)

    pygame.draw.line(surface, color, start_pos, end_pos, width)
    line_offset = (width / 2, 0) if horizontal else (0, width / 2)
    pygame.draw.aaline(surface, color, start_pos + line_offset, end_pos + line_offset)
    pygame.draw.aaline(surface, color, start_pos - line_offset, end_pos - line_offset)
