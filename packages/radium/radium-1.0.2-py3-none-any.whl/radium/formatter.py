# imports
import logging
from sys import stdout

class Formatter(logging.Formatter):
    '''The Radium formatter.'''
    def __init__(self):
        # map of color IDs
        self.style_list = {
            'bright': '\x1b[1m',
            'dim': '\x1b[2m',
            'red': '\x1b[31m',
            'green': '\x1b[32m',
            'yellow': '\x1b[33m',
            'reset': '\x1b[0m'
        }
        # formats
        self.err_fmt = f"{self.style_list.get('dim')}[{self.style_list.get('reset')}{self.style_list.get('red')}!{self.style_list.get('reset')}{self.style_list.get('dim')}]{self.style_list.get('reset')} (f:'%(module)s', l:%(lineno)s) %(message)s"
        self.crit_fmt = f"{self.style_list.get('dim')}[{self.style_list.get('reset')}{self.style_list.get('red')}!!{self.style_list.get('reset')}{self.style_list.get('dim')}]{self.style_list.get('reset')} (f:'%(module)s', l:%(lineno)s) %(message)s"
        self.dbg_fmt = f"{self.style_list.get('dim')}[{self.style_list.get('reset')}{self.style_list.get('yellow')}#{self.style_list.get('reset')}{self.style_list.get('dim')}]{self.style_list.get('reset')} (f:'%(module)s', l:%(lineno)s) %(message)s"
        self.warn_fmt = f"{self.style_list.get('dim')}[{self.style_list.get('reset')}{self.style_list.get('yellow')}?{self.style_list.get('reset')}{self.style_list.get('dim')}]{self.style_list.get('reset')} (f:'%(module)s', l:%(lineno)s) %(message)s"
        self.info_fmt = f"{self.style_list.get('dim')}[{self.style_list.get('reset')}{self.style_list.get('green')}*{self.style_list.get('reset')}{self.style_list.get('dim')}]{self.style_list.get('reset')} %(message)s"
        # initialize main formatter
        super().__init__(fmt=self.info_fmt, datefmt=None, style='%')

    def format(self, record):
        format_orig = self._style._fmt

        # debug
        if record.levelname == 'DEBUG':
            self._style._fmt = self.dbg_fmt
        # info
        if record.levelname == 'ingo':
            self._style._fmt = self.info_fmt
        # warning
        if record.levelname == 'WARNING':
            self._style._fmt = self.warn_fmt
        # error
        if record.levelname == 'ERROR':
            self._style._fmt = self.err_fmt
        # critical
        if record.levelname == 'CRITICAL':
            self._style._fmt = self.crit_fmt

        # format log
        result = logging.Formatter.format(self, record)
        self._style._fmt = format_orig
        # send it off
        return result

Radium = logging.StreamHandler(stdout)
Radium.formatter = Formatter()