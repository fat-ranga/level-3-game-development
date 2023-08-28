import numpy as np
from glm import *
from source.data_definitions import *


class Inventory:
    def __init__(self, dimensions: ivec2):
        self.width: int = dimensions.x
        self.height: int = dimensions.y
        self.array_size: int = dimensions.x * dimensions.y

        # List (used like an array) of items and their properties.
        # We could've used a numpy array like elsewhere, but those can only have
        # a single data type, which wouldn't work with items that need to describe unique properties like
        # how much ammo they have, or the fact that there can only
        # be one in one slot. Numeric IDs therefore aren't a good fit. We use Item()
        # objects instead.
        self.items: list = []

        # Fill the inventory with nothing to start off with.
        for i in range(self.array_size):
            self.items.append(None)

        cap: Item = Item()
        self.set_item(vec2(0.5, 0.5), item=cap)

        print(self.items)

    def set_item(self, position: vec2, item: Item):
        self.items[int(position.x) * self.width + int(position.y)] = item

    def add_item(self, item: Item, amount: int):
        # Iterate through the array until we find a slot occupied by an item
        # of the same type, and increase its amount if the slot isn't greater than its max item stack count.
        for x in range(self.width):
            for y in range(self.height):
                if self.items[x * self.width + y].string_id == item.string_id:
                    if self.items[x * self.width + y].amount < item.max_amount:
                        self.items[x * self.width + y].amount += 1

        # Otherwise, iterate through the array until we find a slot that
        # isn't occupied by an item.
        for x in range(self.width):
            for y in range(self.height):
                if self.items[x * self.width + y] is None:
                    self.set_item(vec2(x, y), item)
                    return

        print(f"Can't fit item {item.string_id} in inventory!")

    def get_item(self, position: vec2) -> int:
        return self.items[int(position.x) * self.width + int(position.y)]