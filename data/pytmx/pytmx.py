from itertools import chain, product
from xml.etree import ElementTree

from .utils import decode_gid, types, parse_properties, read_points


__all__ = ['TiledMap', 'TiledTileset', 'TiledLayer', 'TiledObject', 'TiledObjectGroup', 'TiledImageLayer']


class TiledElement(object):
    def set_properties(self, node):
        """
        read the xml attributes and tiled "properties" from a xml node and fill
        in the values into the object's dictionary.  Names will be checked to
        make sure that they do not conflict with reserved names.
        """

        # set the attributes reserved for tiled
        [setattr(self, k, types[str(k)](v)) for (k, v) in node.items()]

        # set the attributes that are derived from tiled 'properties'
        for k, v in parse_properties(node).items():
            if k in self.reserved:
                msg = "{0} \"{1}\" has a property called \"{2}\""
                print msg.format(self.__class__.__name__, self.name, k, self.__class__.__name__)
                msg = "This name is reserved for {0} objects and cannot be used."
                print msg.format(self.__class__.__name__)
                print "Please change the name in Tiled and try again."
                raise ValueError
            setattr(self, k, types[str(k)](v))


class TiledMap(TiledElement):
    """
    Contains the tile layers, tile images, object groups, and objects from a
    Tiled TMX map.
    """

    reserved = "visible version orientation width height tilewidth tileheight properties tileset layer objectgroup".split()

    def __init__(self, filename=None):
        from collections import defaultdict

        TiledElement.__init__(self)
        self.tilesets = []  # list of TiledTileset objects
        self.tilelayers = []  # list of TiledLayer objects
        self.imagelayers = []  # list of TiledImageLayer objects
        self.objectgroups = []  # list of TiledObjectGroup objects
        self.all_layers = []  # list of all layers in proper order
        self.tile_properties = {}  # dict of tiles that have metadata
        self.filename = filename

        self.layernames = {}

        # only used tiles are actually loaded, so there will be a difference
        # between the GIDs in the Tile map data (tmx) and the data in this
        # class and the layers.  This dictionary keeps track of that difference.
        self.gidmap = defaultdict(list)

        # should be filled in by a loader function
        self.images = []

        # defaults from the TMX specification
        self.version = 0.0
        self.orientation = None
        self.width = 0       # width of map in tiles
        self.height = 0      # height of map in tiles
        self.tilewidth = 0   # width of a tile in pixels
        self.tileheight = 0  # height of a tile in pixels
        self.background_color = None

        self.imagemap = {}  # mapping of gid and trans flags to real gids
        self.maxgid = 1

        if filename:
            self.load()

    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.filename)

    def getTileImage(self, x, y, layer):
        """
        return the tile image for this location
        x and y must be integers and are in tile coordinates, not pixel

        return value will be 0 if there is no tile with that location.
        """

        try:
            x, y, layer = map(int, (x, y, layer))
        except TypeError:
            msg = "Tile indexes/layers must be specified as integers."
            print msg
            raise TypeError

        try:
            assert (x >= 0 and y >= 0)
        except AssertionError:
            raise ValueError

        try:
            gid = self.tilelayers[layer].data[y][x]
        except IndexError:
            msg = "Coords: ({0},{1}) in layer {2} is not valid."
            print msg.format(x, y, layer)
            raise ValueError

        return self.getTileImageByGid(gid)

    def getTileImageByGid(self, gid):
        try:
            assert (gid >= 0)
            return self.images[gid]
        except (IndexError, ValueError, AssertionError):
            msg = "Invalid GID specified: {}"
            print msg.format(gid)
            raise ValueError
        except TypeError:
            msg = "GID must be specified as integer: {}"
            print msg.format(gid)
            raise TypeError

    def getTileGID(self, x, y, layer):
        """
        return GID of a tile in this location
        x and y must be integers and are in tile coordinates, not pixel
        """

        try:
            return self.tilelayers[int(layer)].data[int(y)][int(x)]
        except (IndexError, ValueError):
            msg = "Coords: ({0},{1}) in layer {2} is invalid"
            raise Exception, msg.format(x, y, layer)

    def getDrawOrder(self):
        """
        return a list of objects in the order that they should be drawn
        this will also exclude any layers that are not set to visible

        may be useful if you have objects and want to control rendering
        from tiled
        """

        raise NotImplementedError

    def getTileImages(self, r, layer):
        """
        return a group of tiles in an area
        expects a pygame rect or rect-like list/tuple

        useful if you don't want to repeatedly call getTileImage
        """

        raise NotImplementedError

    def getObjects(self):
        """
        Return iterator of all the objects associated with this map
        """

        return chain(*(i for i in self.objectgroups))

    def getTileProperties(self, (x, y, layer)):
        """
        return the properties for the tile, if any
        x and y must be integers and are in tile coordinates, not pixel

        returns a dict of there are properties, otherwise will be None
        """

        try:
            gid = self.tilelayers[int(layer)].data[int(y)][int(x)]
        except (IndexError, ValueError):
            msg = "Coords: ({0},{1}) in layer {2} is invalid."
            raise Exception, msg.format(x, y, layer)

        else:
            try:
                return self.tile_properties[gid]
            except (IndexError, ValueError):
                msg = "Coords: ({0},{1}) in layer {2} has invalid GID: {3}"
                raise Exception, msg.format(x, y, layer, gid)
            except KeyError:
                return None

    def getLayerData(self, layer):
        """
        Return the data for a layer.

        Data is an array of arrays.

        >>> pos = data[y][x]
        """

        try:
            return self.tilelayers[layer].data
        except IndexError:
            msg = "Layer {0} does not exist."
            raise ValueError, msg.format(layer)

    def getTileLocation(self, gid):
        # experimental way to find locations of a tile by the GID

        p = product(xrange(self.width),
                    xrange(self.height),
                    xrange(len(self.tilelayers)))

        return [(x, y, l) for (x, y, l) in p
                if self.tilelayers[l].data[y][x] == gid]

    def getTilePropertiesByGID(self, gid):
        try:
            return self.tile_properties[gid]
        except KeyError:
            return None

    def setTileProperties(self, gid, d):
        """
        set the properties of a tile by GID.
        must use a standard python dict as d
        """

        try:
            self.tile_properties[gid] = d
        except KeyError:
            msg = "GID #{0} does not exist."
            raise ValueError, msg.format(gid)

    def getTilePropertiesByLayer(self, layer):
        """
        Return a list of tile properties (dict) in use in this tile layer.
        """

        try:
            layer = int(layer)
        except:
            msg = "Layer must be an integer.  Got {0} instead."
            raise ValueError, msg.format(type(layer))

        p = product(range(self.width), range(self.height))
        layergids = set(self.tilelayers[layer].data[y][x] for x, y in p)

        props = []
        for gid in layergids:
            try:
                props.append((gid, self.tile_properties[gid]))
            except:
                continue

        return props

    def register_gid(self, real_gid, flags=0):
        """
        used to manage the mapping of GID between the tmx data and the internal
        data.

        number returned is gid used internally
        """

        if real_gid:
            try:
                return self.imagemap[(real_gid, flags)][0]
            except KeyError:
                # this tile has not been encountered before, or it has been
                # transformed in some way.  make a new GID for it.
                gid = self.maxgid
                self.maxgid += 1
                self.imagemap[(real_gid, flags)] = (gid, flags)
                self.gidmap[real_gid].append((gid, flags))
                return gid
        else:
            return 0

    def map_gid(self, real_gid):
        """
        used to lookup a GID read from a TMX file's data
        """

        try:
            return self.gidmap[int(real_gid)]
        except KeyError:
            return None
        except TypeError:
            msg = "GIDs must be an integer"
            raise TypeError, msg

    def loadTileImages(self, filename):
        raise NotImplementedError

    def load(self):
        """
        parse a map node from a tiled tmx file
        """
        etree = ElementTree.parse(self.filename).getroot()
        self.set_properties(etree)

        # initialize the gid mapping
        self.imagemap[(0, 0)] = 0

        self.background_color = etree.get('backgroundcolor', self.background_color)

        # *** do not change this load order!  gid mapping errors will occur if changed ***
        for node in etree.findall('layer'):
            self.addTileLayer(TiledLayer(self, node))

        for node in etree.findall('imagelayer'):
            self.addImageLayer(TiledImageLayer(self, node))

        for node in etree.findall('objectgroup'):
            self.objectgroups.append(TiledObjectGroup(self, node))

        for node in etree.findall('tileset'):
            self.tilesets.append(TiledTileset(self, node))

        # "tile objects", objects with a GID, have need to have their
        # attributes set after the tileset is loaded, so this step must be performed last
        for o in self.objects:
            p = self.getTilePropertiesByGID(o.gid)
            if p:
                o.__dict__.update(p)

    def addTileLayer(self, layer):
        """
        Add a TiledLayer layer object to the map.
        """

        if not isinstance(layer, TiledLayer):
            msg = "Layer must be an TiledLayer object.  Got {0} instead."
            raise ValueError, msg.format(type(layer))

        self.tilelayers.append(layer)
        self.all_layers.append(layer)
        self.layernames[layer.name] = layer

    def addImageLayer(self, layer):
        """
        Add a TiledImageLayer layer object to the map.
        """

        if not isinstance(layer, TiledImageLayer):
            msg = "Layer must be an TiledImageLayer object.  Got {0} instead."
            raise ValueError, msg.format(type(layer))

        self.imagelayers.append(layer)
        self.all_layers.append(layer)
        self.layernames[layer.name] = layer

    def getTileLayerByName(self, name):
        """
        Return a TiledLayer object with the name.
        This is case-sensitive.
        """

        try:
            return self.layernames[name]
        except KeyError:
            msg = "Layer \"{0}\" not found."
            raise ValueError, msg.format(name)

    def getTileLayerOrder(self):
        """
        Return a list of the map's layers in drawing order.
        """

        return list(self.tilelayers)

    @property
    def visibleTileLayers(self):
        """
        Returns a list of TileLayer objects that are set 'visible'.

        Layers have their visibility set in Tiled.  Optionally, you can over-
        ride the Tiled visibility by creating a property named 'visible'.
        """

        return [layer for layer in self.tilelayers if layer.visible]

    @property
    def objects(self):
        """
        Return iterator of all the objects associated with this map
        """
        return chain(*self.objectgroups)

    @property
    def visibleLayers(self):
        """
        Returns a generator of [Image/Tile]Layer objects that are set 'visible'.

        Layers have their visibility set in Tiled.
        """
        return (l for l in self.all_layers if l.visible)


