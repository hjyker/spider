#!/usr/bin/env python
#-*- coding:gbk -*-

import sys
import getopt
import logContral
import testdoc


class DetectOpts(object):
    def __init__(self):
        # 合法参数字典,返回给WebSpiderMan使用
        self.optionsDict = dict()
        self.logger = logContral.LogContral(50)

        #以下为帮助提示
        self.minHelp = 'spider.py [-u | -d | -l | --key | --thread | --dbfile | --testself | --help]\n'
        self.maxHelp = """
 -u           指定爬虫开始地址
 -d           指定爬虫深度
 -l           日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log
 --key        页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面
 --thread     指定线程池大小，多线程爬取页面，可选参数，默认10
 --dbfile     存放结果数据到指定的数据库(sqlite)文件中
 --testself   程序自测，可选参数
 --help       详细帮助\n
"""
     # 测试命令长度是否合法
    def optionsLen(self, options):
        if not len(options):
            raise getopt.GetoptError('Invalid parameter')

    # 测试有无多余参数
    def errorArgsLen(self, errorArgsList):
        if len(errorArgsList):
            raise getopt.GetoptError('Invalid parameter')

    # 拆分命令参数，存到optionsDict
    def splitOptions(self, options):
        try:
            optionList, errorArgsList = getopt.getopt(
                options,
                'u:d:l:',
                ['key=', 'thread=', 'dbfile=', 'testself', 'help'])
            self.errorArgsLen(errorArgsList)

        except (getopt.GetoptError):
            self.logger.logInfo('Param without a value')
            raise getopt.GetoptError('%s \nPlease use options --help' % self.minHelp)
            #sys.exit(self.minHelp)

        for key, value in optionList:
            self.optionsDict[key] = value

    # 检测命令参数是否合法
    def optionsTest(self, options):
        self.splitOptions(options)
        try:

            if '--help' in self.optionsDict:
                sys.exit(self.maxHelp)
            if '--testself' in self.optionsDict:
                #testdoc.testself()
                sys.exit('Testing Completed...')
            self.isMustVar() # detect necessary values '-u, -d, --dbfile'

            if '-l' not in self.optionsDict:
                self.optionsDict['-l'] = 3
            if '--key' not in self.optionsDict:
                self.optionsDict['--key'] = None
            if '--thread' not in self.optionsDict:
                self.optionsDict['--thread'] = 20

        except (OptionsError), e:
            self.logger.logInfo(e)
            raise getopt.GetoptError('%s. \nPlease use options --help' % e)
            # sys.exit('%s. \nPlease use options --help' % e)

        return self.optionsDict

    # Check whether necessary options
    def isMustVar(self):
        #print self.optionsDict
        if '-u' not in self.optionsDict:
            raise OptionsError("[-] '-u not exsit' : -u, -d, --dbfile are Necessary Option")

        if '-d' not in self.optionsDict:
            raise OptionsError("[-] '-d not exsit' : -u, -d, --dbfile are Necessary Option")

        if '--dbfile' not in self.optionsDict:
            raise OptionsError("[-] '--dbfile not exsit' : -u, -d, --dbfile are Necessary Option")

# Custom exceptions, for class DetectOpts ---> def isMustVar
class OptionsError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg

def test():
    '''
        >>> test = DetectOpts()

        >>> options = sys.argv[1:]

        >>> test.optionsTest(options)
        >>> print test.optionsDict
    '''
if __name__ == '__main__': pass
    #test()