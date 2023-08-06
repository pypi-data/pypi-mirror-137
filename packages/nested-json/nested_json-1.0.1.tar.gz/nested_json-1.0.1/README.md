# nested-json

![PyPI](https://img.shields.io/pypi/v/nested-json?style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dw/nested-json?style=flat-square) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/szikszail/nested-json?style=flat-square)

A library to manage JSONs with encoded JSON more effectively (e.g. AWS Event Bridge Events, AWS API Gateway Events)

## Install

```shell
pip install nested_json
```

## Usage

```python
import nested_json as njson
```

The main API of the library consist of:

* `Nested(obj)` - to convert any list or dictionary to a nested one
* `parse(str)` - to parse a JSON string to a nested JSON
* `process(obj)` - to process/stringify any nested JSON
* `dumps(obj)`,  `dump(obj, fp)` - same as from the `json` module, but supports nested JSON
* `loads(str)`,  `load(fp)` - same as from the `json` module, but supports nested JSON

### Marking `dict` / `list` as nested

The `Nested` function can be used to mark a dictionary or
list as nested data, which will add a particular property to it, 
marking it nested. This property was later removed during processing.

```python
data = {
  "id": "12345",
  "event": {
    "payload": {
      "rawpayload": njson.Nested({
        "key": "value",
        "other": 2,
        "foo": True
      }),
      "tags": njson.Nested([
        "hello",
        "world
      ])
    }
  }
}
# {
#   "id": "12345",
#   "event": {
#     "payload": {
#       "rawpayload": {
#         "__nested__": True,
#         "key": "value",
#         "other": 2,
#         "foo": True
#       },
#       "tags": [
#         "__nested__",
#         "hello",
#         "world
#       ]
#     }
#   }
# }
```

### Processing nested JSON

Using the `process` function, the nested keys can be removed
and nested data converted to JSON string.

```python
processed_data = njson.process(data)
# {
#   "id": "12345",
#   "event": {
#     "payload": {
#       "rawpayload": "{\"key\": \"value\", \"other\": 2, \"foo\": true}",
#       "tags": "[\"hello\", \"world\"]"
#     }
#   }
# }
```

### Converting to JSON string

The result of `process` can be already passed to `json.dumps` , 
but the `njson.dumps` can also be used with nested JSON data.

```python
json_string = njson.dumps(data)

# '{"id": "12345", "event": {"payload": {"rawpayload": "{\\"key\\": \\"value\\", \\"other\\": 2, \\"foo\\": true}", "tags": "[\\"hello\\", \\"world\\"]"}}}'
```

### Parsing JSON string

Nested JSON string can be parsed to nested JSON data with the `loads` function or the `parse` function

```python
assert njson.loads(json_string) == data
assert njson.parse(processed_data) == data
assert njson.parse(json.loads(json_string)) == data
```

## Compatibility

Note that both `loads` and `dumps` use the `json.loads` and `json.dumps` functions; thus they can be used with "normal" JSON as well.
