from pyparsing import Opt
from chonf import load, Option, Required, ConfigLoadingIncomplete
import pytest
import json
from functools import partial

from chonf.exceptions import InvalidOption


@pytest.fixture(scope="module")
def preset_load(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("chonf_pre_processing_test")
    data = {
        "a": "1",
        "b": {"a": 1, "b": {"a": 1.5, "b": {"a": "one"}}},
        "c": "1.0",
        "d": "1.5",
        "e": 1.0,
    }
    with open(tmp_dir / "config.json", "w") as f:
        json.dump(data, f)
    return partial(
        load,
        author="me",
        name="myapp",
        path=tmp_dir,
    )


def test_numeric_success(preset_load):
    """Tests a simple pre-processing function that tries
    to convert certain options to floats, in this case they should
    succeed.
    """

    def into_float(value):
        try:
            return float(value)
        except ValueError:
            raise InvalidOption(value, "convertible to float") from ValueError

    model = {
        "a": Option(pre_process=into_float),
        "b": {
            "a": Option(pre_process=into_float),
            "b": {"a": Required(pre_process=into_float), "b": {"a": Required()}},
        },
    }
    config = preset_load(model=model)
    assert config == {"a": 1.0, "b": {"a": 1.0, "b": {"a": 1.5, "b": {"a": "one"}}}}


def test_numeric_failure(preset_load):
    """Tests a simple pre-processing function that tries
    to convert ceretain options to integers, in this case some
    should fail and some should succeed.
    """

    def into_int(value):
        # test if number can be read as integer, even if it has a dot
        try:
            fvalue = float(value)
            ivalue = int(fvalue)
            if fvalue == ivalue:
                return ivalue
            else:
                raise InvalidOption(value, "convertible to int")
        except ValueError as err:
            raise InvalidOption(value, "convertible to int") from err

    model = {
        "a": Option(pre_process=into_int),
        "b": {
            "a": Option(pre_process=into_int),
            "b": {
                "a": Required(pre_process=into_int),
                "b": {
                    "a": Required(pre_process=into_int),
                },
            },
        },
        "c": Option(pre_process=into_int),
        "d": Option(pre_process=into_int),
        "e": Option(pre_process=into_int),
    }
    with pytest.raises(ConfigLoadingIncomplete) as err:
        preset_load(model=model)
    assert err.value.loaded_configs == {
        "a": 1,
        "b": {
            "a": 1,
            "b": {
                "a": InvalidOption(1.5, "convertible to int"),
                "b": {
                    "a": InvalidOption("one", "convertible to int"),
                },
            },
        },
        "c": 1,
        "d": InvalidOption("1.5", "convertible to int"),
        "e": 1,
    }
