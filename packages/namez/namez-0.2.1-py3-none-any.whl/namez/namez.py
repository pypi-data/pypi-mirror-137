from __future__ import annotations
import importlib
import sys
import os
import re
import types
import inspect

import __main__

from typing import Any, List, Tuple

def get_module_from_obj_name(obj_name: str) -> Tuple[types.ModuleType, str]:
  """Searches for the underlying module behind the name to some python object.
  Returns the module and the object name (original name with module part removed)."""
  if obj_name.startswith('/'):
    return __main__, obj_name[1:]
  if '.' in obj_name and '/' not in obj_name:
    if obj_name.split('.', 1)[0] in __main__.__dict__:
      return __main__, obj_name

  if '/' in obj_name:
    obj_name, local_name = obj_name.rsplit('/', 1)
    module, local_obj_name = get_module_from_obj_name(obj_name)
    return module, os.path.join(local_obj_name, local_name)

  # allow convenience shorthands, substitute them by full names
  obj_name = re.sub("^np\\b", "numpy", obj_name)
  obj_name = re.sub("^jnp\\b", "jax.numpy", obj_name)
  obj_name = re.sub("^tf\\b", "tensorflow", obj_name)
  obj_name = re.sub("^py\\b", "builtins", obj_name)

  # list alternatives for (module_name, local_obj_name)
  parts = obj_name.split(".")
  name_pairs = [(".".join(parts[:i]), ".".join(parts[i:])) for i in range(len(parts), 0, -1)]

  # try each alternative in turn
  for module_name, local_obj_name in name_pairs:
    try:
      module = importlib.import_module(module_name)  # may raise ImportError
      get_obj_from_module(module, local_obj_name)  # may raise AttributeError
      return module, local_obj_name
    except:
      pass

  # maybe some of the modules themselves contain errors?
  for module_name, _local_obj_name in name_pairs:
    try:
      importlib.import_module(module_name)  # may raise ImportError
    except ImportError:
      if not str(sys.exc_info()[1]).startswith("No module named '" + module_name + "'"):
        raise

  if '.' not in obj_name and '/' not in obj_name:
    return __main__, obj_name

  # maybe the requested attribute is missing?
  for module_name, local_obj_name in name_pairs:
    try:
      module = importlib.import_module(module_name)  # may raise ImportError
      get_obj_from_module(module, local_obj_name)  # may raise AttributeError
    except ImportError:
      pass

  # we are out of luck, but we have no idea why
  raise ImportError(obj_name)


def get_obj_from_module(module: types.ModuleType, obj_name: str) -> Any:
  """Traverses the object name and returns the last (rightmost) python object."""
  if obj_name == '':
    return module
  obj = module
  for part in obj_name.replace('/', '.').split("."):
    obj = getattr(obj, part)
  return obj

def set_obj_from_module(module: types.ModuleType, obj_name: str, value: Any) -> Any:
  """Traverses the object name and returns the last (rightmost) python object."""
  if obj_name == '':
    return module
  obj = module
  parts = obj_name.replace('/', '.').split(".")
  last = parts.pop()
  for part in parts:
    obj = getattr(obj, part)
  return setattr(obj, last, value)

def get_obj_by_name(name: str) -> Any:
  """Finds the python object with the given name."""
  module, obj_name = get_module_from_obj_name(name)
  return get_obj_from_module(module, obj_name)

def set_obj_by_name(name: str, value: Any) -> Any:
  """Finds the python object with the given name."""
  module, obj_name = get_module_from_obj_name(name)
  return set_obj_from_module(module, obj_name, value)

class CyclicIndirection(Exception):
  pass

def get_indirect(name):
  tortoise = hare = name
  while True:
    if not isinstance(hare, str):
      break
    hare = get_obj_by_name(hare)
    if not isinstance(hare, str):
      break
    hare = get_obj_by_name(hare)
    tortoise = get_obj_by_name(tortoise)
    if hare == tortoise:
      raise CyclicIndirection()
  return hare


def get_obj_name(obj: Any) -> str:
  """Return the fully-qualified name of the object."""
  # if isinstance(obj, str):
  #   obj = get_indirect(obj)
  if inspect.ismodule(obj):
    return obj.__name__
  mod = inspect.getmodule(obj)
  if mod is None:
    raise ValueError("Couldn't get module for {!r}".format(obj))
  if not hasattr(obj, '__qualname__'):
    obj = type(obj)
  if not hasattr(obj, '__qualname__'):
    raise ValueError("Couldn't get qualified name for {!r} in module {!r}".format(obj, mod.__name__))
  return os.path.join(mod.__name__, obj.__qualname__)


def find_objs(name: str, ignore_case: str = 'smart') -> List[Tuple[str, Any]]:
  name = re.compile(name)
  if ignore_case == 'smart':
    ignore_case = not re.search('[A-Z]', name.pattern)
  if ignore_case:
    name = re.compile(name.pattern, flags=name.flags | re.IGNORECASE)
  h = []
  for modname, module in sys.modules.items():
    for k, v in module.__dict__.items():
      if re.match(name, k) and re.match(name, getattr(v, '__name__', '')):
        fqn = get_obj_name(v)
        h.append((fqn, v))
  return h
