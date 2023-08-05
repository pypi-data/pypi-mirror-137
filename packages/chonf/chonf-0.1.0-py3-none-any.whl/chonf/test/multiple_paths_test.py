from chonf import load, Option
import pytest, toml, json

model = {
    "a": Option(),
    "b": {
        "a": Option(),
        "b": {
            "a": Option(),
            "b": Option(),
        },
    },
}


@pytest.fixture(scope="session")
def system_configs(tmp_path_factory):
    system = tmp_path_factory.mktemp("chonf_multiple_path_system")
    with open(system / "config.toml", "w") as config_file:
        toml.dump({"a": "system", "b": {"a": "system"}}, config_file)
    return system


@pytest.fixture(scope="session")
def user_configs(tmp_path_factory):
    user = tmp_path_factory.mktemp("chonf_multiple_path_user")
    with open(user / "config.json", "w") as config_file:
        json.dump({"b": {"a": "user", "b": {"a": "user"}}}, config_file)
    return user


@pytest.fixture(scope="session")
def mock_configs(user_configs, system_configs):
    configs = load(
        model=model,
        author="me",
        name="asdfghjkl",
        env_prefix="asdfghjkl",
        path=[user_configs, system_configs],  # fist should have greater priority
    )
    return configs


def test_first(mock_configs):
    assert mock_configs["b"]["b"]["a"] == "user"


def test_last(mock_configs):
    assert mock_configs["a"] == "system"


def test_shadow(mock_configs):
    assert mock_configs["b"]["a"] == "user"
