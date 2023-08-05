from chonf import load, Required, ConfigLoadingIncomplete
import pytest


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv("mockapp__aaa", "value_a")
    monkeypatch.setenv("mockapp__bbb__ccc", "value_b")


def test_read(env_vars):
    model = {"aaa": Required(), "bbb": {"ccc": Required()}}
    conf = load(model, author="me", name="mockapp", env_prefix="mockapp")
    assert conf["aaa"] == "value_a" and conf["bbb"]["ccc"] == "value_b"


def test_fail(env_vars):
    model = {"aaa": Required(), "bbb": {"ccd": Required()}, "ccc": Required()}
    with pytest.raises(ConfigLoadingIncomplete) as err:
        load(model, author="me", name="mockapp", env_prefix="mockapp")
    assert err.value.unlocated_keys == [["bbb", "ccd"], ["ccc"]]
