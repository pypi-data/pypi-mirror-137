"""Add style"""
__all__ = (
    'black',
    'blue',
    'cyan',
    'green',
    'magenta',
    'red',
    'white',
    'yellow',
)

from typing import Any
from typing import Optional
from typing import Union

import click

from .color import *

def black(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=BLACK"""
    return click.style(text,
    fg=BLACK, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def blue(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=BLUE"""
    return click.style(text,
    fg=BLUE, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def cyan(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=CYAN"""
    return click.style(text,
    fg=CYAN, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def green(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=GREEN"""
    return click.style(text,
    fg=GREEN, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def magenta(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=MAGENTA"""
    return click.style(text,
    fg=MAGENTA, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def red(text: Any,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=RED"""
    return click.style(text,
    fg=RED, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def white(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=WHITE"""
    return click.style(text,
    fg=WHITE, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

def yellow(text: Any, 
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> str: 
    """Format with fg=YELLOW"""
    return click.style(text,
    fg=YELLOW, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)

