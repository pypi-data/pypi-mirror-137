
import typing as t

from nr.util.generic import T


class Consumer(t.Protocol[T]):

  def __call__(self, value: T) -> t.Any:
    ...
