from fa_purity import (
    _iter_factory,
)
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.pure_iter.core import (
    PureIter,
)
from fa_purity.stream.core import (
    _Stream,
    Stream,
)
from typing import (
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


def chain(
    unchained: Stream[PureIter[_T]],
) -> Stream[_T]:
    draft = _Stream(unchained.unsafe_to_iter().map(_iter_factory.chain))
    return Stream(draft)


def squash(stm: Stream[Cmd[_T]]) -> Stream[_T]:
    draft = _Stream(stm.unsafe_to_iter().map(_iter_factory.squash))
    return Stream(draft)


def consume(stm: Stream[Cmd[None]]) -> Cmd[None]:
    return Cmd.from_cmd(
        lambda: _iter_factory.deque(
            iter(unsafe_unwrap(a) for a in unsafe_unwrap(stm.unsafe_to_iter()))
        )
    )


def filter_opt(stm: Stream[Optional[_T]]) -> Stream[_T]:
    draft = _Stream(stm.unsafe_to_iter().map(_iter_factory.filter_none))
    return Stream(draft)


def filter_maybe(stm: Stream[Maybe[_T]]) -> Stream[_T]:
    return filter_opt(stm.map(lambda x: x.value_or(None)))


def until_none(stm: Stream[Optional[_T]]) -> Stream[_T]:
    draft = _Stream(stm.unsafe_to_iter().map(_iter_factory.until_none))
    return Stream(draft)


def until_empty(stm: Stream[Maybe[_T]]) -> Stream[_T]:
    return until_none(stm.map(lambda m: m.value_or(None)))
