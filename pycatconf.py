#!/usr/bin/env python

"""
 ----------------------------------------------------------------------
 ideal idealities@gmail.com
 Homepage: http://dev.bjtu.edu.cn/ideal
 ----------------------------------------------------------------------
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 ----------------------------------------------------------------------
"""

import os
import sys

info = {
  '-u': '',
  '-p': '',
  '-ip': '202.113.18.188',
  '-r': '1',
  '-a': '0'
}

#Print the help information.
def usage():
    print '''Useage: pycatconf [options]
Options:
    -u <user name>\tUser name, like 052812**
    -p <password>\tPassword
    -ip <server IP>\tServer IP address, 202.113.18.180 for domitory
    -r <remeber passwd>\t0:no, 1:yes, default: 1
    -a <auto login>\t0:no, 1:yes, default: 0
    --help \t\tPrint this message
    --show \t\tPrint account string

Examples:
    pycatconf
    pycatconf -u 052812** -p ******
  
Config file is saved in ~/.pycat/account, use "less ~/.pycat/account"
to view your account setting.

By ideal (idealities@gmail.com)
Homepage: http://dev.bjtu.edu.cn/ideal
'''
    sys.exit(0)
    
#Get user information from account file.
def show():
    #Get the path to account file, location different for POSIX and Windows.
    if sys.platform == 'win32':
        homedir = os.getenv('HOMEDRIVE')
        homedir += os.getenv('HOMEPATH')
    else:
        homedir = os.getenv('HOME')
    filename = os.path.join(homedir, '.pycat', 'account')
    #Open and read account information from account file.
    if not os.path.isfile(filename):
        return False
    else:
        pycatfile = open(filename, 'r')
        line = pycatfile.readline()
        pycatfile.close()
        if line == '':
            return False
        return line
        
#Parse arguments from the command line.
def parse_args(argv):
    i = 1
    while i < len(argv):
        if argv[i].startswith('--'):
            option = argv[i]
            i = i + 1
            if option == '--help':
                usage()
            elif option == '--show':
                #print show()
                #added by ideal
                #test if the config file exists
                if show() == False:
                    print 'You have no saved information. Please reconfigure :)'
                else:
                    print show()
                sys.exit(0)
            else:
                print >>sys.stderr, "Unrecognized option \"%s\", ignored!" % option
                continue
        if argv[i].startswith('-'):
            option = argv[i]
            i = i + 1
            #Put the options start with one '-' into infomation dictionary.
            if option in info:
                info[option] = argv[i]
                i = i + 1
            else:
                print >>sys.stderr, "Unrecognized option \"%s\", ignored!" % option
        else:
            print >>sys.stderr, "Poor option value \"%s\", ignored!" % argv[i]
            i = i + 1
    return True
    
#Put str into options dictionary.
def input_arg(str, option):
    s = raw_input("%s: " % str)
    if s != '':
        info[option] = s
    return True
    
#Write account information in information dictionary to account file.
def write_info():
    #Get the path to account file, location different for POSIX and Windows.
    if sys.platform == 'win32':
        homedir = os.getenv('HOMEDRIVE')
        homedir += os.getenv('HOMEPATH')
    else:
        homedir = os.getenv('HOME')
    pycatdir = os.path.join(homedir, '.pycat')
    filename = os.path.join(pycatdir, 'account')
    #If application directory does not exist, create it.
    if not os.path.isdir(pycatdir):
        os.mkdir(pycatdir)
        os.chmod(pycatdir, 0700)
    #If account file does not exist, create one.
    if not os.path.isfile(filename):
        pycatfile = open(filename, 'w+')
        os.chmod(filename, 0600)
    else:
        pycatfile = open(filename, 'w+')
    #Format options directory to account string, write it to account file.
    if info['-r'] == '0':
        line = info['-u'] + '::'
    else:
        line = info['-u'] + ':' + info['-p'] + ':'
    line = line + info['-ip'] + ':'
    line = line + info['-r'] + ':'+ info['-a']
    pycatfile.write(line)
    pycatfile.close()
    return True
    
#Main function.
def main(argv=sys.argv, verbose=True):
    #Get user input, interactively or non-interactively.
    if len(argv) > 1:
        parse_args(argv)
        while info['-u'] == '':
            input_arg('user name', '-u')
        while info['-p'] == '':
            input_arg('password', '-p')
    else:
        input_arg('server ip(default %s for domitory, 202.113.18.180 for other)' % info['-ip'], '-ip')
        while info['-u'] == '':
            input_arg('user name', '-u')

        while info['-p'] == '':
            input_arg('password', '-p')
        input_arg('remember password(0:no, 1:yes; default 1)', '-r')
        input_arg('auto login(0:no, 1:yes; default 0)', '-a')
    #If verbose is True(that means 'pycatconf' runs alone), print user's
    #information to confirm. Or(that means 'pycatconf' is called as a module)
    #do nothing. 
    if verbose:
        print 'You settings:'
        print '  User name: \t%s' % info['-u']
        print '  Password: \t%s' % info['-p']
        print '  Server IP: \t%s' % info['-ip']
        print '  Remember passwd(0:no,1:yes): \t%s' % info['-r']
        print '  Auto login(0:no,1:yes): \t%s' % info['-a']
    #Write the options to account file.
    write_info()
    return True
    
#If 'pycatconf' invoked in command line, run main function with no argument.
#Else if 'pycatconf' invoked as a module, do nothing.
if __name__ == "__main__":
  main()
