import json
from typing import Any, Dict, List
from urllib.parse import urlencode
from slugify import slugify


def to_camel_case(value: str) -> str:
    words = []
    split_on = {" ", "_", "-"}
    word = ""
    for char in value:
        if char in split_on:
            if word:
                words.append(word.capitalize())
            word = ""
        else:
            word += char

    if word:
        words.append(word.capitalize())

    return "".join(words)


def to_snake_case(value: str) -> str:
    return slugify(value.lower()).replace("-", "_")


def to_query_string(data: Dict[str, List[Any]]) -> str:
    return urlencode(data, doseq=True)


def jsondump(data) -> str:
    return json.dumps(data)
