"""
class IE:
    url,geometry,title = "","",""
    def __init__(self,url="www.baidu.com",geometry="1200*600+100+10",title="Browser"):
        url,geometry,title = url,geometry,title
    def change_url(self,change_url):
        url = change_url
    def change_geometry(self,change_geometry):
        geometry = change_geometry
    def chang_title(self,change_title):
        title = change_title
    def run(self):
        return[url,geometry,title]
"""
from tkinter import Frame,Tk
from tkwebview2.tkwebview2 import WebView2
class IE:
    dictionary={}
    def __init__(self,name,url="http://www.baidu.com",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):
        li = [url,geometry,title]
        if type(name) == type([]):
            for i in name:
                dictionary[i] = li
        else:
            dictionary[name] = li
    def url(self,name,url,dictionary=dictionary):
        dictionary[name][0] = url
    def geometry(self,name,geometry,dictionary=dictionary):
        dictionary[name][1] = geometry
    def title(self,name,title,dictionary=dictionary):
        dictionary[name][2] = title
    def run(self,name,dictionary=dictionary):
        root = Tk()
        root.title(dictionary[name][2])
        root.geometry(dictionary[name][1])
        frame = WebView2(root,1300,610)
        frame.load_url(dictionary[name][0])
        frame.pack(fill="x",expand=True)
        root.mainloop()
        return dictionary[name]
class HTML:
    dictionary={}
    def __init__(self,name,html="<h1>Browser</h1>",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):
        li = [html,geometry,title]
        if type(name) == type([]):
            for i in name:
                dictionary[i] = li
        else:
            dictionary[name] = li
    def html(self,name,html,dictionary=dictionary):
        dictionary[name][0] = html
    def geometry(self,name,geometry,dictionary=dictionary):
        dictionary[name][1] = geometry
    def title(self,name,title,dictionary=dictionary):
        dictionary[name][2] = title
    def run(self,name,dictionary=dictionary):
        root = Tk()
        root.title(dictionary[name][2])
        root.geometry(dictionary[name][1])
        frame = WebView2(root,1300,610)
        frame.load_html(dictionary[name][0])
        frame.pack(fill="x",expand=True)
        root.mainloop()
        return dictionary[name]
