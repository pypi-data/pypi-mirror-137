from chonf import load, Option, Required, Repeat, ConfigLoadingIncomplete
import pytest
import json

from chonf.exceptions import InvalidOption

MODEL = {
    "option_a": Option(),
    "option_b": Option(),
    "option_repeat": Repeat(Option()),
    "users": Repeat(
        {
            "name": Required(),
            "nick": Option(),
        }
    ),
}

VALID_DATA = {
    "option_a": "value_a",
    "option_b": "value_b",
    "option_repeat": {"a": "a", "b": "b", "c": "c"},
    "users": {
        "user_1": {
            "name": "Jean Jacques Rousseau",
            "nick": "Jack",
        },
        "user_2": {
            "name": "Mary Wollstonecraft",
        },
        "user_3": {"name": "James Hoffman", "nick": "Internet Coffee Dude"},
    },
}

INVALID_DATA = {
    "option_a": "value_a",
    "option_b": "value_b",
    "option_repeat": "invalid_value",  # this should be a subtree
    "users": {
        "user_1": {
            "name": "Jean Jacques Rousseau",
            "nick": "Jack",
        },
        "user_2": {
            "nick": "Did she have a nickname?",  # no name on this one
        },
        "user_3": {"name": "James Hoffman", "nick": "Internet Coffee Dude"},
    },
}


@pytest.fixture(scope="module")
def valid_conf_dir(tmp_path_factory):
    dir_path = tmp_path_factory.mktemp("chonf_repeat_test_valid")
    with open(dir_path / "config.json", "w") as f:
        json.dump(VALID_DATA, f)
    return dir_path


@pytest.fixture(scope="module")
def invalid_conf_dir(tmp_path_factory):
    dir_path = tmp_path_factory.mktemp("chonf_repeat_test_invalid")
    with open(dir_path / "config.json", "w") as f:
        json.dump(INVALID_DATA, f)
    return dir_path


def test_valid_data(valid_conf_dir):
    configs = load(MODEL, author="me", name="mock", path=valid_conf_dir)
    assert configs == {
        "option_a": "value_a",
        "option_b": "value_b",
        "option_repeat": {"a": "a", "b": "b", "c": "c"},
        "users": {
            "user_1": {
                "name": "Jean Jacques Rousseau",
                "nick": "Jack",
            },
            "user_2": {
                "name": "Mary Wollstonecraft",
                "nick": None,  # here the not found value reads to None
            },
            "user_3": {"name": "James Hoffman", "nick": "Internet Coffee Dude"},
        },
    }


@pytest.fixture(scope="module")
def invalid_data_error(invalid_conf_dir):
    with pytest.raises(ConfigLoadingIncomplete) as err:
        load(MODEL, author="me", name="mock", path=invalid_conf_dir)
    return err.value


def test_invalid_data_loaded_configs(invalid_data_error):
    assert invalid_data_error.loaded_configs == {
        "option_a": "value_a",
        "option_b": "value_b",
        "option_repeat": InvalidOption("invalid_value", Repeat(Option())),
        "users": {
            "user_1": {
                "name": "Jean Jacques Rousseau",
                "nick": "Jack",
            },
            "user_2": {
                "name": InvalidOption(None, Required()),
                "nick": "Did she have a nickname?",  # no name on this one
            },
            "user_3": {"name": "James Hoffman", "nick": "Internet Coffee Dude"},
        },
    }