class TiledTileset(TiledElement):
    reserved = "visible firstgid source name tilewidth tileheight spacing margin image tile properties".split()

    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent

        # defaults from the specification
        self.firstgid = 0
        self.source = None
        self.name = None
        self.tilewidth = 0
        self.tileheight = 0
        self.spacing = 0
        self.margin = 0
        self.tiles = {}
        self.trans = None
        self.width = 0
        self.height = 0

        self.parse(node)

    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    def parse(self, node):
        """
        parse a tileset element and return a tileset object and properties for
        tiles as a dict

        a bit of mangling is done here so that tilesets that have external
        TSX files appear the same as those that don't
        """
        import os

        # if true, then node references an external tileset
        source = node.get('source', False)
        if source:
            if source[-4:].lower() == ".tsx":

                # external tilesets don't save this, store it for later
                self.firstgid = int(node.get('firstgid'))

                # we need to mangle the path - tiled stores relative paths
                dirname = os.path.dirname(self.parent.filename)
                path = os.path.abspath(os.path.join(dirname, source))
                try:
                    node = ElementTree.parse(path).getroot()
                except IOError:
                    msg = "Cannot load external tileset: {0}"
                    raise Exception, msg.format(path)

            else:
                msg = "Found external tileset, but cannot handle type: {0}"
                raise Exception, msg.format(self.source)

        self.set_properties(node)

        # since tile objects [probably] don't have a lot of metadata,
        # we store it separately in the parent (a TiledMap instance)
        for child in node.getiterator('tile'):
            real_gid = int(child.get("id"))
            p = parse_properties(child)
            p['width'] = self.tilewidth
            p['height'] = self.tileheight
            for gid, flags in self.parent.map_gid(real_gid + self.firstgid):
                self.parent.setTileProperties(gid, p)

        image_node = node.find('image')
        self.source = image_node.get('source')
        self.trans = image_node.get("trans", None)


