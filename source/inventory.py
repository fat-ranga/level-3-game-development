import numpy as np
from glm import *
from source.data_definitions import *

class Inventory:
    def __init__(self):
        self.width: int = 5
        self.height: int = 5
        self.array_size: int = self.width * self.height

        # Array of item IDs. # TODO array of classes or structs or something, since properties such as ammo amount needed.
        self.item_ids = np.zeros(self.array_size, dtype=int)
        # Array that corresponds to how much of an item is in a slot.
        self.item_amounts = np.zeros(self.array_size, dtype=int)

        self.set_item(vec2(0.5, 0.5), 5)

    def set_item(self, position: vec2, item_id: int, amount: int):
        self.item_ids[int(position.x) * self.width + int(position.y)] = item_id
        self.item_amounts[int(position.x) * self.width + int(position.y)] += 1
        print(self.item_ids)

    def add_item(self, item_id: int, amount: int):
        # Iterate through the array until we find a slot that
        # isn't occupied by an item, or is occupied by an item
        # of the same type.
        for x in range(self.width):
            for y in range(self.height):
                if self.item_ids[x * self.width + y] == 0 or self.item_ids[x * self.width + y] == item_id:
                    self.set_item_id(vec2(x, y), item_id)

    def get_item(self, position: vec2) -> int:
        return self.item_ids[int(position.x) * self.width + int(position.y)]