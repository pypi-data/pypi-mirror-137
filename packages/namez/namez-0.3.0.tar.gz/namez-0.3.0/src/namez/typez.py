from __future__ import annotations
from typing import Type, TypeVar, Union, Tuple, Sized, Mapping, Sequence
import typing
import enum
import sys
import re
import inspect

GenericAlias: Type = typing._GenericAlias
if sys.version_info < (3, 9):
  GenericParameterized = GenericAlias
else:
  GenericParameterized: Type = type(dict[int, int])

_T = TypeVar("_T")

def verify_length(l: _T, size: int) -> _T:
  n = len(verify_type(l, Sized))
  if n != size:
    raise ValueError(f"Expected length {size}, got {n}")
  return l

def isgenericalias(t: Type) -> bool:
  return isinstance(t, (GenericAlias, GenericParameterized))

def type_origin(t: Type) -> Type:
  return typing.get_origin(t) or t

def type_args(t: Type) -> Tuple[Type, ...]:
  return typing.get_args(t)

def verify_type(x: _T, t: Type) -> _T:
  t_type = type_origin(t)
  t_args = type_args(t)
  if t_type is Union:
    for t_arg in t_args:
      t_arg_origin = type_origin(t_arg)
      if isinstance(x, t_arg_origin):
        return verify_type(x, t_arg)
    # if isinstance(x, tuple([type_origin(v) for v in t_args])):
    #     return x
  elif isgenericalias(t) and issubclass(t_type, Mapping):
    x: Mapping = verify_type(x, t_type)
    if t_args:
      k_T, v_T = verify_length(t_args, 2)
      verify_type(list(x.keys()), Sequence[k_T])
      verify_type(list(x.values()), Sequence[v_T])
    return x
  elif isgenericalias(t) and issubclass(t_type, Sequence):
    verify_type(x, t_type)
    if hasattr(t, '__args__'):
      if t_type is tuple:
        verify_length(x, len(t_args))
        for i, (v, t) in enumerate(zip(x, t_args)):
          verify_type(v, t)
      else:
        v_T = verify_length(t_args, 1)[0]
        for i, v in enumerate(x):
          verify_type(v, v_T)
    return x
  # elif len(t_args) <= 0:
  #     if isinstance(x, t_type):
  #         return x
  elif inspect.isclass(t) and issubclass(t, enum.Enum):
    t: enum.EnumMeta
    enum_values = [getattr(x, 'value', x) for x in t.__members__.values()]
    if getattr(x, 'value', x) in enum_values:
      return x
  else:
    if isinstance(x, t_type):
      return x
  msg = f"Type mismatch; expected {t!r}, was {type(x)!r} for input value {x!r}"
  raise TypeError(re.sub("""<class ['"](.*?)['"]>""", r"\1", msg))
