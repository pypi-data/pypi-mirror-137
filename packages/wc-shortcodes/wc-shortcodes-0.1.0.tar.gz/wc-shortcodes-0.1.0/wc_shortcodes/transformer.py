from typing import (
    TYPE_CHECKING, Any, Callable, Deque, Dict, Iterable, List, Optional, Set,
    Tuple, Type, Generator,
)
import re
from collections import deque

from . import parser


if TYPE_CHECKING:
    from .registry import CodesRegistry


__all__ = 'SolvedEntity', 'ResolveState', 'resolve', 'solve_content', 'transform',

SolvedEntity = Tuple[parser.Entity, str]
QueueEntity = Tuple[parser.Entity, Optional[int]]
UnresolvedEntity = Tuple[int, parser.Entity, List[SolvedEntity]]


def solve_content(content: str, solved_entities: List[SolvedEntity]) -> str:
    start = 0
    parts = []

    for entity, part in sorted(solved_entities, key=lambda x: x[0].start):
        parts.append(content[start:entity.start])
        parts.append(part)
        start = entity.end

    parts.append(content[start:])

    return ''.join(parts)


def find_entities(registry: 'CodesRegistry', content: str) -> List[parser.Entity]:
    # TODO: Make api method to get names in registry:
    matches = '|'.join(re.escape(x) for x in registry.definitions.keys())

    return parser.find_entities(content, name_regex=f'({matches})')


class ResolveState:
    def __init__(
        self,
        entities: List[parser.Entity],
    ):
        self.entities: List[parser.Entity] = entities
        self.queue: Deque[QueueEntity] = deque([
            (x, None) for x in entities
        ])
        self.indexes: List[parser.Entity] = []
        self.dependencies: Dict[Optional[int], Set[int]] = {}
        self.name_to_index: Dict[str, Set[int]] = {}
        self.i: int = -1
        self.resolveds: Dict[int, str] = {}

    def q_pop(self) -> QueueEntity:
        return self.queue.popleft()

    def q_append(self, item: parser.Entity, parent: Optional[int] = None):
        self.queue.append((item, parent))

    def q_filled(self) -> bool:
        return bool(self.queue)

    def add(self, entity: parser.Entity, parent: Optional[int]):
        self.i += 1
        self.indexes.append(entity)
        # Registering item dependency:
        self.dependencies[parent] = self.dependencies.get(parent) or set()
        self.dependencies[parent].add(self.i)

        # Grouping items:
        self.name_to_index[entity.name] = (
            self.name_to_index.get(entity.name) or set()
        )
        self.name_to_index[entity.name].add(self.i)

    @property
    def is_resolved(self):
        return len(self.indexes) == len(self.resolveds)

    def unresolved_groups(self, key=lambda x: x) -> Generator[
        Tuple[str, List[UnresolvedEntity]], None, None
    ]:
        ordered = sorted(self.name_to_index, key=key)

        for key in ordered:
            groups: List[UnresolvedEntity] = []

            for i in self.name_to_index[key]:
                if i in self.resolveds:
                    continue

                dependencies: List[SolvedEntity] = []
                broken = False

                for j in self.dependencies.get(i, ()):
                    if j not in self.resolveds:
                        broken = True
                        break

                    dependencies.append((self.indexes[j], self.resolveds[j]))

                if not broken:
                    groups.append((i, self.indexes[i], dependencies))

            if len(groups):
                yield key, groups

    def resolve(self, index: int, content: str):
        self.resolveds[index] = content

    def get_solved(self, indexes: Iterable[int]) -> List[SolvedEntity]:
        return [(self.indexes[i], self.resolveds[i]) for i in indexes]


def resolve_entity(
    unresolved: UnresolvedEntity,
    content_solver: Callable = solve_content,
) -> parser.Entity:
    # FIXME: This method mutates underlying entity `content` property.
    # It would be better if not, of course.
    _, entity, dependencies = unresolved

    if len(dependencies) == 0:
        return entity

    entity.content = content_solver(entity.content, dependencies)

    return entity


def resolve(
    registry: 'CodesRegistry',
    entities: List[parser.Entity],
    context: Optional[Dict] = None,
    state_class: Type[ResolveState] = ResolveState,
    content_solver: Callable = solve_content,
    entities_parser: Callable = find_entities,
) -> List[SolvedEntity]:
    # 1.1. Gathering pool with resolved dependencies.
    # 1.2. Grouping them by type.
    # 2.1. First place resolve - singular.
    # 2.2. After all singular ready go 1.1, if were no singulars continue.
    # 2.3. Resolving multiples.
    # 3.1. Go 1.1 until no unresolved items left.

    roots = set(range(len(entities)))
    state = state_class(entities)
    context = {} if context is None else {**context}
    context['shortcode_resolver'] = {
        'registry': registry, 'content_solver': content_solver,
        'entities_parser': entities_parser,
    }

    # Collecting all the possible entities to resolve.
    while state.q_filled():
        entity, parent = state.q_pop()
        definition = registry.get(entity.name)

        state.add(entity, parent)

        if definition.autoresolve_content and entity.content:
            for found in entities_parser(registry, entity.content):
                state.q_append(found, parent=state.i)

    # Resolving entities.
    # Grouping them by same resolvers.
    # Those that are not accept multiple items will resolve first.
    # Then multiresolvables will be resolved.
    # This is because non-multiresolvable might be dependencies for
    # multiresolvables.
    while not state.is_resolved:
        unresolved = state.unresolved_groups(
            key=lambda x: registry.get(x).multiple
        )
        multiple = None

        for key, group in unresolved:
            definition = registry.get(key)

            # If there was change, then there singular-resolvables items
            # finished to resolve, so more multiresolvables can be resolved now.
            # TODO: It should be better to recalculate what to resolve next
            # on every tick. But more performant algorithm is harder to
            # figure out.
            # So for now recalculations will happen only on singular/multiple
            # change to use most of out of multiresolver optimizations.
            if multiple is not None and multiple != definition.multiple:
                break

            multiple = definition.multiple
            resolved_items = [
                resolve_entity(u, content_solver=content_solver)
                for u in group
            ]

            if multiple:
                contents = definition.resolver(
                    resolved_items, context=context
                )

                for i, content in enumerate(contents):
                    state.resolve(group[i][0], content)
            else:
                for i, item in enumerate(resolved_items):
                    content = definition.resolver(item, context=context)
                    state.resolve(group[i][0], content)

        # This can't be true. At least in theory.
        if multiple is None:  # pragma: no cover
            raise ValueError(
                'Can\'t proceed.\n'
                'No unresolved groups for unresolved state.\n'
                'There might somehow be a circular dependency inside.\n'
                'Or it\'s algorithm error.'
            )

    return state.get_solved(roots)


def transform(
    registry: 'CodesRegistry',
    content: str,
    context: Optional[Dict] = None,
) -> str:
    entities = find_entities(registry, content)
    solved = resolve(
        registry, entities, context=context,
        content_solver=solve_content, entities_parser=find_entities,
    )

    return solve_content(content, solved)
