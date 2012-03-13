# -*- encoding: utf-8 -*-
import sys

class Logger(object):
    def __init__(self):
        self._real_stderr = sys.stderr
        self._real_stdout = sys.stdout
        self._fp = sys.stdout

    def start(self, file = 'data/debug.log' ):
        self._fp = open( file, 'w', False )
        sys.stderr = self._fp
        sys.stdout = self._fp
        self.log( " === Logger started ===" )

    def __call__(self, *args, **kwargs):
        self.log(*args, **kwargs)

    def log(self,txt):
        self._fp.write( txt + '\n' )

    def stop(self):
        self.log( " === Logger ended ===" )
        sys.stderr = self._real_stderr
        sys.stdout = self._real_stdout
    
    def getLocale(self):
        return self._real_stdout.encoding

LOGGER = Logger()
