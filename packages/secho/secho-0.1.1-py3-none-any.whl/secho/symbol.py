__all__ = (
    'CRITICAL',
    'ERROR',
    'OK',
    'NOTICE',
    'SUCCESS',
    'VERBOSE',
    'WARNING',

    'MINUS',
    'MORE',
    'MULTIPLY',
    'PLUS',
    'WAIT',
)

import click 

from .color import *


"""symbol: '✘', color: RED (bg)"""
CRITICAL = click.style('✘', fg=RED, blink=True, bold=True)

"""symbol: '✘', color: RED"""
ERROR = click.style('✘', fg=RED, bold=True)

"""symbol: '✔', color: GREEN"""
OK = click.style('✔', fg=GREEN, bold=True)

"""symbol: '‼', color: CYAN"""
NOTICE = click.style('‼', fg=CYAN, bold=True)

"""symbol: '◉', color: BLUE"""
SUCCESS = click.style('◉', fg=BLUE, bold=True)

"""symbol: '＋', color: MAGENTA"""
VERBOSE= click.style('＋', fg=MAGENTA, bold=True)

"""symbol: '！', color: YELLOW"""
WARNING = click.style('！', fg=YELLOW, bold=True)


"""letter: '-', color: RED"""
MINUS = click.style('－', fg=RED, bold=True)

"""letter: '>, color: MAGENTA"""
MORE = click.style('>', fg=MAGENTA, bold=True)

"""letter: 'x', color: BLUE"""
MULTIPLY = click.style('×', fg=BLUE, bold=True)

"""letter: '+', color: GREEN"""
PLUS = click.style('+', fg=GREEN, bold=True)

"""symbol: '…', color: YELLOW (blink)"""
WAIT = click.style('…', fg=YELLOW, blink=True, bold=True)



