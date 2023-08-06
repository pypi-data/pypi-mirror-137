from ctypes import Union
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Type

if TYPE_CHECKING:
    from .parser import Entity


__all__ = 'CodeDefinition', 'CodesRegistry',


@dataclass
class CodeDefinition:
    name: str
    resolver: Callable
    # Union[
    #     Callable[['Entity', Optional[Dict]], str],
    #     Callable[[List['Entity'], Optional[Dict]], List[str]]
    # ]
    multiple: bool = False
    autoresolve_content: bool = True


class CodesRegistry:
    Definition: Type[CodeDefinition] = CodeDefinition
    definitions: Dict[str, CodeDefinition]

    def __init__(self):
        self.definitions = {}

    def has(self, name: str) -> bool:
        return name in self.definitions

    def add(
        self,
        name: str,
        resolver: Callable,
        /,
        multiple: bool = False,
        autoresolve_content: bool = True
    ) -> CodeDefinition:
        if self.has(name):
            # TODO: Add own library exceptions.
            raise KeyError(
                f'Code resolver for "{name}" already registered.\n'
                'Remove it and only then add a new one.'
            )

        definition = self.Definition(
            name=name, resolver=resolver,
            multiple=multiple, autoresolve_content=autoresolve_content
        )
        self.definitions[name] = definition

        return definition

    def remove(self, name: str) -> None:
        self.definitions.pop(name)

    def get(self, name: str) -> CodeDefinition:
        return self.definitions[name]

    def register(
        self,
        name: Optional[str] = None,
        /,
        multiple: bool = False,
        autoresolve_content: bool = True
    ):
        def wrapper(func):
            self.add(
                name or func.__name__, func,
                multiple=multiple, autoresolve_content=autoresolve_content
            )

            return func

        return wrapper
