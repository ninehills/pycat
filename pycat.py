#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 ----------------------------------------------------------------------
 ideal idealities@gmail.com
 Homepage: http://dev.bjtu.edu.cn/ideal

 Modified By cynic <swulling@gmail.com>
 Homepage: http://9hills.us
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

import sys
import httplib
import pycatconf
import urllib

NAME = "Pycat 0.0.6"
VERSION = "0.0.6"

#Share the connection information.
conn_info = []

#Display helper information.
def usage():
    print '''Useage: pycat [options]
Options:
    [None]\tPrint this message
    on\t\tOnline
    off\t\tOffline
    query\tPrint account statistics
    kick\t[Unable]Kick off the online account
    status\tLike query but report the online status
    fortune\tA sentence
    --help\tPrint this message

Examples:
    pycat on
    pycat query

*NOTE*: Before use "pycat", you must configure your account with
    "pycatconf" command. 

Modified By cynic (swulling@gmail.com)
Homepage: http://9hills.us

Orign: ideal (idealities@gmail.com)
Homepage: http://dev.bjtu.edu.cn/ideal
'''
    sys.exit(0)
    
def connect(account):
    result = False
    if len(conn_info) == 0:
        conn = httplib.HTTPConnection(account[2])
        conn_info.insert(0, conn)
    else:
        conn = conn_info[0]
    try:
        conn.connect()
    except httplib.InvalidURL:
        msg = 'Error server ip, please run pycatconf to reconfigure.'
    except Exception:
        msg = 'Error occured when connected to the server.'
    else:
        headers = {'Host':account[2],'User-Agent':NAME}
        conn_info.insert(1, headers)
        result = True
        msg = 'Connection OK'
    return (result, msg)
    
def __getmsg__(line):
    '''返回网关信息代码

    首先在返回的网页中寻找"Msg"字段，如果找不到，返回空字符串。
    找到后，截取从Msg出现处再靠后5个字节到';'结束（不包括';'号，前四个字节为'Msg='）并返回。
    Msg的具体意义参见 doc/msg.txt
    '''
    start = line.find('Msg')
    if start == -1:
        return ''
    start += 4
    end = line.find(';', start)
    return line[start:end]
    
def online(account):
    conn = conn_info[0]
    data = 'DDDDD=%s&upass=%s' % (account[0], account[1])
    #import hashlib
    #data = 'DDDDD1=%s&upass=%s' % (account[0], hashlib.md5('1'+account[1]+'12345678').hexdigest()+'12345678'+'1')
    submit = "登录 login"
    submit = urllib.quote(submit)
    data += ('&0MKKey=' + submit)
    #data += '&R1=0&R2=1&para=00&0MKKey=123456'
    headers = {'Host':account[2],'User-Agent':NAME,
             'Content-Length':str(len(data))}
    conn.request('POST', '/', data, headers)
    res = conn.getresponse()
    res_html = res.read()
    #南开网关在登录成功后会跳转到http://gateway/1.htm页面(window.location=url2)
    #只有在出现错误的时候才能显示错误代码(Msg)
    #同时在登录成功后返回的页面中包含"Gno=01"字符串。
    if(res_html.find("Gno=01") == -1):
        code = __getmsg__(res_html)
        if code == '01':
            #"帐号或密码不对，请重新输入"
            return (False, 'Wrong ID or password, please reconfigure.')
        elif code == '02':
            #"该账号正在使用中"
            return (False, 'Account is being in use!')
        elif code == '04':
            #"本帐号费用超支或时长流量超过限制"
            return (False, 'Sorry, your account is overspended.')
        elif code == '05':
            #"本帐号暂停使用"
            return (False, 'Sorry, your account is paused to use.')
        else:
            #'' or other
            return (False, 'Unknown error!')
    else:
        return (True, 'Online succeeded.')
        
def fortune():
    msg = "九原山区(http://9hills.us)欢迎您！"
    if sys.getfilesystemencoding() == "mbcs":
        return (True, msg.decode('UTF-8').encode('GBK'))
    return (True, msg)

def offline():
    conn = conn_info[0]
    headers = conn_info[1]
    # 离线地址: http://gateway/F.htm
    conn.request('GET', '/F.htm', None, headers)
    res = conn.getresponse()
    res_html = res.read()
    code = __getmsg__(res_html)
    if code == '14':
        #"注销成功"
        return (True, 'Offline succeeded.')
    else:
        #未在线或其他错误
        return (False, 'Offline failed. Due to some error.')
    
