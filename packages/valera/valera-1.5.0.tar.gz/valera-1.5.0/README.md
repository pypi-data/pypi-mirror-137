# valera

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/valera/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/valera)
[![PyPI](https://img.shields.io/pypi/v/valera.svg?style=flat-square)](https://pypi.python.org/pypi/valera/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/valera?style=flat-square)](https://pypi.python.org/pypi/valera/)
[![Python Version](https://img.shields.io/pypi/pyversions/valera.svg?style=flat-square)](https://pypi.python.org/pypi/valera/)

Validator for [district42](https://github.com/nikitanovosibirsk/district42) schema

(!) Work in progress, breaking changes are possible until v2.0 is released

## Installation

```sh
pip3 install valera
```

## Usage

`eq` returns `True` or `False`

```python
from district42 import schema
from valera import eq

assert eq(schema.int, 42)

# syntax sugar
assert schema.int == 42
```

`validate` returns `ValidationResult`

```python
from district42 import schema
from valera import validate

res = validate(schema.int, 42)
assert res.get_errors() == []
```

`validate_or_fail` returns `True` or raise `ValidationException`
```python
from district42 import schema
from valera import validate_or_fail

assert validate_or_fail(schema.int, 42)
```

## Documentation

* [Documentation](#documentation)
  * [None](#none)
    * [schema.none](#schemanone)
  * [Bool](#bool)
    * [schema.bool](#schemabool)
    * [schema.bool(`value`)](#schemaboolvalue)
  * [Int](#int)
    * [schema.int](#schemaint)
    * [schema.int(`value`)](#schemaintvalue)
    * [schema.int.min(`value`)](#schemaintminvalue)
    * [schema.int.max(`value`)](#schemaintmaxvalue)
  * [Float](#float)
    * [schema.float](#schemafloat)
    * [schema.float(`value`)](#schemafloatvalue)
    * [schema.float.min(`value`)](#schemafloatminvalue)
    * [schema.float.max(`value`)](#schemafloatmaxvalue)
  * [Str](#str)
    * [schema.str](#schemastr)
    * [schema.str.len(`length`)](#schemastrlenlength)
    * [schema.str.len(`min_length`, `max_length`)](#schemastrlenmin_length-max_length)
    * [schema.str.alphabet(`letters`)](#schemastralphabetletters)
    * [schema.str.contains(`substr`)](#schemastrcontainssubstr)
    * [schema.str.regex(`pattern`)](#schemastrregexpattern)
  * [List](#list)
    * [schema.list](#schemalist)
    * [schema.list(`elements`)](#schemalistelements)
    * [schema.list(`type`)](#schemalisttype)
    * [schema.list(`type`).len(`length`)](#schemalisttypelenlength)
    * [schema.list(`type`).len(`min_length`, `max_length`)](#schemalisttypelenmin_length-max_length)
  * [Dict](#dict)
    * [schema.dict](#schemadict)
    * [schema.dict(`keys`)](#schemadictkeys)
  * [Any](#any)
    * [schema.any](#schemaany)
    * [schema.any(`*types`)](#schemaanytypes)
  * [Custom Types](#custom-types)
    * [1. Declare Schema](#1-declare-schema)
    * [2. Register Validator](#2-register-validator)
    * [3. Use](#3-use)

### None

#### schema.none

```python
sch = schema.none

assert sch == None

assert sch != False  # incorrect type
```

### Bool

#### schema.bool

```python
sch = schema.bool

assert sch == True
assert sch == False

assert sch != None  # incorrect type
```

#### schema.bool(`value`)

```python
sch = schema.bool(True)

assert sch == True

assert sch != False  # incorrect value
```

### Int

#### schema.int

```python
sch = schema.int

assert sch == 42

assert sch != 3.14  # incorrect type
assert sch != "42"  # incorrect type
```

#### schema.int(`value`)

```python
sch = schema.int(42)

assert sch == 42

assert sch != 43  # incorrect value
```

#### schema.int.min(`value`)

```python
sch = schema.int.min(0)

assert sch == 0
assert sch == 1

assert sch != -1  # < min
```

#### schema.int.max(`value`)

```python
sch = schema.int.max(0)

assert sch == 0
assert sch == -1

assert sch != 1  # > max
```

### Float

#### schema.float

```python
sch = schema.float

assert sch == 3.14

assert sch != 3  # incorrect type
assert sch != "3.14"  # incorrect type
```

#### schema.float(`value`)

```python
sch = schema.float(3.14)

assert sch == 3.14

assert sch != 3.15  # incorrect value
```

#### schema.float.min(`value`)

```python
sch = schema.float.min(0.0)

assert sch == 0.0
assert sch == 0.1

assert sch != -0.1  # < min
```

#### schema.float.max(`value`)

```python
sch = schema.float.max(0.0)

assert sch == 0.0
assert sch == -0.1

assert sch != 0.1  # > max
```

### Str

#### schema.str

```python
sch = schema.str

assert sch == ""
assert sch == "banana"

assert sch != None  # incorrect type
```

#### schema.str.len(`length`)

```python
sch = schema.str.len(2)

assert sch == "ab"

assert sch != "a"  # missing symbol
```

#### schema.str.len(`min_length`, `max_length`)

```python
sch = schema.str.len(1, ...)

assert sch == "a"
assert sch == "ab"

assert sch != ""  # missing symbol
```

```python
sch = schema.str.len(..., 2)

assert sch == ""
assert sch == "ab"

assert sch != "abc"  # extra symbol
```

```python
sch = schema.str.len(1, 2)
assert sch == "a"
assert sch == "ab"

assert sch != ""  # missing symbol
assert sch != "abc"  # extra symbol
```

#### schema.str.alphabet(`letters`)

```python
digits = "01234567890"
sch = schema.str.alphabet(digits)

assert sch == "123"

assert sch != "abc"  # incorrect alphabet
```

#### schema.str.contains(`substr`)

```python
sch = schema.str.contains("banana")

assert sch == "banana!"

assert sch != ""
```

#### schema.str.regex(`pattern`)

```python
sch = schema.str.regex(r"[a-z]+")

assert sch == "abc"

assert sch != "123"  # pattern missmatch
```

### List

#### schema.list

```python
sch = schema.list
assert sch == []
assert sch == [1, 2]

assert sch != {}  # incorrect type
```

#### schema.list(`elements`)

```python
sch = schema.list([schema.int(1), schema.int(2)])

assert sch == [1, 2]

assert sch != [1]  # missing element "2"
```

#### schema.list(`type`)

```python
sch = schema.list(schema.int)

assert sch == [42]

assert sch != ["42"]  # incorrect type
```

#### schema.list(`type`).len(`length`)

```python
sch = schema.list(schema.int).len(3)

assert sch == [1, 2, 3]

assert sch != [1, 2]  # missing element
```

#### schema.list(`type`).len(`min_length`, `max_length`)

```python
sch = schema.list(schema.int).len(1, ...)

assert sch == [1]
assert sch == [1, 2]

assert sch != []  # missing element
```

```python
sch = schema.list(schema.int).len(..., 2)

assert sch == []
assert sch == [1, 2]

assert sch != [1, 2, 3]  # extra element
```

```python
sch = schema.list(schema.int).len(1, 2)

assert sch == [1]
assert sch == [1, 2]

assert sch != []  # missing element
assert sch != [1, 2, 3]  # extra element
```

### Dict

#### schema.dict

```python
sch = schema.dict

assert sch == {}
assert sch == {"id": 1}

assert sch != []
```

#### schema.dict(`keys`)

**strict**

```python
sch = schema.dict({
    "id": schema.int,
    optional("name"): schema.str
})

assert sch == {"id": 1}
assert sch == {"id": 1, "name": "Bob"}

assert sch != {"id": 1, "field": "value"}  # extra key 'field'
assert sch != {"id": 1, "name": None}  # incorrect type
```

**relaxed**

```python
sch = schema.dict({
    "id": schema.int,
    optional("name"): schema.str,
    ...: ...
})

assert sch == {"id": 1}
assert sch == {"id": 1, "name": "Bob"}
assert sch == {"id": 1, "field": "value"}
assert sch == {"id": 1, "name": "Bob", "field": "value"}

assert sch != {"id": 1, "name": None}  # incorrect type
```

### Any

#### schema.any

```python
sch = schema.any

assert sch == None
assert sch == 42
assert sch == "banana"
assert sch == []
assert sch == {}
```

#### schema.any(`*types`)

```python
sch = schema.any(schema.str, schema.none)

assert sch == None
assert sch == "banana"

assert sch != 42  # incorrect type
```

### Custom Types

#### 1. Declare Schema

```python
from typing import Any
from uuid import UUID
from district42 import Props, SchemaVisitor, SchemaVisitorReturnType as ReturnType
from district42.types import Schema
from niltype import Nilable


class UUIDProps(Props):
    @property
    def value(self) -> Nilable[UUID]:
        return self.get("value")


class UUIDSchema(Schema[UUIDProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_uuid(self, **kwargs)

    def __call__(self, /, value: UUID) -> "UUIDSchema":
        return self.__class__(self.props.update(value=value))
```

#### 2. Register Validator

```python
from typing import Any
from uuid import UUID
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator


class UUIDValidator(Validator, extend=True):
    def visit_uuid(self, schema: UUIDSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, UUID):
            return result.add_error(error)

        if schema.props.value is not Nil:
            if error := self._validate_value(path, value, schema.props.value):
                return result.add_error(error)

        return result
```

#### 3. Use

```python
from uuid import uuid4
from district42 import register_type, schema
from valera import validate_or_fail

register_type("uuid", UUIDSchema)

assert validate_or_fail(schema.uuid, uuid4())
```

Full code available here: [district42_exp_types/uuid](https://github.com/nikitanovosibirsk/district42-exp-types/tree/master/district42_exp_types/uuid)
