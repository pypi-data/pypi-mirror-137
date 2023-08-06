import dataclasses
import typing

from dataclasses_jsonschema import JsonSchemaMixin
from django.core.paginator import Paginator


def iterable_factory(item_cls, paginate=False):
    """A factory for processing iterable results.

    Generates a dynamic dataclass wrapper that can facilitate
    returning iterable results of items and paginated results.
    """

    class Wrapper:
        items: typing.List[item_cls]
        page: int = dataclasses.field(init=False)
        count: int = dataclasses.field(init=False)

        page_num: dataclasses.InitVar[int] = 1
        page_size: dataclasses.InitVar[int] = 10

        def __post_init__(self, page_num, page_size):
            if paginate:
                paginator = Paginator(self.items, page_size)
                page = paginator.get_page(page_num)
                self.page = page_num
                self.count = paginator.count
                self.items = page.object_list
            else:
                self.page = 1
                self.count = len(self.items)

    new_cls = type(
        f"Iterable[{item_cls.__name__}]",
        (Wrapper, JsonSchemaMixin),
        dict(Wrapper.__dict__),
    )
    new_cls.__doc__ = f"An Iterable of {item_cls.__name__} items."
    return dataclasses.dataclass(new_cls)
