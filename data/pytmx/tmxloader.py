import itertools
import os

import pygame

from data.pytmx import pytmx
from .constants import *


__all__ = ['load_pygame', 'load_tmx']


def handle_transformation(tile, flags):
    if flags:
        fx = flags & TRANS_FLIPX == TRANS_FLIPX
        fy = flags & TRANS_FLIPY == TRANS_FLIPY
        r = flags & TRANS_ROT == TRANS_ROT

        if r:
            # not sure why the flip is required...but it is.
            newtile = pygame.transform.rotate(tile, 270)
            newtile = pygame.transform.flip(newtile, 1, 0)

            if fx or fy:
                newtile = pygame.transform.flip(newtile, fx, fy)

        elif fx or fy:
            newtile = pygame.transform.flip(tile, fx, fy)

        return newtile

    else:
        return tile


def smart_convert(original, colorkey, force_colorkey, pixelalpha):
    """
    this method does several tests on a surface to determine the optimal
    flags and pixel format for each tile surface.

    this is done for the best rendering speeds and removes the need to
    convert() the images on your own
    """
    tile_size = original.get_size()

    # count the number of pixels in the tile that are not transparent
    px = pygame.mask.from_surface(original).count()

    # there are no transparent pixels in the image
    if px == tile_size[0] * tile_size[1]:
        tile = original.convert()

    # there are transparent pixels, and set to force a colorkey
    elif force_colorkey:
        tile = pygame.Surface(tile_size)
        tile.fill(force_colorkey)
        tile.blit(original, (0, 0))
        tile.set_colorkey(force_colorkey, pygame.RLEACCEL)

    # there are transparent pixels, and tiled set a colorkey
    elif colorkey:
        tile = original.convert()
        tile.set_colorkey(colorkey, pygame.RLEACCEL)

    # there are transparent pixels, and set for perpixel alpha
    elif pixelalpha:
        tile = original.convert_alpha()

    # there are transparent pixels, and we won't handle them
    else:
        tile = original.convert()

    return tile


def _load_images_pygame(tmxdata, mapping, *args, **kwargs):
    """
    Utility function to load images.


    due to the way the tiles are loaded, they will be in the same pixel format
    as the display when it is loaded.  take this into consideration if you
    intend to support different screen pixel formats.

    by default, the images will not have per-pixel alphas.  this can be
    changed by including "pixelalpha=True" in the keywords.  this will result
    in much slower blitting speeds.

    if the tileset's image has colorkey transparency set in Tiled, the loader
    will return images that have their transparency already set.  using a
    tileset with colorkey transparency will greatly increase the speed of
    rendering the map.

    optionally, you can force the loader to strip the alpha channel of the
    tileset image and to fill in the missing areas with a color, then use that
    new color as a colorkey.  the resulting tiles will render much faster, but
    will not preserve the transparency of the tile if it uses partial
    transparency (which you shouldn't be doing anyway, this is SDL).

    TL;DR:
    Don't attempt to convert() or convert_alpha() the individual tiles.  It is
    already done for you.
    """

    pixelalpha = kwargs.get("pixelalpha", False)
    force_colorkey = kwargs.get("force_colorkey", False)

    if force_colorkey:
        pixelalpha = True

    if force_colorkey:
        try:
            force_colorkey = pygame.Color(*force_colorkey)
        except:
            msg = 'Cannot understand color: {0}'
            print msg.format(force_colorkey)
            raise ValueError

    # change background color into something nice
    if tmxdata.background_color:
        tmxdata.background_color = pygame.Color(tmxdata.background_color)

    # initialize the array of images
    tmxdata.images = [0] * tmxdata.maxgid

    for ts in tmxdata.tilesets:
        path = os.path.join(os.path.dirname(tmxdata.filename), ts.source)
        image = pygame.image.load(path)
        w, h = image.get_size()

        # margins and spacing
        tilewidth = ts.tilewidth + ts.spacing
        tileheight = ts.tileheight + ts.spacing
        tile_size = ts.tilewidth, ts.tileheight

        # some tileset images may be slightly larger than the tile area
        # ie: may include a banner, copyright, ect.  this compensates for that
        width = int((((w - ts.margin * 2 + ts.spacing) / tilewidth) * tilewidth) - ts.spacing)
        height = int((((h - ts.margin * 2 + ts.spacing) / tileheight) * tileheight) - ts.spacing)

        # trim off any pixels on the right side that isn't a tile
        # this happens if extra graphics are included on the left, but they are not actually part of the tileset
        width -= (w - ts.margin) % tilewidth

        # using product avoids the overhead of nested loops
        p = itertools.product(xrange(ts.margin, height + ts.margin, tileheight),
                              xrange(ts.margin, width + ts.margin, tilewidth))

        colorkey = getattr(ts, 'trans', None)
        if colorkey:
            colorkey = pygame.Color('#{0}'.format(colorkey))

        for real_gid, (y, x) in enumerate(p, ts.firstgid):
            if x + ts.tilewidth-ts.spacing > width:
                continue

            gids = tmxdata.map_gid(real_gid)

            if gids:
                original = image.subsurface(((x, y), tile_size))

                for gid, flags in gids:
                    tile = handle_transformation(original, flags)
                    tile = smart_convert(tile, colorkey, force_colorkey, pixelalpha)
                    tmxdata.images[gid] = tile

    # load image layer images
    for layer in tmxdata.all_layers:
        if isinstance(layer, pytmx.TiledImageLayer):
            colorkey = getattr(layer, 'trans', None)
            if colorkey:
                colorkey = pygame.Color("#{0}".format(colorkey))

            source = getattr(layer, 'source', None)
            if source:
                real_gid = len(tmxdata.images)
                gid = tmxdata.register_gid(real_gid)
                layer.gid = gid
                path = os.path.join(os.path.dirname(tmxdata.filename), source)
                image = pygame.image.load(path)
                image = smart_convert(image, colorkey, force_colorkey, pixelalpha)
                tmxdata.images.append(image)


def load_pygame(filename, *args, **kwargs):
    """
    PYGAME USERS: Use me.

    Load a TMX file, load the images, and return a TiledMap class that is ready to use.
    """
    tmxdata = pytmx.TiledMap(filename)
    _load_images_pygame(tmxdata, None, *args, **kwargs)
    return tmxdata


load_tmx = pytmx.TiledMap