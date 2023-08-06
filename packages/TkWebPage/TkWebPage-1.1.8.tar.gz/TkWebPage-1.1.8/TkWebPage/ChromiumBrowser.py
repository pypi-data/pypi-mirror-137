from tkinter import Frame,Tk
from MBPython import miniblink
import platform
class Chromium:
    dictionary={}
    def __init__(self,name,url="http://www.baidu.com",title="Browser",dictionary=dictionary):
        li = [url,title]
        if type(name) == type([]):
            for i in name:
                dictionary[i] = li
        else:
            dictionary[name] = li
    def url(self,name,url,dictionary=dictionary):
        dictionary[name][0] = url
    def title(self,name,title,dictionary=dictionary):
        dictionary[name][1] = title
    def run(self,name,dictionary=dictionary):
        a=Tk()
        a.state("zoom")
        a.update()
        a.title(dictionary[name][1])
        mbpython=miniblink.Miniblink
        if platform.machine() == "AMD64":
            mb=mbpython.init('./miniblink_x64.dll')
        else:
            mb=mbpython.init('./node.dll')
        wke=mbpython(mb)
        window=wke.window
        webview=window.wkeCreateWebWindow(2,a.winfo_id(),0,0,a.winfo_width(),a.winfo_height())
        mb.wkeLoadURLW(webview,dictionary[name][0])
        window.wkeShowWindow(webview)
        a.mainloop()
        return dictionary[name]
