#!/usr/bin/env python

#-*- coding:gbk -*-

import urllib2
import threading
from Queue import Queue, Empty
from bs3 import BeautifulSoup
import zlib
import time
import getopt
# import datetime
import sys, os
from socket import timeout
# Add the current file path
if os.getcwd not in sys.path:
    sys.path.append(os.getcwd())

# import ./detectOpts.py
import logContral
import detectOpts
import storeDB

# set default charset
#reload(sys)
#sys.setdefaultencoding('gbk')


threadLook = threading.Lock()
dlLinksNow = Queue()   # download webpage now
dlLinksNext = Queue()  # new links from webpage
threadsPool = list()   # thread pool
totalLinks = 1         # total Links
count = 1   ###########test#############################test , only test#######


class Control():
    def __init__(self):
        global dlLinksNow
        try:
            optionsDict = detectOpts.DetectOpts()
            spiderOpts = sys.argv[1:]
            self.opts = optionsDict.optionsTest(spiderOpts)
        except (getopt.GetoptError), e:
            sys.exit(e)

        self.deep = int(self.opts['-d'])
        self.url1 = self.opts['-u'] # start url
        self.dbfile = self.opts['--dbfile']
        self.thread = int(self.opts['--thread']) # spider number
        if not self.opts['--key']:
            self.keyword = self.opts['--key']
        else:
            self.keyword = self.opts['--key'].decode('gbk').encode('utf-8')

        self.loglevel = int(self.opts['-l']) * 10

        #print self.loglevel
        self.db = storeDB.StoreWebpage(self.dbfile)


        dlLinksNow.put(self.url1)  # init dlLinksNow, it's url entrance
        self.initTimer()           # timer, Print the process info, Every 10 seconds

    def downLoad(self):
        self.initThreadPool()

    def initThreadPool(self, threadNum=10):
        global threadsPool, dlLinksNow
        for i in xrange(threadNum):
            threadsPool.append( SpiderThread(self.db, self.keyword, self.loglevel) )

    def initTimer(self):
        t = Timer()
        t.setDaemon(True)
        t.start()

    def isThreadAlive(self):
        global threadsPool
        for xt in threadsPool: # xt is thread
            if xt.isAlive():
                xt.join()
            else:
                pass   #print '>>>>>>>>>>>>>>>>>>>>>>>>>>',threading.activeCount()-1

    def main(self):
        global dlLinksNow, dlLinksNext, totalLinks
        for dth in xrange(self.deep):
            self.downLoad()
            self.isThreadAlive()

            dlLinksNow = dlLinksNext
            totalLinks += dlLinksNow.qsize()
            dlLinksNext = Queue() # clean dlLinksNext

# class Thread
class SpiderThread(threading.Thread):
    def __init__(self, db, keyword, loglevel):
        threading.Thread.__init__(self)
        self.db = db
        self.keyword = keyword
        self.loger = logContral.LogContral(loglevel)
        self.start()

    # Determine whether to compressed webpages, if yes decompression
    def isCompressWeb(self, webRes):
        header = webRes.info()
        for key in header.keys():
            key = key.lower()
        webpage = webRes.read()

        if ('content-encoding' in header) and (header['content-encoding'] == 'gzip'):
            #print header['content-encoding']
            deWebpage = zlib.decompress(webpage, 16+zlib.MAX_WBITS)
            return deWebpage
        return webpage

    # get new links from wepage
    def geturl(self, webpage, key=None):
        #key = None ##############################test
        global dlLinksNext

        try:
            webpage = unicode(webpage, 'gbk').encode('utf-8')
            soup = BeautifulSoup(webpage)
            tagA = soup.findAll('a')

            for link in tagA:
                if not key:
                    dlLinksNext.put(link.get('href'))
                elif key in str(link):
                    dlLinksNext.put(link.get('href'))

        except (UnicodeDecodeError):
            #error = '132 have code'
            error = 'UnicodeDecodeError'
            self.loger.logInfo(error)
        except (UnicodeEncodeError):
            #error = '135 had code'
            error = 'UnicodeDecodeError'
            self.loger.logInfo(error)

    # capture webpage from dlLinksNow
    def captureWebpage(self, url):
        global dlLinksNext, count, threadLook

        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout=20) #socket timeout is 20sec
            webpage = self.isCompressWeb(res)

        # test ################
            #count += 1       ##
            #print count, url  ##
        # test ################

        except (ValueError,AttributeError), e:
            error = '[-] ', e, url
            self.loger.logInfo(error)
        except (urllib2.HTTPError), e:
            error = '[-] ', e, url
            self.loger.logInfo(error)
        except (urllib2.URLError), e:
            error = '[-] ', e, url
            self.loger.logInfo(error)
        except (timeout), e:
            error = '[-] ', e, url
            self.loger.logInfo(error)
        else:
            # store webpages to webspider.db(sqlit3)
            threadLook.acquire() # Lock
            self.db.store(webpage)
            threadLook.release() # release Lock

            self.geturl(webpage, self.keyword)

    def run(self):
        global dlLinksNow

        while True:
            try:
                url = dlLinksNow.get(block=0)

                self.captureWebpage(url)
            except (Empty):
                error = '[-] Queue(dlLinksNow) had Empty!'
                #self.loger.logInfo(error)
                break

# It's Timer, Print the process info, Every 10 seconds,
class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            global dlLinksNow, totalLinks
            print '+' * 80
            printInfo() # global function printInfo()
            print '+' * 80, '\n'
            time.sleep(3)

# It's global function , print Progress informations
def printInfo():
    global dlLinksNow, totalLinks
    print '+   Surplus: %d  Spiders: %d  Total: %d  Progress: %.2f%%' % \
            (dlLinksNow.qsize(), threading.activeCount()-1, totalLinks, 100.00-(dlLinksNow.qsize()*100.00 / totalLinks))

if __name__ == '__main__':
    try:
        test = Control()
        test.main()
        print '\nGame Over :)'
    except (KeyboardInterrupt):
        logContral.LogContral(30).logInfo('User Interrupt Program!')