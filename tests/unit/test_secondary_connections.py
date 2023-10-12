from unittest.mock import Mock

import pytest
from easyasyncpg.secondary_connections import SecondaryConnections


def test_add_secondary_connection():
    secondary_connections = SecondaryConnections()
    connection = Mock()
    secondary_connections.add(connection, 3)
    assert len(secondary_connections) == 1
    assert secondary_connections.connections[0] == connection
    assert secondary_connections.original_weights[0] == 3
    assert secondary_connections.connection_map == {1: 0, 2: 0, 3: 0}
    assert secondary_connections.total_weight == 3


def test_add_multiple_secondary_connections():
    secondary_connections = SecondaryConnections()
    connection1 = Mock()
    connection2 = Mock()
    secondary_connections.add(connection1, 2)
    secondary_connections.add(connection2, 3)
    assert len(secondary_connections) == 2
    assert secondary_connections.connections[0] == connection1
    assert secondary_connections.connections[1] == connection2
    assert secondary_connections.original_weights[0] == 2
    assert secondary_connections.original_weights[1] == 3
    assert secondary_connections.connection_map == {1: 0, 2: 0, 3: 1, 4: 1, 5: 1}
    assert secondary_connections.total_weight == 5


def test_get_secondary_connection_single():
    secondary_connections = SecondaryConnections()
    connection = Mock()
    secondary_connections.add(connection, 3)
    assert secondary_connections.get_connection() == connection


def test_get_secondary_connection_multiple():
    secondary_connections = SecondaryConnections()
    connection1 = Mock()
    connection2 = Mock()
    secondary_connections.add(connection1, 2)
    secondary_connections.add(connection2, 3)
    connection = secondary_connections.get_connection()
    assert connection in (connection1, connection2)


def test_get_secondary_connection_no_connections():
    secondary_connections = SecondaryConnections()
    with pytest.raises(Exception) as e:
        secondary_connections.get_connection()
    assert str(e.value) == "No secondary connections available"


def test_random_distribution():
    secondary_connections = SecondaryConnections()
    connection1 = Mock()
    connection2 = Mock()
    secondary_connections.add(connection1, 2)
    secondary_connections.add(connection2, 3)
    connection1_count = 0
    connection2_count = 0
    for _ in range(50000):
        connection = secondary_connections.get_connection()
        if connection == connection1:
            connection1_count += 1
        else:
            connection2_count += 1
    assert connection1_count < 21000
    assert connection2_count > 29000
