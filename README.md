<h1 align="center">EasyAsyncPg</h1>
<p align="center"><i>Wrapper for asyncpg that makes it easier to use and adds new functionalities</i></p>

<div align="center">
    <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python 3.11"/></a>
    <a href="https://github.com/camcima/easyasyncpg/actions/workflows/main.yml"><img src="https://github.com/camcima/easyasyncpg/actions/workflows/main.yml/badge.svg" alt="build status"/></a>
    <a href="https://sonarcloud.io/component_measures?id=camcima_easyasyncpg&metric=coverage&view=list"><img src="https://sonarcloud.io/api/project_badges/measure?project=camcima_easyasyncpg&metric=coverage" alt="Coverage">
    <a href="https://sonarcloud.io/project/issues?resolved=false&types=VULNERABILITY&id=loggi_loggy"><img src="https://sonarcloud.io/api/project_badges/measure?project=camcima_easyasyncpg&metric=vulnerabilities" alt="Vulnerabilities">
    <a href="https://sonarcloud.io/project/issues?resolved=false&types=BUG&id=camcima_easyasyncpg"><img src="https://sonarcloud.io/api/project_badges/measure?project=camcima_easyasyncpg&metric=bugs" alt="Bugs">
    <a href="https://sonarcloud.io/summary/overall?id=camcima_easyasyncpg"><img src="https://sonarcloud.io/api/project_badges/measure?project=camcima_easyasyncpg&metric=alert_status" alt="Quality Gate Status">
</div>

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
