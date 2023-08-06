"""Prints the complete message in color (print)"""

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
from typing import IO
from typing import Optional
from typing import Union

import click
import typer

from .color import *

def black(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=BLACK
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)    
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=BLACK, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def blue(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=BLUE
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)    
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=BLUE, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def cyan(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=CYAN
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)        
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=CYAN, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def green(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=GREEN
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)    
    
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=GREEN, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def magenta(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=MAGENTA
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)        
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=MAGENTA, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def red(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=RED
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)        
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=RED, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def white(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=WHITE
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)        
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=WHITE, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

def yellow(message: Any = None, 
         code: Optional[int] = None, 
         err: bool = True, 
         file: Optional[IO] = None, 
         nl: bool = True,
          bg: Union[str, int, tuple[int, int, int]] = None, 
          bold: Optional[bool] = None, 
          dim: Optional[bool] = None, 
          underline: Optional[bool] = None,
          overline: Optional[bool] = None, 
          italic: Optional[bool] = None, 
          blink: Optional[bool] = None, 
          reverse: Optional[bool] = None, 
          strikethrough: Optional[bool] = None, 
          reset: bool = True) -> None: 
    """
    Print with fg=YELLOW
    
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)    
    """
    click.secho(message, err=err, file=file, nl=nl, color=PRETTY,
    fg=YELLOW, bg=bg, bold=bold, dim=dim, underline=underline,
                      overline=overline, italic=italic, blink=blink, reverse=reverse, 
                      strikethrough=strikethrough, reset=reset)
    if code is not None:
        raise typer.Exit(code)

