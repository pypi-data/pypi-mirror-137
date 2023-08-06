from collections import namedtuple
from enum import Enumerate
from pygame import Surface
import logging

log = logging.getLogger(__name__)

# Based on this info, we will spawn specific tile on specific place
Tile = namedtuple("Tile", ["value", "surface"])

# And this is collection that holds tiles. It should be subclassed
# class TileScheme(Enum):
#    pass


class SimpleMap:
    pass


class TiledMap(SimpleMap):
    """Tiled map blueprint"""

    def __init__(self, layout):
        # Layout should be map's layout. Internally its array of arrays, I think?
        self.layout = layout
        # self.background = None
        # pass

    # #TODO: maybe add ability to append multiple layouts, for multiple layers? Idk

    def generate(tiles, background: Surface = None) -> Surface:
        """Generate surface out of this map's layout"""
        # stub
        pass


class LayeredMap:
    """Map that consists of multiple layers"""

    def __init__(self, first_layer: SimpleMap):
        self.layers = [first_layer]

    def __getitem__(self, key: int):
        return self.layers[key]

    def add_layer(self, layer: SimpleMap):
        self.layers.append(layer)

    def generate(background: Surface = None) -> Surface:
        # stub
        for layer in self.layers:
            pass


####
# tests below, to be removed on release
