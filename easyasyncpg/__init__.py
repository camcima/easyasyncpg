from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import asyncpg

from easyasyncpg.named_parameter_query import NamedParameterQuery
from easyasyncpg.role import Role
from easyasyncpg.secondary_connections import SecondaryConnections

if TYPE_CHECKING:
    from asyncpg.transaction import Transaction  # pragma: no cover


class EasyAsyncPg:
    def __init__(self, safe_mode: bool = True) -> None:
        self.safe_mode = safe_mode
        self.primary_connection: asyncpg.Connection | None = None
        self.secondary_connections = SecondaryConnections()
        self.active_transaction: Transaction | None = None
        self.has_used_primary = False

    async def add_connection(
        self,
        host: str = "localhost",
        user: str = "postgres",
        password: str = "postgres",  # noqa: S107
        database: str = "postgres",
        port: int = 5432,
        role: Role = Role.PRIMARY,
        weight: int = 1,
    ) -> None:
        self._validate_role(role)
        connection = await asyncpg.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
        )

        if role == Role.PRIMARY:
            self.primary_connection = connection
        else:
            self.secondary_connections.add(connection, weight)

    def get_connections(self) -> dict:
        return {
            "primary": self.primary_connection,
            "secondaries": self.secondary_connections.get_all(),
        }

    async def begin_transaction(self) -> bool:
        if self.active_transaction:
            return False

        self.active_transaction = self._get_write_connection().transaction()
        await self.active_transaction.start()
        return True

    async def commit_transaction(self) -> bool:
        if not self.active_transaction:
            return False

        await self.active_transaction.commit()
        self.active_transaction = None
        return True

    async def rollback_transaction(self) -> bool:
        if not self.active_transaction:
            return False

        await self.active_transaction.rollback()
        self.active_transaction = None
        return True

    async def execute_transaction(self, transaction: Callable) -> Any:
        try:
            await self.begin_transaction()
            result = await transaction(self)
            await self.commit_transaction()
            return result
        except Exception as e:
            await self.rollback_transaction()
            raise e

    async def execute(self, query: str, params: dict | None = None) -> None:
        if params is None:
            params = {}
        connection = self._get_write_connection()
        named_query = NamedParameterQuery(query, params)
        await connection.execute(
            named_query.positional_query, *named_query.positional_params
        )

    async def execute_many(self, query: str, params: list[dict] | None = None) -> None:
        if params is None:
            raise ValueError("execute_many requires a list of params")
        connection = self._get_write_connection()
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        await stmt.executemany(named_query.positional_params)

    async def fetch_all(
        self,
        query: str,
        params: dict | None = None,
        force_primary_connection: bool = False,
    ) -> list[dict]:
        if params is None:
            params = {}
        connection = self._get_read_connection(force_primary_connection)
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        records = await stmt.fetch(*named_query.positional_params)
        return [dict(record) for record in records]

    async def fetch_one(
        self,
        query: str,
        params: dict | None = None,
        force_primary_connection: bool = False,
    ) -> dict | None:
        if params is None:
            params = {}
        connection = self._get_read_connection(force_primary_connection)
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        record = await stmt.fetchrow(*named_query.positional_params)
        if record is None:
            return None
        return dict(record)

    async def fetch_val(
        self,
        query: str,
        params: dict | None = None,
        force_primary_connection: bool = False,
    ) -> Any:
        if params is None:
            params = {}
        connection = self._get_read_connection(force_primary_connection)
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        return await stmt.fetchval(*named_query.positional_params)

    async def fetch_column(
        self,
        query: str,
        params: dict | None = None,
        index: int = 0,
        force_primary_connection: bool = False,
    ) -> list[Any]:
        if params is None:
            params = {}
        connection = self._get_read_connection(force_primary_connection)
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        records = await stmt.fetch(*named_query.positional_params)
        return [record[index] for record in records]

    async def fetch_key_pairs(
        self,
        query: str,
        params: dict | None = None,
        force_primary_connection: bool = False,
    ) -> dict[Any, Any]:
        if params is None:
            params = {}
        connection = self._get_read_connection(force_primary_connection)
        named_query = NamedParameterQuery(query, params)
        stmt = await connection.prepare(named_query.positional_query)
        records = await stmt.fetch(*named_query.positional_params)
        return {record[0]: record[1] for record in records}

    def _get_read_connection(
        self, force_primary_connection: bool = False
    ) -> asyncpg.Connection:
        if self.safe_mode and self.has_used_primary:
            return self._get_write_connection()

        if force_primary_connection:
            return self._get_write_connection()

        if self.active_transaction:
            return self._get_write_connection()

        if not self.secondary_connections:
            return self._get_write_connection()

        return self.secondary_connections.get_connection()

    def _get_write_connection(self) -> asyncpg.Connection:
        self.has_used_primary = True
        if self.primary_connection is None:
            raise Exception("No primary connection available")
        return self.primary_connection

    def _validate_role(self, role: Role) -> None:
        if role not in [Role.PRIMARY, Role.SECONDARY]:
            raise ValueError(f"Invalid role: {role}")
