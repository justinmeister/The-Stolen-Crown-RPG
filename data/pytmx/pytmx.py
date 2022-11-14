from itertools import chain, product
from xml.etree import ElementTree
from .utils import decode_gid, types, parse_properties, read_points

#해당 파일을 import * 했을 때 변수 안에 있는 클래스들을 임포트 대상으로 한다
__all__ = ['TiledMap', 'TiledTileset', 'TiledLayer', 'TiledObject', 'TiledObjectGroup', 'TiledImageLayer']


#
class TiledElement(object):#pyhon 2.2 이상, 3 미만에서는 클래스에 object를 명시적으로 상속해줘야 한다
    
    #
    def set_properties(self, node):
        """
        read the xml attributes and tiled "properties" from a xml node and fill
        in the values into the object's dictionary.  Names will be checked to
        make sure that they do not conflict with reserved names.
        """

        # set the attributes reserved for tiled
        # tiled을 위해 예약된 속성을 설정(tiled = 게임 콘텐츠를 개발하는 데 도움이 되는 2D 레벨 편집기)
        [setattr(self, k, types[str(k)](v)) for (k, v) in node.items()]

        # set the attributes that are derived from tiled 'properties'
        # tiled의 'properties'에서 얻어와 attributes를 설정
        for k, v in parse_properties(node).items():
            if k in self.reserved:
                msg = "{0} \"{1}\" has a property called \"{2}\""
                print(msg.format(self.__class__.__name__, self.name, k, self.__class__.__name__))
                msg = "This name is reserved for {0} objects and cannot be used."
                print(msg.format(self.__class__.__name__))
                print("Please change the name in Tiled and try again.")
                raise ValueError
            setattr(self, k, types[str(k)](v))