class TiledLayer(TiledElement):
    reserved = "visible name x y width height opacity properties data".split()

    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent
        self.data = []

        # defaults from the specification
        self.name = None
        self.opacity = 1.0
        self.visible = True

        self.parse(node)

    def __iter__(self):
        return self.iter_tiles()

    def iter_tiles(self):
        for y, x in product(range(self.height), range(self.width)):
            yield x, y, self.data[y][x]

    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    def parse(self, node):
        """
        parse a layer element
        """
        from data.pytmx.utils import group
        from itertools import product, imap
        from struct import unpack
        import array

        self.set_properties(node)

        data = None
        next_gid = None

        data_node = node.find('data')

        encoding = data_node.get("encoding", None)
        if encoding == "base64":
            from base64 import decodestring

            data = decodestring(data_node.text.strip())

        elif encoding == "csv":
            next_gid = imap(int, "".join(
                line.strip() for line in data_node.text.strip()
            ).split(","))

        elif encoding:
            msg = "TMX encoding type: {0} is not supported."
            raise Exception, msg.format(encoding)

        compression = data_node.get("compression", None)
        if compression == "gzip":
            from StringIO import StringIO
            import gzip

            fh = gzip.GzipFile(fileobj=StringIO(data))
            data = fh.read()
            fh.close()

        elif compression == "zlib":
            import zlib

            data = zlib.decompress(data)

        elif compression:
            msg = "TMX compression type: {0} is not supported."
            raise Exception, msg.format(str(attr["compression"]))

        # if data is None, then it was not decoded or decompressed, so
        # we assume here that it is going to be a bunch of tile elements
        # TODO: this will probably raise an exception if there are no tiles
        if encoding == next_gid is None:
            def get_children(parent):
                for child in parent.findall('tile'):
                    yield int(child.get('gid'))

            next_gid = get_children(data_node)

        elif data:
            # data is a list of gids. cast as 32-bit ints to format properly
            # create iterator to efficiently parse data
            next_gid = imap(lambda i: unpack("<L", "".join(i))[0], group(data, 4))

        # using bytes here limits the layer to 256 unique tiles
        # may be a limitation for very detailed maps, but most maps are not
        # so detailed.
        [self.data.append(array.array("H")) for i in xrange(self.height)]

        for (y, x) in product(xrange(self.height), xrange(self.width)):
            self.data[y].append(self.parent.register_gid(*decode_gid(next(next_gid))))


