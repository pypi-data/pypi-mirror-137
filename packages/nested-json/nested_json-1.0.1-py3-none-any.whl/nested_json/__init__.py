import json
import re
from typing import IO, Any

__version__ = "1.0.1"

__NESTED__ = "__nested__"


class CircularReferenceError(Exception):
    pass


def Nested(obj: Any, in_place: bool = False) -> Any:
    """Decorates the object passed (in place or not)
    to mark it as nested JSON, i.e. in the final object
    it will be stringifyed.

    Args:
        obj (Any): The object to mark nested.
        in_place (bool, optional): Should the original object be modified. Defaults to False.

    Returns:
        Any: The marked object.
    """
    if type(obj) is dict:
        if not in_place:
            obj = obj.copy()
        obj[__NESTED__] = True
    elif type(obj) is list:
        if not in_place:
            obj = obj.copy()
        obj.insert(0, __NESTED__)
    return obj


def _is_json_string(s: str) -> bool:
    p = re.compile(r'^(?:\{.*\}|\[.*\])$')
    return bool(p.match(s))


def parse(obj: Any) -> Any:
    """Parses any nested (stringifyed) JSON in the passed object
    to nested JSON objects, to easily and effectively handle it.

    Args:
        obj (Any): The object to parse.

    Returns:
        Any: The parsed object with nested JSON object, if there was any.
    """
    if type(obj) is str and _is_json_string(obj):
        return Nested(loads(obj))
    if type(obj) is dict:
        return {k: parse(v) for k, v in obj.items()}
    if type(obj) is list:
        return [parse(i) for i in obj]
    if type(obj) is tuple:
        return tuple(parse(i) for i in obj)
    return obj


def process(obj: Any) -> Any:
    """Processes the passed object, particularly any nested JSON in it,
    dumps the nested JSON to JSON string.

    Args:
        obj (Any): The object to process.

    Returns:
        Any: The processed object (with any nested JSON dumped).
    """
    if type(obj) is list:
        if __NESTED__ not in obj:
            return [process(i) for i in obj]
        obj = obj.copy()
        obj.remove(__NESTED__)
        return json.dumps(process(obj))
    if type(obj) is dict:
        if __NESTED__ not in obj:
            return {k: process(v) for k, v in obj.items()}
        obj = obj.copy()
        obj.pop(__NESTED__)
        return json.dumps(process(obj))
    if type(obj) is tuple:
        return tuple(process(i) for i in obj)
    return obj


def dump(obj: Any, fp: IO[str], **kwargs) -> None:
    """Serialize obj as a JSON formatted stream to fp
    (a .write()-supporting file-like object) using this conversion table.

    Same as json.dump, but it supports nested JSONs
    (https://docs.python.org/3/library/json.html)

    Args:
        obj (Any): The object to serialize.
        fp (IO[str]): The file pointer.
        **kwargs: Any other argument to pass (same as json.dump).
    """
    json.dump(process(obj), fp, **kwargs)


def dumps(obj: Any, **kwargs) -> str:
    """Serialize obj to a JSON formatted str using this conversion table.
    The arguments have the same meaning as in dump().

    Same as json.dumps, but it supports nested JSONs
    (https://docs.python.org/3/library/json.html)

    Args:
        obj (Any): The object to serialize.
        **kwargs: Any other argument to pass (same as json.dumps).

    Returns:
        str: The JSON string representation of the object.
    """
    return json.dumps(process(obj), **kwargs)


def load(fp: IO[str], **kwargs) -> Any:
    """Deserialize fp (a .read()-supporting text file or binary file
    containing a JSON document) to a Python object using this conversion table.

    Same as json.load, but it supports nested JSONs
    (https://docs.python.org/3/library/json.html)

    Args:
        fp (IO[str]): The file pointer.
        **kwargs: Any other argument to pass (same as json.load).

    Returns:
        Any: The deserialized object, with nested JSON if needed.
    """
    return parse(json.load(fp, **kwargs))


def loads(s: str, **kwargs) -> Any:
    """Deserialize s (a str, bytes or bytearray instance containing a JSON document)
    to a Python object using this conversion table.
    The other arguments have the same meaning as in load().

    Same as json.loads, but it supports nested JSONs
    (https://docs.python.org/3/library/json.html)

    Args:
        s (str): The JSON string to deserialize.

    Returns:
        Any: The deserialized object, with nested JSON if needed.
    """
    return parse(json.loads(s, **kwargs))
