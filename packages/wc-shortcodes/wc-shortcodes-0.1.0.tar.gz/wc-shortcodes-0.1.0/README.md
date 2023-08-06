# Text shortcodes resolver

## Installation

```sh
pip install wc-shortcodes
```

## Usage

Simple usage:

```python
from wc_shortcodes.registry import CodesRegistry
from wc_shortcodes.transformer import transform


registry = CodesRegistry()


# Adding handler for a specific shortcode:
@registry.register()
def shortcode(entity, context={}):
  return entity.content


# Transforming some content using registered resolvers.
transform(registry, '''
[shortcode unhandled-parameter="it's value"]
Content.
[/shortcode]
''')
# Result will be:
# > 'Content.'
```

Shortcode handler can also be defined with additional parameters:

```python
@registry.register(
  # Shortcode custom name:
  'name',
  # Does this shortcode can handle multiple entities at a time.
  # `False` by default.
  multiple=False,
  # Should entity's `content` property be parsed and resolved before it
  # passed to this handler.
  # Or you should do something with raw content instead.
  # `True` by default.
  autoresolve_content=True,
)
```

### Multiresolver

Multiresolver is not the same as singular one(duh..).

This configuration was made for performance reasons.

For example if there is, lets say, 10 same shortcuts with different parameters passed inside one text. It's obvious that whose 10 items will do same work for 10 times. So to prevent such unefficiency multihandlers had been added.

```python
@registry.register(multiple=True)
def shortcode(
  # They receive all current entities as `*args`.
  entities: List[Entity],
  context={}
) -> List[str]:
  return [
    # And must return result in the exact same order as they have been passed.
    entity.content for entity in entities
  ]
```

## Django

### Installation

In `settings.py`:

```python
INSTALLED_APPS += [
  'wc_shortcodes.contrib.django',
]
```

### Usage

Specific implementation not yet ready. Can be used as described before.
