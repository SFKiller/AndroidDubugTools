#!/usr/bin/python
"""
    This is a python script for automatic generating trace info android .so library
    debug.
    @author SFKiller
    @usage: python addr2line.py logfile
"""

import os
import sys
import string

#Android project root path
ANDROID_PROJECT_ROOT_DIR = os.getcwd() + '/'
#Android target product out dir of your project
ANDROID_PRODUCT_NAME = 'generic'        #your should change 'generic' to be your actural product name, like 'qcom'.
#symbol root dir
symbol_root_dir = ANDROID_PROJECT_ROOT_DIR + 'out/target/product/' + ANDROID_PRODUCT_NAME + '/symbols'
#addr2line tool
addr2line_tool ='/usr/bin/addr2line'    #This need you execute the script 'build/envsetup.sh'

class CheckLogFile:
    def __init__(self, log_file):
        self.log = log_file
    def get_trace_line(self):
        f = file(self.log, 'r')
        lines = f.readlines()
        if [] == lines:
            print 'Log file is empty, please set the right log file.'
            sys.exit(0)
        else:
            trace = []
            for line in lines:
                if (-1 != line.find('DEBUG')) and (-1 != line.find('pc')) and (-1 != line.find('system')):
                    trace.append(line)
        if [] == trace:
            print 'Can not find trace log in the file, please make sure your have set the right log file.'
            sys.exit(0)
        else:
            return trace

class Addr2Line:
    def __init__(self, trace_line):
        self.lines = trace_line
    def addr_to_line(self, single_line):
        linesplit = single_line.split()
"""
    For my Android project, the crash log is in the form:

[0]  |  [1]        | [2] | [3] | [4]| [5] | [6]  | [7]|[8]|[9]    |    [10]

11-02 09:46:40.654   148   148   I   DEBUG   :     #05 pc 00018a63  /system/lib/libsurfaceflinger.so
11-02 09:46:40.654   148   148   I   DEBUG   :     #06 pc 000187d1  /system/lib/libsurfaceflinger.so

    So the pc address is the [9] and file is [10]. Therefore, I use linesplit[10] and linesplit[9].
    You should change it to suit your log format.
"""
        result = addr2line_tool + " -f -e " + symbol_root_dir + linesplit[10] + " " + linesplit[9]
        stream = os.popen(result)
        result_line = stream.readlines()
        result_lines = map(string.strip, result_line)
        return result_lines
    def dump_all_lines(self):
        result = []
        for line in self.lines:
            cmd = self.addr_to_line(line)
            result.append(cmd)
        return result
def PrintResult(lines):
    i = 0
    for line in lines:
        print "#%-6d%-30s" % (i, line[0])
        print "%s" % (line[1])
        i += 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python ' + sys.argv[0] + ' logfile'
        sys.exit(0)
    logfile = sys.argv[1]
    checklog = CheckLogFile(logfile)
    traceline = checklog.get_trace_line()

    add2line = Addr2Line(traceline)
    resultline = add2line.dump_all_lines()

    PrintResult(resultline)
