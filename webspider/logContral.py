#!/usr/bin/env python

# -*- coding:gbk -*-

import logging

class LogContral():
    def __init__(self, level):
        if not level:
            level = 30
        else:
            level = 60 - level
        #print '$'*80, level
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        outFormate = '%(levelname)s - %(pathname)s - %(funcName)s - %(asctime)s \n' \
                     '  +----+ %(message)s\n'
        self.formatter = logging.Formatter(outFormate)

        self.initFileHandler(level)
        self.initStreamHandler(level)

    def initFileHandler(self, level=30):
        fh = logging.FileHandler(r'logSpider.txt')
        fh.setLevel(level)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

    def initStreamHandler(self, level=10):
        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)

    def logInfo(self, l_info):
        self.logger.info(l_info)
def testdoc():
    '''
        >>> t = LogContral(50)
        >>> t.logInfo('test')
    '''

if __name__ == '__main__': pass