class TiledObjectGroup(TiledElement, list):
    """
    Stores TiledObjects.  Supports any operation of a normal list.
    """
    reserved = "visible name color x y width height opacity object properties".split()

    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent

        # defaults from the specification
        self.name = None
        self.color = None
        self.opacity = 1
        self.visible = 1
        self.parse(node)

    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    def parse(self, node):
        """
        parse a objectgroup element and return a object group
        """

        self.set_properties(node)

        for child in node.findall('object'):
            o = TiledObject(self.parent, child)
            self.append(o)


class TiledObject(TiledElement):
    reserved = "visible name type x y width height gid properties polygon polyline image".split()

    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent

        # defaults from the specification
        self.name = None
        self.type = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.rotation = 0
        self.gid = 0
        self.visible = 1

        self.parse(node)

    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    def parse(self, node):
        self.set_properties(node)

        # correctly handle "tile objects" (object with gid set)
        if self.gid:
            self.gid = self.parent.register_gid(self.gid)

        points = None

        polygon = node.find('polygon')
        if polygon is not None:
            points = read_points(polygon.get('points'))
            self.closed = True

        polyline = node.find('polyline')
        if polyline is not None:
            points = read_points(polyline.get('points'))
            self.closed = False

        if points:
            x1 = x2 = y1 = y2 = 0
            for x, y in points:
                if x < x1: x1 = x
                if x > x2: x2 = x
                if y < y1: y1 = y
                if y > y2: y2 = y
            self.width = abs(x1) + abs(x2)
            self.height = abs(y1) + abs(y2)
            self.points = tuple([(i[0] + self.x, i[1] + self.y) for i in points])

class TiledImageLayer(TiledElement):
    reserved = "visible source name width height opacity visible".split()

    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent
        self.source = None
        self.trans = None

        # unify the structure of layers
        self.gid = 0

        # defaults from the specification
        self.name = None
        self.opacity = 1
        self.visible = 1

        self.parse(node)

    def parse(self, node):
        self.set_properties(node)

        self.name = node.get('name', None)
        self.opacity = node.get('opacity', self.opacity)
        self.visible = node.get('visible', self.visible)

        image_node = node.find('image')
        self.source = image_node.get('source')
        self.trans = image_node.get('trans', None)