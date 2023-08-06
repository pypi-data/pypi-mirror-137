# @Time     : 2022/2/8
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Callable, Union

from ._timeunt import MILLISECOND, MICROSECOND

FloatOrInt = Union[float, int]

ConvertFn = Callable[[FloatOrInt], FloatOrInt]


def convert(timestamp: FloatOrInt, fn: ConvertFn = None):
    return fn(timestamp) if fn else timestamp


def second(timestamp: FloatOrInt) -> FloatOrInt:
    return convert(timestamp)


def millisecond(timestamp: FloatOrInt) -> FloatOrInt:
    return convert(timestamp, lambda t: t * MILLISECOND)


def microsecond(timestamp: FloatOrInt) -> FloatOrInt:
    return convert(timestamp, lambda t: t * MICROSECOND)
