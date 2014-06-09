#!/usr/bin/env python
#-*- coding:gbk -*-

import sys
import getopt
import logContral
import testdoc


class DetectOpts(object):
    def __init__(self):
        # �Ϸ������ֵ�,���ظ�WebSpiderManʹ��
        self.optionsDict = dict()
        self.logger = logContral.LogContral(50)

        #����Ϊ������ʾ
        self.minHelp = 'spider.py [-u | -d | -l | --key | --thread | --dbfile | --testself | --help]\n'
        self.maxHelp = """
 -u           ָ�����濪ʼ��ַ
 -d           ָ���������
 -l           ��־��¼�ļ���¼��ϸ�̶ȣ�����Խ���¼Խ��ϸ����ѡ������Ĭ��spider.log
 --key        ҳ���ڵĹؼ��ʣ���ȡ����ùؼ��ʵ���ҳ����ѡ������Ĭ��Ϊ����ҳ��
 --thread     ָ���̳߳ش�С�����߳���ȡҳ�棬��ѡ������Ĭ��10
 --dbfile     ��Ž�����ݵ�ָ�������ݿ�(sqlite)�ļ���
 --testself   �����Բ⣬��ѡ����
 --help       ��ϸ����\n
"""
     # ����������Ƿ�Ϸ�
    def optionsLen(self, options):
        if not len(options):
            raise getopt.GetoptError('Invalid parameter')

    # �������޶������
    def errorArgsLen(self, errorArgsList):
        if len(errorArgsList):
            raise getopt.GetoptError('Invalid parameter')

    # �������������浽optionsDict
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

    # �����������Ƿ�Ϸ�
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