import pytest
from chonf import load, Option


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("mockapp__a", "a")
    monkeypatch.setenv("mockapp__b__b", "b")


def test_by_name(mock_env):
    model = {"a": Option(), "b": {"b": Option()}}
    configs = load(model=model, author="me", name="mockapp")
    assert configs == {"a": "a", "b": {"b": "b"}}


def test_by_prefix(mock_env):
    model = {"a": Option(), "b": {"b": Option()}}
    configs = load(model=model, author="me", name="nope", env_prefix="mockapp")
    assert configs == {"a": "a", "b": {"b": "b"}}
