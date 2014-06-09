#!/usr/bin/env python

# -*- coding:utf-8 -*-

import doctest
import storeDB, logContral, detectOpts

#if __name__ == '__main__': pass

def testself():
    doctest.testmod(detectOpts, verbose=True)
    print
    doctest.testmod(logContral, verbose=True)
    print
    doctest.testmod(storeDB, verbose=True)
    #t.logInfo( )
