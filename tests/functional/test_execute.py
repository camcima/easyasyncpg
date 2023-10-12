import pytest
from easyasyncpg import EasyAsyncPg
from easyasyncpg.role import Role


@pytest.mark.asyncio
async def test_execute_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.SECONDARY,
    )
    await db.execute("CREATE TEMP TABLE fruits (id INTEGER, name VARCHAR(20))")
    await db.execute("INSERT INTO fruits VALUES (1, 'apple')")
    await db.execute("INSERT INTO fruits VALUES (2, 'banana')")

    result = await db.fetch_all("SELECT * FROM fruits")
    assert len(result) == 2
    assert result[0]["name"] == "apple"
    assert result[1]["name"] == "banana"


@pytest.mark.asyncio
async def test_execute_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.SECONDARY,
    )
    await db.execute("CREATE TEMP TABLE fruits (id INTEGER, name VARCHAR(20))")
    await db.execute("INSERT INTO fruits VALUES (1, :name)", {"name": "apple"})
    await db.execute("INSERT INTO fruits VALUES (2, :name)", {"name": "banana"})

    result = await db.fetch_all("SELECT * FROM fruits")
    assert len(result) == 2
    assert result[0]["name"] == "apple"
    assert result[1]["name"] == "banana"


@pytest.mark.asyncio
async def test_execute_many_with_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.SECONDARY,
    )
    await db.execute("CREATE TEMP TABLE fruits (id INTEGER, name VARCHAR(20))")
    await db.execute_many(
        "INSERT INTO fruits VALUES (:id, :name)",
        [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "banana"},
        ],
    )

    result = await db.fetch_all("SELECT * FROM fruits")
    assert len(result) == 2
    assert result[0]["name"] == "apple"
    assert result[1]["name"] == "banana"


@pytest.mark.asyncio
async def test_execute_many_no_params(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    with pytest.raises(ValueError) as e:
        await db.execute_many("INSERT INTO fruits VALUES (:id, :name)")

    assert str(e.value) == "execute_many requires a list of params"
