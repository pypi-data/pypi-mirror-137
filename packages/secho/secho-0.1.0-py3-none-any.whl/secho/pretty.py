__all__ = (
    'ins',
    'rinspect',
    'console',
    'cp'
)

# IPYTHONDIR
# $HOME/.ipython
# ~/.ipython/profile_default/startup
from functools import partial

import rich.pretty
import rich.console
import rich

ins = partial(rich.inspect, docs=False, methods=True, private=True)
rinspect  = rich.inspect
console = rich.console.Console(color_system='256')
cp = console.print
rich.pretty.install(console=console, expand_all=True)

if hasattr(__builtins__, '__IPYTHON__'):
    pass
