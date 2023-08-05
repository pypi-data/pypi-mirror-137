import pytest
import json
import toml
from chonf import Option, load

ENV_PREFIX = "mockapp"

MODEL = {
    "name": Option(),
    "nickname": Option(),
    "email": Option(),
    "system": {
        "background": Option("desert"),
        "theme": Option("dark"),
        "id": Option(),
        "web": {
            "homepages": Option(
                {
                    "job": "job.com",
                    "music": "music.com",
                }
            ),
            "key": "123456",
        },
    },
}


@pytest.fixture(scope="session")
def session_patch():
    mpatch = pytest.MonkeyPatch()
    yield mpatch
    mpatch.undo()
    # thanks to Rich Inman: https://stackoverflow.com/questions/53963822/python-monkeypatch-setattr-with-pytest-fixture-at-module-scope


@pytest.fixture(scope="session")
def mock_configs(tmp_path_factory, session_patch):
    session_patch.setenv("mockapp__name", "Leibniz Hamilton")
    session_patch.setenv("mockapp__system__theme", "light")
    dir_path = tmp_path_factory.mktemp("mockapp")
    toml_data = {
        "email": "laib.dbz@hotmail.com",
        "system": {"id": "lebzlebz"},
    }
    json_data = {
        "nickname": "Laibilton",
        "system": {
            "background": "flowers",
        },
    }
    with open(dir_path / "config.json", "w") as json_file:
        json.dump(json_data, json_file)
    with open(dir_path / "config.toml", "w") as toml_file:
        toml.dump(toml_data, toml_file)
    return load(MODEL, author="me", name="mockapp", env_prefix="mockapp", path=dir_path)


class TestEnv:
    def test_shallow(self, mock_configs):
        assert mock_configs["name"] == "Leibniz Hamilton"

    def test_nested(self, mock_configs):
        assert mock_configs["system"]["theme"] == "light"


class TestJson:
    def test_shallow(self, mock_configs):
        assert mock_configs["nickname"] == "Laibilton"

    def test_nested(self, mock_configs):
        assert mock_configs["system"]["background"] == "flowers"


class TestToml:
    def test_shallow(self, mock_configs):
        assert mock_configs["email"] == "laib.dbz@hotmail.com"

    def test_nested(self, mock_configs):
        assert mock_configs["system"]["id"] == "lebzlebz"
