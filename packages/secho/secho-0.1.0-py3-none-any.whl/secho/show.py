"""Show symbol in color and message in normal (print)"""

__all__ = (
    'critical',
    'error',
    'ok',
    'notice',
    'success',
    'verbose',
    'warning',

    'minus',
    'more',
    'multiply',
    'plus',
    'wait',
)

from typing import Any
from typing import IO
from typing import Optional


import click

from .color import *
from .symbol import *


_italic = lambda z: click.style(z, italic=True, bold=False)
_style = lambda sep, color: click.style(sep, fg=WHITE, bold=False)
_after = lambda y, z, sep, color: f'{y}{f"{_style(sep, color)} {_italic(z)}" if z else ""}'
_join = lambda x, y, z, sep, color: f'{x}{f" {_after(y, z, sep, color)}" if y else ""}'

def critical(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '✘', color: RED (bg), with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(CRITICAL, message, after, sep, RED), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def error(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '✘', color: RED, with message in normal.
 
    If after is specified will be appended to message with separator.
   
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(ERROR, message, after, sep, RED), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def ok(message: Any = None, 
              after: Any = None,
             sep: str = ':',
            code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '✔', color: GREEN, with message in normal.
 
    If after is specified will be appended to message with separator.
   
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(OK, message, after, sep, GREEN), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def notice(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '‼', color: CYAN, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(NOTICE, message, after, sep, CYAN), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def success(message: Any = None, 
              after: Any = None,
             sep: str = ':',
            code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '◉', color: BLUE, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
       after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
     code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(SUCCESS, message, after, sep, BLUE), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def verbose(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '＋', color: MAGENTA, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(VERBOSE, message, after, sep, MAGENTA), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def warning(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '！', color: YELLOW, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(WARNING, message, after, sep, YELLOW), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def minus(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '－', color: RED, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(MINUS, message, after, sep, RED), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def more(message: Any = None, 
              after: Any = None,
             sep: str = ':',
            code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: letter: '>, color: MAGENTA, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(MORE, message, after, sep, MAGENTA), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def multiply(message: Any = None, 
              after: Any = None,
             sep: str = ':',
            code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '×', color: BLUE, with message in normal.
   
    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(MULTIPLY, message, after, sep, BLUE), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def plus(message: Any = None, 
              after: Any = None,
             sep: str = ':',
            code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: letter: '+', color: GREEN, with message in normal.

    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
       after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
     code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(PLUS, message, after, sep, RED), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        
def wait(message: Any = None, 
             after: Any = None,
             sep: str = ':',
             code: Optional[int] = None, 
             err: bool = True, 
             file: Optional[IO] = None, 
             nl: bool = True) -> None:
    """
    Print: symbol: '…', color: YELLOW (blink), with message in normal.
    
    If after is specified will be appended to message with separator.
    
    To disable color use 'PRETTY' env var.
    
    Arguments:
      message: to append to symbol (default: '')
      after: will be in italic with separator (defaul: None)
      sep: separator between message and after (defaul: ':')
      code: exit code, will exit if not None (default: None)
      err: print to stderr (default: True)
      file: file to write output (default: None)
      nl: output new line (default: False)
    """
    click.echo(_join(WAIT, message, after, sep, YELLOW), err=err, file=file, nl=nl, color=PRETTY)
    if code is not None:
        raise typer.Exit(code)
        

