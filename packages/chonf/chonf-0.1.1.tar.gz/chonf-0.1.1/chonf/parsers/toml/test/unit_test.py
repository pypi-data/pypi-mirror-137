import pytest
import toml

from chonf.exceptions import SkipSource, NotSubtree
from chonf.parsers.toml import read, list_children

DATA = {
    "option1": "value1",
    "section1": {
        "option2": "value2",
        "repeat": {
            "one": 1,
            "two": 2,
            "three": 3,
        },
    },
    "empty": {},
}


@pytest.fixture(scope="module")
def config_dir(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("chonf_test_toml")
    with open(tmp_path / "config.toml", "w") as toml_file:
        toml.dump(DATA, toml_file)
    return tmp_path


@pytest.fixture(scope="module")
def empty_config_dir(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("chonf_test_toml_empty")
    dir_path = tmp_path / "empty"
    dir_path.mkdir()
    return dir_path


def test_shallow(config_dir):
    key = "option1"
    assert read(keys=[key], path=config_dir) == DATA[key]


def test_shallow_missing(config_dir):
    key = "option3"
    with pytest.raises(SkipSource):
        read(keys=[key], path=config_dir)


def test_nested(config_dir):
    k1, k2 = "section1", "option2"
    assert read(keys=[k1, k2], path=config_dir) == DATA[k1][k2]


def test_nested_missing(config_dir):
    k1, k2 = "section1", "option4"
    with pytest.raises(SkipSource):
        read(keys=[k1, k2], path=config_dir)


def test_missing_file(empty_config_dir):
    with pytest.raises(SkipSource):
        read(keys=["option"], path=empty_config_dir)


def test_list_children_success(config_dir):
    """in this case, list_children should be able to list the child keys"""
    assert list_children(keys=["section1", "repeat"], path=config_dir) == {
        "one",
        "two",
        "three",
    }


def test_list_children_nonexistant(config_dir):
    """in this case, list_children receives a nonexistant key,
    and should return an empty set."""
    assert list_children(keys=["nonexistant"], path=config_dir) == set()


def test_list_children_empty(config_dir):
    """in this case, list_children receives a key to an empty
    dict, and should return an empty set."""
    assert list_children(keys=["empty"], path=config_dir) == set()


def test_list_children_fail(config_dir):
    """in this case, list_children receives a key to a value,
    not a subdict, so it should raise a TypeErr"""
    with pytest.raises(NotSubtree) as err:
        list_children(keys=["option1"], path=config_dir)
    assert err.value.value == "value1"
