from itertools import tee, islice, izip, product
from collections import defaultdict

from pygame import Rect

from .constants import *


def read_points(text):
    return [ tuple(map(lambda x: int(x), i.split(',')))
         for i in text.split() ]


def parse_properties(node):
    """
    parse a node and return a dict that represents a tiled "property"
    """

    # the "properties" from tiled's tmx have an annoying quality that "name"
    # and "value" is included. here we mangle it to get that junk out.

    d = {}

    for child in node.findall('properties'):
        for subnode in child.findall('property'):
            d[subnode.get('name')] = subnode.get('value')

    return d


def decode_gid(raw_gid):
    # gids are encoded with extra information
    # as of 0.7.0 it determines if the tile should be flipped when rendered
    # as of 0.8.0 bit 30 determines if GID is rotated

    flags = 0
    if raw_gid & GID_TRANS_FLIPX == GID_TRANS_FLIPX: flags += TRANS_FLIPX
    if raw_gid & GID_TRANS_FLIPY == GID_TRANS_FLIPY: flags += TRANS_FLIPY
    if raw_gid & GID_TRANS_ROT == GID_TRANS_ROT: flags += TRANS_ROT
    gid = raw_gid & ~(GID_TRANS_FLIPX | GID_TRANS_FLIPY | GID_TRANS_ROT)

    return gid, flags


def handle_bool(text):
    # properly convert strings to a bool
    try:
        return bool(int(text))
    except:
        pass

    try:
        text = str(text).lower()
        if text == "true":   return True
        if text == "yes":    return True
        if text == "false":  return False
        if text == "no":     return False
    except:
        pass

    raise ValueError


# used to change the unicode string returned from xml to proper python
# variable types.
types = defaultdict(lambda: str)
types.update({
    "version": float,
    "orientation": str,
    "width": int,
    "height": int,
    "tilewidth": int,
    "tileheight": int,
    "firstgid": int,
    "source": str,
    "name": str,
    "spacing": int,
    "margin": int,
    "trans": str,
    "id": int,
    "opacity": float,
    "visible": handle_bool,
    "encoding": str,
    "compression": str,
    "gid": int,
    "type": str,
    "x": int,
    "y": int,
    "value": str,
})


def pairwise(iterable):
    # return a list as a sequence of pairs
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def group(l, n):
    # return a list as a sequence of n tuples
    return izip(*(islice(l, i, None, n) for i in xrange(n)))


def buildDistributionRects(tmxmap, layer, tileset=None, real_gid=None):
    """
    generate a set of non-overlapping rects that represents the distribution
    of the specified gid.

    useful for generating rects for use in collision detection
    """

    if isinstance(tileset, int):
        try:
            tileset = tmxmap.tilesets[tileset]
        except IndexError:
            msg = "Tileset #{0} not found in map {1}."
            raise IndexError, msg.format(tileset, tmxmap)

    elif isinstance(tileset, str):
        try:
            tileset = [ t for t in tmxmap.tilesets if t.name == tileset ].pop()
        except IndexError:
            msg = "Tileset \"{0}\" not found in map {1}."
            raise ValueError, msg.format(tileset, tmxmap)

    elif tileset:
        msg = "Tileset must be either a int or string. got: {0}"
        raise ValueError, msg.format(type(tileset))

    gid = None
    if real_gid:
        try:
            gid, flags = tmxmap.map_gid(real_gid)[0]
        except IndexError:
            msg = "GID #{0} not found"
            raise ValueError, msg.format(real_gid)

    if isinstance(layer, int):
        layer_data = tmxmap.getLayerData(layer).data
    elif isinstance(layer, str):
        try:
            layer = [ l for l in tmxmap.tilelayers if l.name == layer ].pop()
            layer_data = layer.data
        except IndexError:
            msg = "Layer \"{0}\" not found in map {1}."
            raise ValueError, msg.format(layer, tmxmap)

    p = product(xrange(tmxmap.width), xrange(tmxmap.height))
    if gid:
        points = [ (x,y) for (x,y) in p if layer_data[y][x] == gid ]
    else:
        points = [ (x,y) for (x,y) in p if layer_data[y][x] ]

    rects = simplify(points, tmxmap.tilewidth, tmxmap.tileheight)
    return rects


def simplify(all_points, tilewidth, tileheight):
    """
    kludge:

    "A kludge (or kluge) is a workaround, a quick-and-dirty solution,
    a clumsy or inelegant, yet effective, solution to a problem, typically
    using parts that are cobbled together."

    -- wikipedia

    turn a list of points into a rects
    adjacent rects will be combined.

    plain english:
        the input list must be a list of tuples that represent
        the areas to be combined into rects
        the rects will be blended together over solid groups

        so if data is something like:

        0 1 1 1 0 0 0
        0 1 1 0 0 0 0
        0 0 0 0 0 4 0
        0 0 0 0 0 4 0
        0 0 0 0 0 0 0
        0 0 1 1 1 1 1

        you'll have the 4 rects that mask the area like this:

        ..######......
        ..####........
        ..........##..
        ..........##..
        ..............
        ....##########

        pretty cool, right?

    there may be cases where the number of rectangles is not as low as possible,
    but I haven't found that it is excessively bad.  certainly much better than
    making a list of rects, one for each tile on the map!

    """

    def pick_rect(points, rects):
        ox, oy = sorted([ (sum(p), p) for p in points ])[0][1]
        x = ox
        y = oy
        ex = None

        while 1:
            x += 1
            if not (x, y) in points:
                if ex is None:
                    ex = x - 1

                if ((ox, y+1) in points):
                    if x == ex + 1 :
                        y += 1
                        x = ox

                    else:
                        y -= 1
                        break
                else:
                    if x <= ex: y-= 1
                    break

        c_rect = Rect(ox*tilewidth,oy*tileheight,\
                     (ex-ox+1)*tilewidth,(y-oy+1)*tileheight)

        rects.append(c_rect)

        rect = Rect(ox,oy,ex-ox+1,y-oy+1)
        kill = [ p for p in points if rect.collidepoint(p) ]
        [ points.remove(i) for i in kill ]

        if points:
            pick_rect(points, rects)

    rect_list = []
    while all_points:
        pick_rect(all_points, rect_list)

    return rect_list

