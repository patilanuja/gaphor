"""Grouping functionality allows nesting of one item within another item
(parent item). This is useful in several use cases.

- artifact deployed within a node
- a class within a package, or a component
- composite structures (i.e. component within a node)
"""

from __future__ import annotations

import functools
import itertools
from typing import Callable

from generic.multidispatch import FunctionDispatcher, multidispatch

from gaphor.core.modeling import Diagram, Element


def no_group(parent, element) -> bool:
    return False


group: FunctionDispatcher[Callable[[Element, Element], bool]] = multidispatch(
    object, object
)(no_group)


@functools.lru_cache()
def can_group(parent: Element, element_or_type: Element | type[Element]) -> bool:
    element_type = (
        type(element_or_type)
        if isinstance(element_or_type, Element)
        else element_or_type
    )
    parent_type = type(parent)
    get_registration = group.registry.get_registration
    for t1, t2 in itertools.product(parent_type.__mro__, element_type.__mro__):
        if r := get_registration(t1, t2):
            return r is not no_group
    return False


@multidispatch(object, object)
def ungroup(parent, element) -> bool:
    return False


@group.register(Element, Diagram)
def diagram_group(element, diagram):
    diagram.element = element
    return True


@ungroup.register(Element, Diagram)
def diagram_ungroup(element, diagram):
    del diagram.element
    return True
