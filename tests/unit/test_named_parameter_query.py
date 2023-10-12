import pytest
from easyasyncpg.named_parameter_query import NamedParameterQuery


def test_simple_query():
    named_query = "SELECT * FROM fruits WHERE name = :name;"
    named_params = {"name": "apple"}

    query = NamedParameterQuery(named_query, named_params)

    assert query.positional_query == "SELECT * FROM fruits WHERE name = $1;"
    assert query.positional_params == ["apple"]


def test_multiple_named_params():
    named_query = "SELECT * FROM fruits WHERE name = :name AND id = :id;"
    named_params = {"name": "apple", "id": 1}

    query = NamedParameterQuery(named_query, named_params)

    assert query.positional_query == "SELECT * FROM fruits WHERE name = $1 AND id = $2;"
    assert query.positional_params == ["apple", 1]


def test_underscored_param_names():
    named_query = "SELECT * FROM fruits WHERE first_name = :first_name AND id = :id;"
    named_params = {"first_name": "apple", "id": 1}

    query = NamedParameterQuery(named_query, named_params)

    assert (
        query.positional_query
        == "SELECT * FROM fruits WHERE first_name = $1 AND id = $2;"
    )
    assert query.positional_params == ["apple", 1]


def test_camel_case_param_names():
    named_query = "SELECT * FROM fruits WHERE firstName = :firstName AND id = :id;"
    named_params = {"firstName": "apple", "id": 1}

    query = NamedParameterQuery(named_query, named_params)

    assert (
        query.positional_query
        == "SELECT * FROM fruits WHERE firstName = $1 AND id = $2;"
    )
    assert query.positional_params == ["apple", 1]


def test_param_names_with_numbers():
    named_query = "SELECT * FROM fruits WHERE name = :name1 AND id = :id;"
    named_params = {"name1": "apple", "id": 1}

    query = NamedParameterQuery(named_query, named_params)

    assert query.positional_query == "SELECT * FROM fruits WHERE name = $1 AND id = $2;"
    assert query.positional_params == ["apple", 1]


def test_numeric_param_names():
    named_query = "SELECT * FROM fruits WHERE name = :1 AND id = :2;"
    named_params = {"1": "apple", "2": 1}

    query = NamedParameterQuery(named_query, named_params)

    assert query.positional_query == "SELECT * FROM fruits WHERE name = $1 AND id = $2;"
    assert query.positional_params == ["apple", 1]


def test_missing_param():
    named_query = "SELECT * FROM fruits WHERE name = :name AND id = :id;"
    named_params = {"name": "apple"}

    with pytest.raises(ValueError) as excinfo:
        NamedParameterQuery(named_query, named_params)

    assert "Missing parameter: id" in str(excinfo.value)


def test_invalid_param_type():
    named_query = "SELECT * FROM fruits WHERE name = :name AND id = :id;"
    named_params = "apple"

    with pytest.raises(ValueError) as excinfo:
        NamedParameterQuery(named_query, named_params)

    assert "params must be a dict or a list of dicts, not <class 'str'>" in str(
        excinfo.value
    )


def test_list_of_dicts():
    named_query = "INSERT INTO fruits (id, name) (:id, :name);"
    named_params = [
        {"id": 1, "name": "apple"},
        {"id": 2, "name": "banana"},
    ]

    query = NamedParameterQuery(named_query, named_params)

    assert query.positional_query == "INSERT INTO fruits (id, name) ($1, $2);"
    assert query.positional_params == [[1, "apple"], [2, "banana"]]
