import asyncpg
import pytest
from easyasyncpg import EasyAsyncPg
from easyasyncpg.role import Role


@pytest.mark.asyncio
async def test_add_connection(db_config):
    db = EasyAsyncPg()
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.PRIMARY,
    )

    connections = db.get_connections()
    assert connections["primary"] is not None

    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config["port"],
        role=Role.SECONDARY,
    )
    connections = db.get_connections()

    assert connections["primary"] is not None
    assert len(connections["secondaries"]) == 1


@pytest.mark.asyncio
async def test_invalid_database_role(db_config):
    db = EasyAsyncPg()
    with pytest.raises(ValueError) as excinfo:
        await db.add_connection(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            port=db_config["port"],
            role="INVALID_ROLE",
        )
    assert "Invalid role: INVALID_ROLE" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_connections(db_config):
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
    connections = db.get_connections()
    assert connections["primary"] is not None
    assert isinstance(connections["primary"], asyncpg.Connection)
    assert len(connections["secondaries"]) == 1
    assert isinstance(connections["secondaries"][0], asyncpg.Connection)


@pytest.mark.asyncio
async def test_begin_commit_transaction(db_config):
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
    assert await db.begin_transaction() is True
    assert await db.commit_transaction() is True


@pytest.mark.asyncio
async def test_begin_rollback_transaction(db_config):
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
    assert await db.begin_transaction() is True
    assert await db.rollback_transaction() is True


@pytest.mark.asyncio
async def test_is_not_creating_nested_transactions(db_config):
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

    assert await db.begin_transaction() is True
    assert await db.begin_transaction() is False
    assert await db.commit_transaction() is True
    assert await db.commit_transaction() is False


@pytest.mark.asyncio
async def test_rollback_no_transaction(db_config):
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

    assert await db.rollback_transaction() is False


@pytest.mark.asyncio
async def test_execute_transaction(db_config):
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

    async def test_transaction(db: EasyAsyncPg):
        return await db.fetch_one("SELECT 1 AS id;")

    result = await db.execute_transaction(test_transaction)
    assert result["id"] == 1


@pytest.mark.asyncio
async def test_execute_transaction_with_error(db_config):
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

    await db.execute("CREATE TEMP TABLE test (id INT);")

    async def test_transaction(db: EasyAsyncPg):
        await db.execute("INSERT INTO test (id) VALUES (1);")
        await db.execute("INVALID SQL")

    with pytest.raises(asyncpg.exceptions.PostgresSyntaxError):
        await db.execute_transaction(test_transaction)

    result = await db.fetch_one("SELECT * FROM test;")
    assert result is None


@pytest.mark.asyncio
async def test_get_read_connection_safe_mode_not_used_primary(db_config):
    db = EasyAsyncPg(safe_mode=True)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    connection = db._get_read_connection()
    assert connection is not None
    assert connection is not db.primary_connection


@pytest.mark.asyncio
async def test_get_read_connection_safe_mode_used_primary(db_config):
    db = EasyAsyncPg(safe_mode=True)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    connection = db._get_write_connection()
    connection = db._get_read_connection()
    assert connection is not None
    assert connection is db.primary_connection


@pytest.mark.asyncio
async def test_get_read_connection_force_primary(db_config):
    db = EasyAsyncPg(safe_mode=False)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    connection = db._get_read_connection(force_primary_connection=True)
    assert connection is not None
    assert connection is db.primary_connection


@pytest.mark.asyncio
async def test_get_read_connection_active_transaction(db_config):
    db = EasyAsyncPg(safe_mode=False)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    await db.begin_transaction()
    connection = db._get_read_connection()
    assert connection is not None
    assert connection is db.primary_connection


@pytest.mark.asyncio
async def test_get_read_connection_no_secondary(db_config):
    db = EasyAsyncPg(safe_mode=False)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )

    connection = db._get_read_connection()
    assert connection is not None
    assert connection is db.primary_connection


@pytest.mark.asyncio
async def test_get_write_connection(db_config):
    db = EasyAsyncPg(safe_mode=False)
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.PRIMARY,
    )
    await db.add_connection(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="postgres",
        port=db_config["port"],
        role=Role.SECONDARY,
    )

    connection = db._get_write_connection()
    assert connection is not None
    assert connection is db.primary_connection


@pytest.mark.asyncio
async def test_no_write_connection():
    db = EasyAsyncPg()

    with pytest.raises(Exception) as e:
        db._get_write_connection()

    assert "No primary connection available" in str(e.value)


@pytest.mark.asyncio
async def test_no_read_connection():
    db = EasyAsyncPg()

    with pytest.raises(Exception) as e:
        db._get_read_connection()

    assert "No primary connection available" in str(e.value)
