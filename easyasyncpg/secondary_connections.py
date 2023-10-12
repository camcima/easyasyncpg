import random

import asyncpg


class SecondaryConnections:
    def __init__(self):
        self.connections = []
        self.original_weights = []
        self.connection_map = {}
        self.total_weight = 0

    def add(self, connection: asyncpg.Connection, weight: int) -> None:
        self.connections.append(connection)
        self.original_weights.append(weight)
        self._update_connection_map()

    def get_connection(self) -> asyncpg.Connection:
        if len(self.connections) == 0:
            raise Exception("No secondary connections available")

        if len(self.connections) == 1:
            return self.connections[0]

        return self._get_weighted_random_connection()

    def get_all(self) -> list:
        return self.connections

    def __len__(self) -> int:
        return len(self.connections)

    def _get_weighted_random_connection(self) -> asyncpg.Connection:
        random_number = random.randint(1, self.total_weight)  # noqa: S311
        connection_index = self.connection_map[random_number]
        return self.connections[connection_index]

    def _update_connection_map(self) -> None:
        connection_map = {}
        total_weight = 0
        index = 0
        map_index = 1

        for weight in self.original_weights:
            total_weight += weight
            for _ in range(weight):
                connection_map[map_index] = index
                map_index += 1
            index += 1

        self.connection_map = connection_map
        self.total_weight = total_weight
