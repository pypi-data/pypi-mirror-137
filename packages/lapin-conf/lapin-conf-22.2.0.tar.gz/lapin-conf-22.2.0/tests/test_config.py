# Copyright 2022 Ryan Eloff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Type, Dict
import dataclasses

import attrs
import pytest

import lapin


# TODO(rpeloff) test working for other data structures: dict, namedtuple, etc., possibly with cattr


def test_attrsconf_config(wrap_dataclass: bool = False, wrap_attrs: bool = False) -> None:
    class Config:
        foo: int
        bar: str = "test"

    # TODO(rpeloff) parametrize to check @dataclass, @define or plain class
    if wrap_dataclass:
        Config = dataclasses.dataclass(Config)
    if wrap_attrs:
        Config = attrs.define(Config)
    Config = lapin.config(Config)

    expected_dict = {"bar": "test"}
    expected_annotations = {"foo": int, "bar": str}

    _check_config_cls(Config, expected_dict, expected_annotations)

    @Config.configure
    class ConfigurableA:
        ...
    
    @Config.configure
    class ConfigurableB:
        ...

    with pytest.raises(TypeError, match="missing 1 required positional argument: 'foo'"):
        instance = ConfigurableA()

    instance = ConfigurableA(foo=3, bar="this is a test")

    assert instance.foo == 3
    assert instance.bar == "this is a test"

    instance_config = instance.get_config()
    
    expected_config = Config(foo=3, bar="this is a test")
    assert instance_config == expected_config

    expected_config_instance = ConfigurableA.from_config(expected_config)
    assert instance == expected_config_instance

    # OR

    expected_config = Config("configurable_a", foo=3, bar="this is a test")
    assert instance_config == expected_config

    expected_config_instance = expected_config.create()
    assert instance == expected_config_instance

    registered_config = lapin.get_registered_config("configurable_a")


def _check_config_cls(cls: Type, expected_dict: Dict[str, Any], expected_annotations: Dict[str, Type]) -> None:
    assert hasattr(cls, "__attrs_attrs__")
    
    for k, v in expected_dict.items():
        assert getattr(cls, k) == v

    for k, v in expected_annotations.items():
        assert cls.__annotations__[k] is v
