from collections import OrderedDict
from functools import lru_cache
from dataclasses import dataclass, field
import re
from typing import List


__all__ = (
    'SHORTCODE_NAME_REGEX_SOURCE',
    'SHORTCODE_REGEX_SOURCE',
    'ATTRIBUTES_REGEX_SOURCE',
    'SHORTCODE_REGEX',
    'ATTRIBUTES_REGEX',

    'Entity',

    'get_shortcode_regex',
    'parse_attributes',
    'find_entities',
)

SHORTCODE_NAME_REGEX_SOURCE = r'[0-9a-z_\:\~\.-]+'
SHORTCODE_REGEX_SOURCE = (
    r'\['                              # Opening bracket.
    r'(\[?)'                           # 1: Optional second opening bracket for escaping shortcodes: [[tag]].
    r'(?P<name>{name})'                # 2: Shortcode name.
    r'(?![\w-])'                       # Not followed by word character or hyphen.
    r'(?P<attributes>'                 # 3: Unroll the loop: Inside the opening shortcode tag.
        r'[^\]\/]*'                    # Not a closing bracket or forward slash.
        r'(?:'
            r'\/(?!\])'                # A forward slash not followed by a closing bracket.
            r'[^\]\/]*'                # Not a closing bracket or forward slash.
        r')*?'
    r')'
    r'(?:'
        r'(\/)'                        # 4: Self closing tag...
        r'\]'                          # ...and closing bracket.
    r'|'
        r'\]'                          # Closing bracket.
        r'(?:'
            r'(?P<content>'            # 5: Unroll the loop: Optionally, anything between the opening and closing shortcode tags.
                r'[^\[]*'              # Not an opening bracket.
                r'(?:'
                    r'\[(?!\/\2\])'    # An opening bracket not followed by the closing shortcode tag.
                    r'[^\[]*'          # Not an opening bracket.
                r')*'
            r')'
            r'\[\/\2\]'                # Closing shortcode tag.
        r')?'
    r')'
    r'(\]?)'
)
ATTRIBUTES_REGEX_SOURCE = (
    r'([\w-]+)\s*=\s*"([^"]*)"(?:\s|$)|([\w-]+)\s*=\s*\'([^\']*)\'(?:\s|$)|([\w-]+)\s*=\s*([^\s\'"]+)(?:\s|$)|"([^"]*)"(?:\s|$)|\'([^\']*)\'(?:\s|$)|(\S+)(?:\s|$)'
)


@lru_cache
def get_shortcode_regex(name_regex: str) -> re.Pattern:
    return re.compile(
        SHORTCODE_REGEX_SOURCE.format(name=name_regex), re.I | re.M
    )


SHORTCODE_REGEX = get_shortcode_regex(SHORTCODE_NAME_REGEX_SOURCE)
ATTRIBUTES_REGEX = re.compile(ATTRIBUTES_REGEX_SOURCE, re.I | re.M)


@dataclass
class Entity:
    name: str
    start: int
    end: int
    match: re.Match
    content: str = ''
    source: str = ''
    attributes: OrderedDict = field(default_factory=OrderedDict)


def parse_attributes(repr: str) -> OrderedDict:
    attrs = OrderedDict()
    parsed = ATTRIBUTES_REGEX.findall(repr)

    # Where:
    # k{n} - Key, that we should check for non emptiness.
    # v{n} - It's value.
    for k1, v1, k2, v2, k3, v3, k4, k5, k6 in parsed:
        attrs[k1 or k2 or k3 or k4 or k5 or k6] = v1 or v2 or v3 or ''

    return attrs


def match_to_entity(match: re.Match) -> Entity:
    entity = Entity(
        name=match['name'], content=match['content'] or '',
        attributes=parse_attributes(match['attributes']),
        match=match, start=match.start(), end=match.end(),
    )
    entity.source = match.string[entity.start:entity.end]

    return entity


def find_entities(
    content: str,
    name_regex: str = SHORTCODE_NAME_REGEX_SOURCE,
) -> List[Entity]:
    return [
        match_to_entity(match)
        for match in get_shortcode_regex(name_regex).finditer(content)
    ]
