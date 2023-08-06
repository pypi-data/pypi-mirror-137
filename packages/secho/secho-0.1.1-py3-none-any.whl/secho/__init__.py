import pathlib

import hasis

from .color import *
from . import color as color

from .helado import *
from . import helado as helado

from .out import *
from . import out as out

from .pretty import *
from . import pretty as pretty

from .show import *
from . import show as show

from .style import *
from . import style as style

from .symbol import *
from . import symbol as symbol

__all__ = \
    color.__all__ + ('color', ) \
    + helado.__all__ + ('helado', ) \
    + out.__all__ + ('out', ) \
    + pretty.__all__ + ('pretty', ) \
    + show.__all__ + ('show', ) \
    + style.__all__ + ('style', ) \
    + symbol.__all__ + ('symbol', )

app = lambda: print(hasis.version(pathlib.Path(__file__).parent.name))

