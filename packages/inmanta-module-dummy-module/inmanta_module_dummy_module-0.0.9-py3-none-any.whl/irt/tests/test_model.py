"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import pydantic
import pytest

from irt.modules import ModuleSetDefinition


@pytest.mark.parametrize(
    "value,valid_constraint",
    [
        ("inmanta", True),
        ("inmanta~=1.2.3", True),
        ("inmanta~=1.2", True),
        ("inmanta~=11.22.33", True),
        ("inmanta~=11.22", True),
        ("inmanta ~= 1.2.3", True),
        ("inmanta_test-123~=1.2.3", True),
        ("inmanta==1.2.3", False),
        ("inmanta~=1", False),
        ("inmanta~=", False),
    ],
)
def test_regex_on_module_set_definition(value: str, valid_constraint: bool):
    """
    Test whether the regex defined on the modules field of the ModuleSetDefinition class works correctly.
    """
    if valid_constraint:
        ModuleSetDefinition(name="test", modules=[value])
    else:
        with pytest.raises(pydantic.ValidationError):
            ModuleSetDefinition(name="test", modules=[value])
