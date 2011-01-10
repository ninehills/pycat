#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys

import pycatconf
import pycat

if sys.platform == 'win32':
    imagepath = os.path.join(os.path.dirname(__file__), 'data')
else:
    imagepath = '/usr/share/pycat/data'

ui_info ="""
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='Preference'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='ToolMenu'>
      <menuitem action='Poem'/>
      <separator/>
      <menuitem action='FlowGraph'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='Thanks'/>
      <separator/>
      <menuitem action='About'/>
    </menu>
  </menubar>
</ui>
"""

class About_Dialog:
    def delete_event(self,widget,event,data=None):
        return False

    def destroy(self,widget,event):
        self.dialog.destroy()

    def show(self):
        self.dialog.show_all()

    def __init__(self,VERSION):
        self.dialog=gtk.Dialog("关于 pycat", None, 0, None)
        button=self.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        button.grab_focus()
        self.dialog.set_default_size(300,280)
        self.dialog.set_icon_from_file(os.path.join(imagepath, 'pycat.png'))
        self.dialog.connect("delete_event",self.delete_event)
        self.dialog.connect("response",self.destroy)
        self.dialog.set_has_separator(True)
        self.dialog.set_position(gtk.WIN_POS_NONE)
        self.image=gtk.Image()
        self.image.set_from_file(os.path.join(imagepath, "logo.png"))
        self.dialog.vbox.pack_start(self.image,True,True)
        string="<span size='x-large' weight='heavy'>pycat gateway client %s</span>\n<span weight='heavy' style='italic'>for Nankai University</span>\n\nModifid By cynic, from ideal Shang\nswulling@gmail.com idealities@gmail.com" % (VERSION,)
        self.label=gtk.Label(string)
        self.label.set_use_markup(True)
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.linkbutton=gtk.LinkButton("http://9hills.us/pycat", "http://9hills.us/pycat")
        self.dialog.vbox.pack_start(self.label,True,True,8)
        self.dialog.vbox.pack_start(self.linkbutton,False,False,8)
        
class Poem_Dialog:
    def delete_event(self,widget,event):
        return False

    def response(self,widget,res_id):
        if res_id == 1:
            self.refresh()
        elif res_id == gtk.RESPONSE_CLOSE:
            self.dialog.destroy()

    def refresh(self):
        import random
        i = random.randint(1,313)
        begin = self.__find__(i-1)
        end = self.__find__(i)
        string = self.tangshi[begin+1:end]
        self.textbuffer.set_text(string)

    def __find__(self, place,char="%"):
        i = 0
        count = 0
        while (count < place):
            if self.tangshi[i] == char:
                count += 1
            i += 1
        return i-1

    def show(self):
        self.dialog.show_all()

    def __init__(self):
        self.dialog=gtk.Dialog("诗词", None, 0, None)
        next = self.dialog.add_button("下一首(_N)",1)
        self.dialog.add_button(gtk.STOCK_CLOSE,gtk.RESPONSE_CLOSE)
        self.dialog.set_default_size(400,280)
        self.dialog.set_icon_from_file(os.path.join(imagepath, 'pycat.png'))
        self.dialog.connect("delete_event",self.delete_event)
        self.dialog.connect("response",self.response)
        self.dialog.set_has_separator(True)
        self.dialog.set_position(gtk.WIN_POS_NONE)
        self.dialog.set_border_width(4) #set vbox border width not work
        self.tangshi = ""
        try:
            f = open(imagepath+"/tangshi", "r")
            try:
                self.tangshi = f.read()
            finally:
                f.close()
        except:
            pass
        self.textbuffer = gtk.TextBuffer()
        self.textview=gtk.TextView(self.textbuffer)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.dialog.vbox.pack_start(self.textview,True,True,8)
        next.grab_focus()
        next.clicked()

