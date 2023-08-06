__all__ = (
    'PRETTY',
    'BLACK',
    'BLUE',
    'CYAN',
    'GREEN',
    'MAGENTA',
    'RED',
    'WHITE',
    'YELLOW',
)

import os

"""None for click to use colors based on tty, False to force no colors"""
PRETTY = False if os.getenv('NO_PRETTY') else os.getenv('PRETTY')

BLACK: str = 'black'
BLUE: str = 'blue'
CYAN: str = 'cyan'
GREEN: str = 'green' 
MAGENTA: str = 'magenta' 
RED: str = 'red' 
WHITE: str = 'white' 
YELLOW: str = 'yellow' 

