import pytest
import os

from chonf.exceptions import SkipSource, NotSubtree
from chonf.parsers.env import read, list_children

ENV_PREFIX = "mockapp"

SHALLOW_KEYS = ["some_option"]
SHALLOW_KEY = "__".join([ENV_PREFIX, *SHALLOW_KEYS])

NESTED_KEYS = ["a_section", "other_option"]
NESTED_KEY = "__".join([ENV_PREFIX, *NESTED_KEYS])

VALUE = "something_maybe_important"


def test_shallow(monkeypatch):
    monkeypatch.setenv(SHALLOW_KEY, VALUE)
    assert read(keys=SHALLOW_KEYS, env_prefix=ENV_PREFIX) == VALUE


def test_shallow_empty(monkeypatch):
    monkeypatch.delenv(SHALLOW_KEY, raising=False)
    with pytest.raises(SkipSource):
        read(keys=SHALLOW_KEYS, env_prefix=ENV_PREFIX)


def test_nested(monkeypatch):
    monkeypatch.setenv(NESTED_KEY, VALUE)
    assert read(keys=NESTED_KEYS, env_prefix=ENV_PREFIX) == VALUE


def test_nested_empty(monkeypatch):
    monkeypatch.delenv(NESTED_KEY, raising=False)
    with pytest.raises(SkipSource):
        read(keys=NESTED_KEYS, env_prefix=ENV_PREFIX)


def test_list_children_success(monkeypatch):
    """success case, should return set of keys"""
    monkeypatch.setenv("app__repeat__group1__item1", "1.1")
    monkeypatch.setenv("app__repeat__group1__item2", "1.2")
    monkeypatch.setenv("app__repeat__group2__item1", "2.1")
    monkeypatch.setenv("app__repeat__group2__item2", "2.2")
    assert list_children(keys=["repeat"], env_prefix="app") == {"group1", "group2"}


def test_list_children_empty(monkeypatch):
    """empty case, should return empty set"""
    for key in os.environ:
        if key.startswith("app__repeat"):
            monkeypatch.delenv(key, raising=False)
    assert list_children(keys=["repeat"], env_prefix="app") == set()


def test_list_children_fail(monkeypatch):
    """error case, for when the key is for a value and not a sub-dict"""
    monkeypatch.setenv("app__repeat", "test")
    with pytest.raises(NotSubtree) as err:
        list_children(keys=["repeat"], env_prefix="app")
    assert err.value.value == "test"
