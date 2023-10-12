import asyncpg
import pytest
import pytest_asyncio
from easyasyncpg import EasyAsyncPg


@pytest_asyncio.fixture(autouse=True)
async def setup_db(db_config):
    connection = await asyncpg.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    await connection.execute("DROP TABLE IF EXISTS fruits;")
    await connection.execute(
        """
        CREATE TABLE IF NOT EXISTS fruits(
            id INTEGER PRIMARY KEY,
            name VARCHAR(20) NOT NULL
        )
        """
    )
    await connection.execute(
        """
        INSERT INTO fruits (id, name) VALUES (1, 'apple'), (2, 'apple'),
            (3, 'banana'), (4, 'orange'), (5, 'pear'), (6, 'strawberry');
        """
    )
    await connection.close()


@pytest.mark.asyncio
async def test_fetch_all_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_all("SELECT * FROM fruits ORDER BY name;")
    assert len(result) == 6


@pytest.mark.asyncio
async def test_fetch_all_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_all(
        "SELECT * FROM fruits WHERE name = :name", {"name": "apple"}
    )
    assert len(result) == 2
    assert result[0]["name"] == "apple"
    assert result[1]["name"] == "apple"


@pytest.mark.asyncio
async def test_fetch_all_empty_result(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_all(
        "SELECT * FROM fruits WHERE name = :name", {"name": "pineapple"}
    )
    assert len(result) == 0


@pytest.mark.asyncio
async def test_fetch_one_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_one("SELECT * FROM fruits")
    assert result["id"] is not None
    assert result["name"] == "apple"


@pytest.mark.asyncio
async def test_fetch_one_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_one(
        "SELECT * FROM fruits WHERE name = :name", {"name": "apple"}
    )
    assert result["id"] is not None
    assert result["name"] == "apple"


@pytest.mark.asyncio
async def test_fetch_one_empty_result(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_one(
        "SELECT * FROM fruits WHERE name = :name", {"name": "pineapple"}
    )
    assert result is None


@pytest.mark.asyncio
async def test_fetch_val_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_val("SELECT COUNT(*) FROM fruits;")
    assert result == 6


@pytest.mark.asyncio
async def test_fetch_val_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_val(
        "SELECT COUNT(*) FROM fruits WHERE name = :name", {"name": "apple"}
    )
    assert result == 2


@pytest.mark.asyncio
async def test_fetch_val_empty_result(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_val(
        "SELECT id FROM fruits WHERE name = :name", {"name": "pineapple"}
    )
    assert result is None


@pytest.mark.asyncio
async def test_fetch_column_no_params_index_zero(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_column("SELECT * FROM fruits ORDER BY name;")
    assert isinstance(result, list)
    assert len(result) == 6
    assert result[0] == 1
    assert result[1] == 2
    assert result[2] == 3
    assert result[3] == 4
    assert result[4] == 5
    assert result[5] == 6


@pytest.mark.asyncio
async def test_fetch_column_no_params_index_one(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_column("SELECT * FROM fruits ORDER BY name;", index=1)
    assert isinstance(result, list)
    assert len(result) == 6
    assert result[0] == "apple"
    assert result[1] == "apple"
    assert result[2] == "banana"
    assert result[3] == "orange"
    assert result[4] == "pear"
    assert result[5] == "strawberry"


@pytest.mark.asyncio
async def test_fetch_column_with_params_index_zero(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_column(
        "SELECT * FROM fruits WHERE name = :name", {"name": "apple"}
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == 1
    assert result[1] == 2


@pytest.mark.asyncio
async def test_fetch_column_with_params_index_one(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_column(
        "SELECT * FROM fruits WHERE name = :name", {"name": "apple"}, index=1
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == "apple"
    assert result[1] == "apple"


@pytest.mark.asyncio
async def test_fetch_key_pairs_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_key_pairs("SELECT id, name FROM fruits ORDER BY name;")
    assert isinstance(result, dict)
    assert len(result) == 6
    assert result[1] == "apple"
    assert result[2] == "apple"
    assert result[3] == "banana"
    assert result[4] == "orange"
    assert result[5] == "pear"
    assert result[6] == "strawberry"


@pytest.mark.asyncio
async def test_fetch_key_pairs_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_key_pairs(
        "SELECT id, name FROM fruits WHERE name = :name", {"name": "apple"}
    )
    assert isinstance(result, dict)
    assert len(result) == 2
    assert result[1] == "apple"
    assert result[2] == "apple"


@pytest.mark.asyncio
async def test_fetch_key_pairs_string_key(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_key_pairs(
        "SELECT name, id FROM fruits WHERE name = :name", {"name": "orange"}
    )
    assert isinstance(result, dict)
    assert len(result) == 1
    assert result["orange"] == 4


@pytest.mark.asyncio
async def test_fetch_key_pairs_empty_result(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
    )

    result = await db.fetch_key_pairs(
        "SELECT id, name FROM fruits WHERE name = :name", {"name": "pineapple"}
    )
    assert isinstance(result, dict)
    assert len(result) == 0