class Pycatgui:
    account = ['', '', '202.113.18.188', '1', '0']
    stat_str = """
在线时间：                
已用流量：                
账户余额：                
"""
    
    def __create_actions(self):
        entries = [
          ( "FileMenu", None, "文件(_F)" ), # name, stock id, label
          ( "ToolMenu", None, "工具(_T)" ),
          ( "HelpMenu", None, "帮助(_H)" ),
          ( "Preference", gtk.STOCK_PREFERENCES, # name, stock id
            "首选项(_P)", "<control>P", # label, accelerator
            "设置账户信息",             # tooltip
            self.preference ),          # callback
          ( "Quit", gtk.STOCK_QUIT,
            "退出(_Q)", "<control>Q",
            "退出程序",
            self.quit ),
          ( "Poem", gtk.STOCK_INFO,
            "诗词(_E)","<control>E",
            "阅读诗词",
            self.poem ), 
          ( "Thanks", None,
            "主题(_S)","<control>S",
            "主题",
            self.thanks ), 
          ( "About", gtk.STOCK_ABOUT,
            "关于(_A)", "<control>A",
            "关于",
            self.about ),
        ]
        toggle_entries = [
          ( "FlowGraph", gtk.STOCK_INFO,
            "流量图(_I)", "<control>I",
            "流量图",
            self.flowgraph,
            False ),
        ]
        actions = gtk.ActionGroup("Actions")
        actions.add_actions(entries)
        actions.add_toggle_actions(toggle_entries)
        return actions
        
    def preference(self, widget):
        return True
        
    def about(self, widget):
        about = About_Dialog(pycat.VERSION)
        about.show()
        return True
        
    def poem(self, widget):
        poem = Poem_Dialog()
        poem.show()
        return True
        
    def flowgraph(self, widget):
        return True
        
    #Method called when close window button was clicked.
    def hide(self, widget, data=None):
        self.window.hide()
        while gtk.events_pending():
            gtk.main_iteration()
        return True
        
    def __connect__(self):
        ret = pycat.connect(self.account)[0]
        if not ret:
            return False
        return True
        
    def stat(self, widget, data=None):
        if len(pycat.conn_info) == 0:
            ret = self.__connect__()
            if not ret:
                return False
        (ret, retdata) = pycat.query()
        if ret == True:
            stat_str = """
在线时间： %s
已用流量： %s
账号余额： %s
""" % (retdata['time'], retdata['flow'], retdata['fee'])
            self.stat_frame.set_label("当前状态： 已连线")
            self.stat_label.set_text(stat_str)
            self.stat_label.show()
            self.stat_frame.show()
            self.trayicon.set_from_file(os.path.join(imagepath, 'online.png'))
            self.trayicon.set_tooltip('Pycat: Online')
            self.trayicon.set_visible(True)
        else:
            self.stat_frame.set_label("当前状态：未连线")
            self.stat_label.set_text(self.stat_str)
            self.stat_label.show()
            self.stat_frame.show()
            self.trayicon.set_from_file(os.path.join(imagepath, 'offline.png'))
            self.trayicon.set_tooltip('Pycat: Offline')
            self.trayicon.set_visible(True)
        self.window.present()
        return True
    
    #显示帮助信息
    def thanks(self, widget, data=None):
        dialog = gtk.Dialog("主题", None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_border_width(20)
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_icon_from_file(os.path.join(imagepath, 'pycat.png'))
        msg = """
                 Pycat %s
\nPycat 是用于登录南开大学计费网关的客户端。
按照GPL协议发布。
\n南开大学有两个网关，一个188，一个180，如果某个网关登录无效，请换另一个网关使用
\n目前已知西区为188，五教为180。应该是宿舍区和教学区的区别。
\n感谢:
ideal 交大客户端开发者
Solrex (http://solrex.cn) 原作者
fortune-zh (where tangshi 300 poems come from)
""" % pycat.VERSION
        label = gtk.Label(msg)
        dialog.vbox.pack_start(label, True, True, 0)
        label.show()
        if dialog.run() == gtk.RESPONSE_OK:
            dialog.destroy()
        return True
    
    def callback_cb(self, widget, data=None):
        if data == 0:
            self.account[3] = ('0', '1')[widget.get_active()]
            if not widget.get_active():
                self.c_auto.set_active(False)
                self.account[3] = '0'
        elif data == 1:
            if self.c_rem.get_active():
                self.account[4] = ('0', '1')[widget.get_active()]
            else:
                self.c_auto.set_active(False)
        return True
    
    def online(self, widget, data=None):
        self.e_user.set_editable(False)
        self.e_passwd.set_editable(False)
        self.account[0] = self.e_user.get_text()
        self.account[1] = self.e_passwd.get_text()
        self.account[2] = self.e_server.get_text()
        pycatconf.info['-u'] = self.account[0]
        pycatconf.info['-p'] = self.account[1]
        pycatconf.info['-ip'] = self.account[2]
        pycatconf.info['-r'] = self.account[3]
        pycatconf.info['-a'] = self.account[4]
        pycatconf.write_info()
        (ret, retstr) = pycat.online(self.account)
        #automatic kick the account which is being in use
        if ret == False:
            if retstr == 'Account is being in use!':
                (ret, retstr) = pycat.kick(self.account)#kick includes relogin
        self.status_bar.pop(self.sid)
        self.status_bar.push(self.sid, retstr)
        self.stat(None, None)
        return True
    
    def offline(self, widget, data=None):
        (ret, retstr) = pycat.offline()
        self.status_bar.pop(self.sid)
        self.status_bar.push(self.sid, retstr)
        self.stat(None, None)
        return True
        
    def quit(self, widget, data=None):
        if len(pycat.conn_info) > 0:
            pycat.conn_info[0].close()
        gtk.main_quit()
        return False
        
    def pop(self, widget, data=None):
        if self.window.is_active():
            self.window.hide()
            while gtk.events_pending():
                gtk.main_iteration()
        else:
            self.window.present()
        return True
        
    #Pop up menu
    def pop_menu(self, widget, button, time, data=None):
        if data:
            data.show_all()
            data.popup(None, None, gtk.status_icon_position_menu, button, time,widget)
        return True
        
    def __init__(self):
        i =  pycatconf.show()
        if i != False:
            self.account = i.split(':')
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Pycat 客户端')
        self.window.set_icon_from_file(os.path.join(imagepath, 'pycat.png'))
        self.window.set_position(gtk.WIN_POS_NONE)
        self.window.set_resizable(True)
        
        self.window.connect("delete-event", self.hide)
        self.window.connect("destroy", self.hide)
        
        ui = gtk.UIManager()
        ui.insert_action_group(self.__create_actions(), 0)
        self.window.add_accel_group(ui.get_accel_group())
        
        self.top_vbox = gtk.VBox(False, 0)
        self.window.add(self.top_vbox)
        
        ui.add_ui_from_string(ui_info)
        
        bar = ui.get_widget("/MenuBar")
        self.top_vbox.pack_start(bar, False, True, 0)
        bar.show()
        
        separator = gtk.HSeparator()
        self.top_vbox.pack_start(separator, False, True, 0)
        separator.show()

        main_vbox = gtk.VBox(False, 0)
        main_vbox.set_border_width(10)
        self.top_vbox.add(main_vbox)
        
        self.stat_frame = gtk.Frame('当前状态： 未连线')
        main_vbox.pack_start(self.stat_frame, True, True, 0)

        self.stat_label = gtk.Label(self.stat_str)
        self.stat_frame.add(self.stat_label)
        self.stat_label.show()
        self.stat_frame.show()

        bbox = gtk.HButtonBox()
        bbox.set_border_width(10)
        bbox.set_layout(gtk.BUTTONBOX_END)
        main_vbox.pack_start(bbox, False, True, 0)
        b_stat = gtk.Button('刷新(_R)')
        b_stat.connect('clicked', self.stat, None)
        bbox.add(b_stat)
        b_stat.show()

        bbox.show()

        li_hbox = gtk.HBox(False,0)
        main_vbox.pack_start(li_hbox, True, True, 0)

        l_vbox = gtk.VBox(False, 0)
        li_hbox.pack_start(l_vbox, True, True, 0)
        r_vbox = gtk.VBox(False, 0)
        li_hbox.pack_start(r_vbox, True, True, 0)

        label = gtk.Label('用户名')
        l_vbox.pack_start(label, True, True, 0)
        label.show()

        self.e_user = gtk.Entry()
        self.e_user.set_max_length(20)
        self.e_user.set_text(self.account[0])
        r_vbox.pack_start(self.e_user, True, True, 0)
        self.e_user.show()

        label = gtk.Label('密  码')
        l_vbox.pack_start(label, True, True, 0)
        label.show()

        self.e_passwd = gtk.Entry()
        self.e_passwd.set_max_length(32)
        self.e_passwd.set_visibility(False)
        self.e_passwd.set_text(self.account[1])
        r_vbox.pack_start(self.e_passwd, True, True, 0)
        self.e_passwd.show()

        label = gtk.Label('服务器')
        l_vbox.pack_start(label, True, True, 0)
        label.show()

        self.e_server = gtk.Entry()
        self.e_server.set_max_length(20)
        self.e_server.set_text(self.account[2])
        #self.e_server.set_editable(False)
        r_vbox.pack_start(self.e_server, True, True, 0)
        self.e_server.show()

        l_vbox.show()
        r_vbox.show()
        li_hbox.show()

        bbox = gtk.HButtonBox()
        bbox.set_border_width(10)
        main_vbox.pack_start(bbox, False, True, 0)

        self.c_rem = gtk.CheckButton('记住密码')
        self.c_rem.connect('toggled', self.callback_cb, 0)
        self.c_rem.set_active(int(self.account[3]))
        bbox.add(self.c_rem)
        self.c_rem.show()

        self.c_auto = gtk.CheckButton('下次自动登录')
        self.c_auto.connect('toggled', self.callback_cb, 1)
        self.c_auto.set_active(int(self.account[4]))
        bbox.add(self.c_auto)
        self.c_auto.show()
        bbox.show()

        separator = gtk.HSeparator()
        main_vbox.pack_start(separator, False, True, 0)
        separator.show()

        bbox = gtk.HButtonBox()
        bbox.set_border_width(10)
        bbox.set_spacing(4)
        main_vbox.pack_start(bbox, False, True, 0)

        b_online = gtk.Button('登录(_L)')
        b_online.connect('clicked', self.online, None)
        bbox.add(b_online)
        #b_online.set_flags(gtk.CAN_DEFAULT)
        #b_online.grab_default()
        b_online.show()

        b_offline = gtk.Button('离线(_O)')
        b_offline.connect('clicked', self.offline, None)
        bbox.add(b_offline)
        b_offline.show()

        b_help = gtk.Button('退出(_Q)')
        b_help.connect('clicked', self.quit, None)
        bbox.add(b_help)
        b_help.show()
        bbox.show()

        self.status_bar = gtk.Statusbar()
        self.top_vbox.pack_start(self.status_bar, False, True, 0)
        self.status_bar.show()
        self.sid = self.status_bar.get_context_id("Pycat")

        p_menu = gtk.Menu()
        menu_item = gtk.MenuItem('显示')
        menu_item.connect('activate', self.pop, None)
        p_menu.append(menu_item)
        menu_item = gtk.SeparatorMenuItem()
        p_menu.append(menu_item)
        menu_item = gtk.MenuItem('登录')
        menu_item.connect('activate', self.online, None)
        p_menu.append(menu_item)
        menu_item = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
        menu_item.connect('activate', self.stat, None)
        p_menu.append(menu_item)
        menu_item = gtk.MenuItem('离线')
        menu_item.connect('activate', self.offline, None)
        p_menu.append(menu_item)
        menu_item = gtk.SeparatorMenuItem()
        p_menu.append(menu_item)
        menu_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu_item.connect('activate', self.about)
        p_menu.append(menu_item)
        menu_item = gtk.SeparatorMenuItem()
        p_menu.append(menu_item)
        menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu_item.connect('activate', self.quit, None)
        p_menu.append(menu_item)

        self.trayicon = gtk.StatusIcon()
        self.trayicon.connect('activate', self.pop)
        self.trayicon.connect('popup-menu', self.pop_menu, p_menu)
        self.trayicon.set_from_file(os.path.join(imagepath, 'offline.png'))
        self.trayicon.set_tooltip('Pycat: Offline')
        self.trayicon.set_visible(True)

        self.top_vbox.show()
        main_vbox.show()
        self.window.show()

        if self.account[4] == '1' and len(self.account[2]) > 0:
            b_online.clicked()
        b_stat.clicked()
        if self.window.is_active() == False:
            self.window.present()
            
def main():
    gtk.main()
    return True
    
if __name__ == "__main__":
    cat = Pycatgui()
    main()