#Tiled TMX map에서 tile의 layer와 이미지, object groups, object들을 가져와 저장하고 있는 클래스
class TiledMap(TiledElement):
    """
    Contains the tile layers, tile images, object groups, and objects from a
    Tiled TMX map.
    """

    #예약어를 정의
    reserved = "visible version orientation width height tilewidth tileheight properties tileset layer objectgroup".split()

    #초기화
    def __init__(self, filename=None):
        #defaultdict import
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

    #class명과 매개변수로 받은 filename을 문자열로 반환한다
    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.filename)

    #tile image를 반환한다. x와 y는 좌표이며 매개변수로 주어진 좌표에 tile이 없으면 0을 반환한다.
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
            print(msg)
            raise TypeError

        try:
            assert (x >= 0 and y >= 0)
        except AssertionError:
            raise ValueError

        try:
            gid = self.tilelayers[layer].data[y][x]
        except IndexError:
            msg = "Coords: ({0},{1}) in layer {2} is not valid."
            print(msg.format(x, y, layer))
            raise ValueError

        return self.getTileImageByGid(gid)

    #gid가 0보다 작으면 Valueerror를 일으키고 0보다 크거나 같으면 image 변수(list) 의 gid인덱스 값을 반환한다
    def getTileImageByGid(self, gid):
        try:
            assert (gid >= 0)
            return self.images[gid]
        except (IndexError, ValueError, AssertionError):
            msg = "Invalid GID specified: {}"
            print(msg.format(gid))
            raise ValueError
        except TypeError:
            msg = "GID must be specified as integer: {}"
            print(msg.format(gid))
            raise TypeError
        
    #tile gid를 반환한다. x와 y는 좌표이다.
    def getTileGID(self, x, y, layer):
        """
        return GID of a tile in this location
        x and y must be integers and are in tile coordinates, not pixel
        """

        try:
            return self.tilelayers[int(layer)].data[int(y)][int(x)]
        except (IndexError, ValueError):
            msg = "Coords: ({0},{1}) in layer {2} is invalid"
            raise Exception(msg.format(x, y, layer))

    #object list를 반환한다.표시되도록 하지 않은 layers는 제외된다.(하위클래스에서 반드시 Override 하여 구현해야 한다)
    def getDrawOrder(self):
        """
        return a list of objects in the order that they should be drawn
        this will also exclude any layers that are not set to visible

        may be useful if you have objects and want to control rendering
        from tiled
        """

        raise NotImplementedError

    #area 내에 있는 타일들의 모음을 반환한다.(하위클래스에서 반드시 Override 하여 구현해야 한다)
    def getTileImages(self, r, layer):
        """
        return a group of tiles in an area
        expects a pygame rect or rect-like list/tuple

        useful if you don't want to repeatedly call getTileImage
        """

        raise NotImplementedError

    #map에 있는 모든 object를 return할 수 있는 Iterator를 반환한다
    def getObjects(self):
        """
        Return iterator of all the objects associated with this map
        """

        return chain(*(i for i in self.objectgroups))

    #tile의 "properties"를 반환한다.x와 y는 좌표이다.
    def getTileProperties(self, source):
        """
        return the properties for the tile, if any
        x and y must be integers and are in tile coordinates, not pixel

        returns a dict of there are properties, otherwise will be None
        """

        try:
            gid = self.tilelayers[int(source[2])].data[int(source[1])][int(source[0])]
        except (IndexError, ValueError):
            msg = "Coords: ({0},{1}) in layer {2} is invalid."
            raise Exception(msg.format(source[0], source[1], source[2]))

        else:
            try:
                return self.tile_properties[gid]
            except (IndexError, ValueError):
                msg = "Coords: ({0},{1}) in layer {2} has invalid GID: {3}"
                raise Exception(msg.format(source[0], source[1], source[2], gid))
            except KeyError:
                return None

    #layer의 data를 반환한다.
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
            raise ValueError(msg.format(layer))

    #gid를 매개변수로 받아 tile의 위치를 반환한다
    def getTileLocation(self, gid):
        # experimental way to find locations of a tile by the GID

        p = product(range(self.width),
                    range(self.height),
                    range(len(self.tilelayers)))

        return [(x, y, l) for (x, y, l) in p
                if self.tilelayers[l].data[y][x] == gid]

    #gid를 매개변수로 받아 tile의 Properties를 반환한다
    def getTilePropertiesByGID(self, gid):
        try:
            return self.tile_properties[gid]
        except KeyError:
            return None

    #gid를 매개변수로 받아 tile의 Properties를 set 한다
    def setTileProperties(self, gid, d):
        """
        set the properties of a tile by GID.
        must use a standard python dict as d
        """

        try:
            self.tile_properties[gid] = d
        except KeyError:
            msg = "GID #{0} does not exist."
            raise ValueError(msg.format(gid))

    #layer를 매개변수로 받아 tile의 Properties를 반환한다
    def getTilePropertiesByLayer(self, layer):
        """
        Return a list of tile properties (dict) in use in this tile layer.
        """

        try:
            layer = int(layer)
        except:
            msg = "Layer must be an integer.  Got {0} instead."
            raise ValueError(msg.format(type(layer)))

        p = product(range(self.width), range(self.height))
        layergids = set(self.tilelayers[layer].data[y][x] for x, y in p)

        props = []
        for gid in layergids:
            try:
                props.append((gid, self.tile_properties[gid]))
            except:
                continue

        return props

    #tmx 데이터와 내부 데이터 사이의 GID 매핑을 관리한다. 반환값은 내부적으로 사용된다.
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

    #TMX 파일의 데이터에서 읽은 GID를 조회한다
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
            raise TypeError(msg)

    #filename을 변수로 받아 tileimages를 load한다.(하위클래스에서 반드시 Override 하여 구현해야 한다)
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

    #map에 layer를 추가한다
    def addTileLayer(self, layer):
        """
        Add a TiledLayer layer object to the map.
        """

        if not isinstance(layer, TiledLayer):
            msg = "Layer must be an TiledLayer object.  Got {0} instead."
            raise ValueError(msg.format(type(layer)))

        self.tilelayers.append(layer)
        self.all_layers.append(layer)
        self.layernames[layer.name] = layer

    #map에 imagelayer를 추가한다
    def addImageLayer(self, layer):
        """
        Add a TiledImageLayer layer object to the map.
        """

        if not isinstance(layer, TiledImageLayer):
            msg = "Layer must be an TiledImageLayer object.  Got {0} instead."
            raise ValueError(msg.format(type(layer)))

        self.imagelayers.append(layer)
        self.all_layers.append(layer)
        self.layernames[layer.name] = layer

    #name을 매개변수로 받아 해당 layer 객체를 반환한다
    def getTileLayerByName(self, name):
        """
        Return a TiledLayer object with the name.
        This is case-sensitive.
        """

        try:
            return self.layernames[name]
        except KeyError:
            msg = "Layer \"{0}\" not found."
            raise ValueError(msg.format(name))

    #map의 layer list를 draw 순서대로 return한다
    def getTileLayerOrder(self):
        """
        Return a list of the map's layers in drawing order.
        """

        return list(self.tilelayers)

    
    @property
    #visible한 titlelayer들을 list형태로 반환한다(@property 데코레이터를 사용함으로써 getter 처럼 사용 가능하다)
    def visibleTileLayers(self):
        """
        Returns a list of TileLayer objects that are set 'visible'.

        Layers have their visibility set in Tiled.  Optionally, you can over-
        ride the Tiled visibility by creating a property named 'visible'.
        """

        return [layer for layer in self.tilelayers if layer.visible]

    @property
    #map에 있는 모든 object를 return할 수 있는 Iterator를 반환한다(@property 데코레이터를 사용함으로써 getter 처럼 사용 가능하다)
    def objects(self):
        """
        Return iterator of all the objects associated with this map
        """
        return chain(*self.objectgroups)

    @property
    #visible한 layer들을 list형태로 반환한다(@property 데코레이터를 사용함으로써 getter 처럼 사용 가능하다)
    def visibleLayers(self):
        """
        Returns a generator of [Image/Tile]Layer objects that are set 'visible'.

        Layers have their visibility set in Tiled.  
        """     
        return (l for l in self.all_layers if l.visible)


