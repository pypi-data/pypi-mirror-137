from baby_steps import given, then, when
from district42 import schema
from district42.types import TypeAliasSchema
from th import PathHolder

from valera import validate
from valera.errors import MinValueValidationError


def test_alias_default_validation():
    with given:
        sch = TypeAliasSchema()

    with when:
        result = validate(sch, None)

    with then:
        assert result.get_errors() == []


def test_alias_validation():
    with given:
        sch = schema.alias("uint", schema.int.min(0))

    with when:
        result = validate(sch, 42)

    with then:
        assert result.get_errors() == []


def test_alias_validation_error():
    with given:
        min_value = 0
        sch = schema.alias("uint", schema.int.min(min_value))
        actual_value = -1

    with when:
        result = validate(sch, actual_value)

    with then:
        assert result.get_errors() == [
            MinValueValidationError(PathHolder(), actual_value, min_value)
        ]
