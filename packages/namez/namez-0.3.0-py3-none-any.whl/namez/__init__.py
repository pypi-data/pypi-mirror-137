# read version from installed package
from importlib.metadata import version
__version__ = version("namez")

from namez import namez as lib

get = lib.get_obj_by_name
set = lib.set_obj_by_name
fqn = name = lib.get_obj_name
module = lib.get_module_from_obj_name