#Tiled된 tile들을 저장하는 클래스(TiledElement의 자식 클래스)
class TiledTileset(TiledElement):
    
    reserved = "visible firstgid source name tilewidth tileheight spacing margin image tile properties".split()

    #초기화
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

    #사용자가 객체 자체를 이해할 수 있게 객체 정보를 문자열로 반환한다
    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    #.tsx로 끝나는(tileset element) 파일을 찾아 tileset object와 properties를 딕셔너리 형태로 반환한다
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
                    raise Exception(msg.format(path))

            else:
                msg = "Found external tileset, but cannot handle type: {0}"
                raise Exception(msg.format(self.source))
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


#Tiled된 layer들을 저장하는 클래스(TiledElement의 자식 클래스, 인터러블 객체)
class TiledLayer(TiledElement):
    reserved = "visible name x y width height opacity properties data".split()

    #초기화
    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent
        self.data = []

        # defaults from the specification
        self.name = None
        self.opacity = 1.0
        self.visible = True

        self.parse(node)

    #iter_tiles()를 이터레이터 객체로 반환한다
    def __iter__(self):
        return self.iter_tiles()

    #class의 좌표값과 좌표값에 해당되는 data를 이터레이터 객체로 반환한다
    def iter_tiles(self):
        for y, x in product(range(self.height), range(self.width)):
            yield x, y, self.data[y][x]

    #사용자가 객체 자체를 이해할 수 있게 객체 정보를 문자열로 반환한다
    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    #매개변수로 받은 node에서 data를 찾은 후 해당 data의 encoding과 압축 유형을 확인해서 압축을 해제한 후 해당 파일들에 tile elements가 있으면 decoding한다
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
            raise Exception(msg.format(encoding))

        compression = data_node.get("compression", None)
        if compression == "gzip":
            from io import StringIO
            import gzip

            fh = gzip.GzipFile(fileobj=StringIO(data))
            data = fh.read()
            fh.close()

        elif compression == "zlib":
            import zlib

            data = zlib.decompress(data)

        elif compression:
            msg = "TMX compression type: {0} is not supported."
            raise Exception(msg.format("compression"))

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
        [self.data.append(array.array("H")) for i in range(self.height)]

        for (y, x) in product(range(self.height), range(self.width)):
            self.data[y].append(self.parent.register_gid(*decode_gid(next(next_gid))))

#Tiled 객체의 그룹을 저장하는 클래스(TiledElement, list의 자식 클래스)
class TiledObjectGroup(TiledElement, list):
    """
    Stores TiledObjects.  Supports any operation of a normal list.
    """
    reserved = "visible name color x y width height opacity object properties".split()

    #초기화
    def __init__(self, parent, node):
        TiledElement.__init__(self)
        self.parent = parent

        # defaults from the specification
        self.name = None
        self.color = None
        self.opacity = 1
        self.visible = 1
        self.parse(node)

    #사용자가 객체 자체를 이해할 수 있게 객체 정보를 문자열로 반환한다
    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    #node에서 object를 pares해 object그룹으로 반환한다
    def parse(self, node):
        """
        parse a objectgroup element and return a object group
        """

        self.set_properties(node)

        for child in node.findall('object'):
            o = TiledObject(self.parent, child)
            self.append(o)

#Tiled 객체를 나타내는 클래스(TiledElement의 자식 클래스)
class TiledObject(TiledElement):
    reserved = "visible name type x y width height gid properties polygon polyline image".split()

    #초기화
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

    #사용자가 객체 자체를 이해할 수 있게 객체 정보를 문자열로 반환한다
    def __repr__(self):
        return "<{0}: \"{1}\">".format(self.__class__.__name__, self.name)

    #point를 parse해 좌표를 얻고 self.point에 저장한다
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

        #points가 존재하면
        if points:
            x1 = x2 = y1 = y2 = 0
            for x, y in points:
                if x < x1: x1 = x  #x가 음수이면 x1에 x를 넣는다.
                if x > x2: x2 = x  #x가 양수이면 x2에 x를 넣는다.
                if y < y1: y1 = y  #y가 양수이면 y1에 y를 넣는다.
                if y > y2: y2 = y  #y가 양수이면 y2에 y를 넣는다.
            self.width = abs(x1) + abs(x2) #width에 x1절댓값 + x2절댓값을 저장한다(길이)
            self.height = abs(y1) + abs(y2) #height y1절댓값 + y2절댓값을 저장한다(높이)
            self.points = tuple([(i[0] + self.x, i[1] + self.y) for i in points])

#Tiled의 imagelayer을 나타내는 클래스
class TiledImageLayer(TiledElement):
    reserved = "visible source name width height opacity visible".split()

    #초기화
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

    #node에서 name, opacity, visible를 parse해 저장하고 image를 parse해 source와 trans를 저장한다
    def parse(self, node):
        self.set_properties(node)

        self.name = node.get('name', None)
        self.opacity = node.get('opacity', self.opacity)
        self.visible = node.get('visible', self.visible)

        image_node = node.find('image')
        self.source = image_node.get('source')
        self.trans = image_node.get('trans', None)