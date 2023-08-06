from fa_purity import (
    _iter_factory,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.pure_iter.core import (
    PureIter,
)
from fa_purity.stream.core import (
    _Stream,
    Stream,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def from_piter(piter: PureIter[Cmd[_T]]) -> Stream[_T]:
    draft = _Stream(Cmd.from_cmd(lambda: _iter_factory.squash(piter)))
    return Stream(draft)