def __getinfo__(line):
    result = {}
    start = line.find('time')
    if start == -1:
        time = '-1'
    else:
        start += 6
        end = line.find('\'', start)
        time = line[start:end]
    time = int(time)
    result['time'] = time
    
    start = line.find('flow')
    if start == -1:
        flow = '-1'
    else:
        start += 6
        end = line.find('\'', start)
        flow = line[start:end]
    flow = int(flow)
    result['flow'] = flow

    start = line.find('fee')
    if start == -1:
        fee = '-1'
    else:
        start += 5
        end = line.find('\'', start)
        fee = line[start:end]
    fee = int(fee)
    result['fee'] = fee

    return result
    
def __convtime__(time):
    if time < 60:
        return str(time)+'min'
    elif time >= 60 and time < 1440:
        return str(time/60)+'hour '+str(time%60)+'min'
    else:
        return str(time/1440)+'day '+str((time%1440)/60)+'hour '+str((time%1440)%60)+'min'
    
def __convflow__(flow):
    #TODO: need improvement
    flowk = flow%1024
    flowm = (flow - flowk)/1024
    flowg = flowm/1024
    flowm = flowm%1024
    result = ''
    if flowg != 0:
        result += str(flowg) + 'G '
    result += str(flowm) + 'M ' + str(flowk) + 'K'
    return result

def __convfee__(fee):
    fee = float(fee)/10000
    result = str(fee) + ' yuan'
    return result

def query():
    conn = conn_info[0]
    headers = conn_info[1]
    conn.request('GET', '/', None, headers)
    res = conn.getresponse()
    res_html = res.read()
    stat = __getinfo__(res_html)
    if stat['time'] == -1 or stat['flow'] == -1 or stat['fee'] == -1:
        return (False, 'Query failed, please be online first!')
    stat['time'] = __convtime__(stat['time'])
    stat['flow'] = __convflow__(stat['flow'])
    stat['fee'] = __convfee__(stat['fee'])
    return (True, stat)
    
def kick(account):
    #该功能不可用
    conn = conn_info[0]
    headers = conn_info[1]
    conn.request('GET', '/a11.htm', None, headers)
    res = conn.getresponse()
    res_html = res.read()
    if (res_html.find("请输入账号密码，重登录") != -1):
        data = 'DDDDD=%s&upass=%s' % (account[0], account[1])
        data += '&AMKKey=%B5%C7++%C2%BC'
        headers = {'Host':account[2],'User-Agent':NAME,
                 'Content-Length':str(len(data))}
        conn.request('POST', '/a11.htm', data, headers)
        res = conn.getresponse()
        res_html = res.read()
        if(res_html.find("您已经成功登录") == -1):
            return (False, 'Unknown error after kicked the account!')
        else:
            return (True, 'Online succeeded.')
    return (False, 'Error occured when kick the account being in use.')
    
def main(account=[], verbose=True):
    if len(account) != 5:
        s = pycatconf.show()
        if s != False:
            account = s.split(':')
        else:
            print 'Please run pycatconf and configure infomation first :)'
    result = ''
    if(connect(account)[0] == False):
        return (False, 'Connect Failed')
    else:
        if len(sys.argv) == 1:
            conn_info[0].close()
            usage()
        elif sys.argv[1] == 'on':
            ret, retstr = online(account)
            result += retstr
            ret, retdata = query()
            if ret:
                result += 'Time: %s\nUsed: %s\nBanlance: %s\n' % (retdata['time'], retdata['flow'], retdata['fee'])
        elif sys.argv[1] == 'query':
            ret, retdata = query()
            if ret:
                result += 'Time: %s\nUsed: %s\nBanlance: %s\n' % (retdata['time'], retdata['flow'], retdata['fee'])
            else:
                result += retdata
        elif sys.argv[1] == 'off':
            ret, retdata = query()
            if ret:
                result += 'Time: %s\nUsed: %s\nBanlance: %s\n' % (retdata['time'], retdata['flow'], retdata['fee'])
            else:
                pass
            ret, retstr = offline()
            result += retstr
        elif sys.argv[1] == 'kick':
            print 'This option is unable:', sys.argv[1]
            usage()
            #ret, retstr = kick(account)
            #result += retstr
        elif sys.argv[1] == 'fortune':
            ret, retstr = fortune()
            result += retstr
        elif sys.argv[1] == 'status':
            ret, retdata = query()
            if ret:
                result += 'Status: online\n' \
                          'Time: %s\nUsed: %s\nBanlance: %s\n' % (retdata['time'], retdata['flow'], retdata['fee'])
            else:
                result += 'Status: offline'
        #TODO: change password
        else:
            if verbose:
                conn_info[0].close()
                if not (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
                    print 'Unknown option:', sys.argv[1]
                usage()
            else:
                conn_info[0].close()
                return False
    conn_info[0].close()
    if verbose:
        print result
        
if __name__ == '__main__':
    main()
