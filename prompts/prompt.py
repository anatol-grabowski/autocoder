# I start with a blank python file, and incrementally modify it by adding code.
# Libraries (e.g. os, sys, re, json, np, etc.) are imported.

# Create a function that tests if an iterable conains all values from another iterable.
def contains_all(iterable, other):
    does_contain = all(x in iterable for x in other)
    return does_contain

# Create a function that reads a key on a json object by path.
# Example: read_json_key({'a': [1, 2, 3]}, 'a[1]') returns 2.
def read_json_field(obj, path):
    parts_re = '(\[\d+\])|([^.].*?)'
    parts = re.findall(parts_re, path)
    val = obj
    for part in parts:
        if part[0] is not None:
            key = int(part[0][1:-1])
        else:
            key = part[1]
        val = val[key]
    return val
