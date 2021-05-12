from __future__ import annotations

from typing import List, Tuple

import numpy as np
import tcod

from actions import Action
from components.base_component import BaseComponent

class BaseAI(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.
        If there is no valid path than return an empty list.
        """
        # Copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # Lower = more enemies crowd behind each other
                # Higher = enemies will choose longer routes to
                # surround the player
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass the graph to the pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Starting position

        # compute the path to the destination and remove starting points
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]]
        return [(index[0], index[1]) for index in path]