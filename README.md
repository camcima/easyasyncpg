# EasyAsyncPg

## Introduction

`EasyAsyncPg` is a Python library that provides a convenient, high-level API to work with PostgreSQL databases using `asyncpg`. The library allows you to manage multiple database connections, transactional operations, and parameterized queries in an easy-to-use manner.

## Features

- **Primary and Secondary Connections**: Distribute database reads and writes efficiently.
- **Transaction Management**: Easily begin, commit, or rollback transactions.
- **Safe Mode**: Optionally enforce read-write separation.
- **Connection Weights**: Specify the weight for secondary connections for custom load balancing.

## Installation

To install `EasyAsyncPg`, you can use `pip`:

```bash
pip install easyasyncpg
```

or, if you use `poetry`:

```bash
poetry add easyasyncpg
```


## Basic Usage

### Initialization

```python
from easyasyncpg import EasyAsyncPg

db = EasyAsyncPg(safe_mode=True)
```

### Adding Connections

```python
await db.add_connection(
    host="localhost",
    user="postgres",
    password="postgres",
    database="mydb",
    port=5432,
    role=Role.PRIMARY,
    weight=1,
)
```

### Executing Queries

```python
await db.execute("INSERT INTO users (name, age) VALUES (:name, :age)", {"name": "Alice", "age": 30})
```

### Transaction Management

```python
async def my_transaction(db):
    await db.execute("UPDATE users SET age=31 WHERE name='Alice'")
    
await db.execute_transaction(my_transaction)
```

## API Reference

### `EasyAsyncPg`

#### Methods

- `add_connection(...)`: Add a new database connection.
- `get_connections()`: Get all active connections.
- `begin_transaction()`: Begin a new transaction.
- `commit_transaction()`: Commit the current transaction.
- `rollback_transaction()`: Rollback the current transaction.
- `execute(...)`: Execute a SQL query.
- `execute_many(...)`: Execute a SQL query multiple times.
- `fetch_all(...)`: Fetch all rows from a SQL query.
- `fetch_one(...)`: Fetch one row from a SQL query.
- `fetch_val(...)`: Fetch a single value from a SQL query.
- `fetch_column(...)`: Fetch a single column from a SQL query.
- `fetch_key_pairs(...)`: Fetch key-value pairs from a SQL query.

## Contributing

Feel free to open an issue or submit a pull request if you find any bugs or have suggestions for additional features.

## License

MIT License. See [LICENSE](LICENSE) for more information.
