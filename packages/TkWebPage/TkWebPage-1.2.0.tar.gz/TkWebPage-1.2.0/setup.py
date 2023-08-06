#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="TkWebPage",
    version="1.2.0",
    description=(
        "一个提供多种内核的网页浏览器"
    ),
    long_description="""
==================================================
这是一个提供网页浏览网页的库，包含Chromium和IE内核
==================================================

---------------------------------------------------------------------------------------
This is a package for web browser, including the Chromium and Internet explorer kernels
---------------------------------------------------------------------------------------


中文Chinese

========
使用方法
========

----
安装
----

安装方法：

pip install TkWebPage

----
使用
----

 * IE:

	 - def __init__(self,name,url="http://www.baidu.com",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):

		用来创建

		 - 使用：名字 = IE(名字)

		 - self：不用管

		 - name：名字（后期调用时需要填），str或list

		 - url：网址

		 - geometry：大小

		 - title：网页名称

		 - dictionary：格式：name:[url,geometry,title]（默认不需要提供，是因为不加报错所以添加）

	 - def url(self,name,url,dictionary=dictionary):

		用来更改网址

		 - 使用：名字.url(名字，网址)

		 - self：不用管

		 - name：名字（需要和上文填的一致）

		 - url：网址

	 - def geometry(self,name,geometry,dictionary=dictionary):

		用来更改大小

		 - 使用：名字.geometry(名字，大小，例"1200x600+100+10")

		 - name：名字

		 - geometry：大小（长x宽+长+宽）注：x是小写的X，不是乘号*

	 - def title(self,name,title,dictionary=dictionary):

		用来更改标题

		 - 使用：名字.title(名字，标题)

		 - name：名字

		 - title：标题

	 - def run(self,name,dictionary=dictionary):

		用来运行

		 - 使用：名字.run(名字)

		 - name：名字

 * HTML:

	 - 注：HTML用的是IE内核

	 - def __init__(self,name,html="<h1>Browser</h1>",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):

		用来创建

		 - 使用：名字 = IE(名字)

		 - self：不用管

		 - name：名字（后期调用时需要填），str或list

		 - html：HTML

		 - geometry：大小

		 - title：网页名称

		 - dictionary：格式：name:[url,geometry,title]（默认不需要提供，是因为不加报错所以添加）

	 - def html(self,name,html,dictionary=dictionary):

		用来更改HTML

		 - 使用：名字.html(名字，网址)

		 - self：不用管

		 - name：名字（需要和上文填的一致）

		 - html：网址

	 - def geometry(self,name,geometry,dictionary=dictionary):

		用来更改大小

		 - 使用：名字.geometry(名字，大小，例"1200x600+100+10")

		 - name：名字

		 - geometry：大小（长x宽+长+宽）注：x是小写的X，不是乘号*

	 - def title(self,name,title,dictionary=dictionary):

		用来更改标题

		 - 使用：名字.title(名字，标题)

		 - name：名字

		 - title：标题

	 - def run(self,name,dictionary=dictionary):

		用来运行

		 - 使用：名字.run(名字)

		 - name：名字
 * Chromium:

	 - def __init__(self,name,url="http://www.baidu.com",title="Browser",dictionary=dictionary):

		用来创建

		 - 使用：名字 = Chromium(名字)

		 - self：不用管

		 - name：名字（后期调用时需要填），str或list

		 - url：网址

		 - title：网页名称

		 - dictionary：格式：name:[url,geometry,title]（默认不需要提供，是因为不加报错所以添加）

	 - def url(self,name,url,dictionary=dictionary):

		用来更改网址

		 - 使用：名字.url(名字，网址)

		 - self：不用管

		 - name：名字（需要和上文填的一致）

		 - url：网址

	 - def title(self,name,title,dictionary=dictionary):

		用来更改标题

		 - 使用：名字.title(名字，标题)

		 - name：名字

		 - title：标题

	 - def run(self,name,dictionary=dictionary):

		用来运行

		 - 使用：名字.run(名字)

		 - name：名字

英文English

=============
Method of use
=============

=======
install
=======

Method of install:

pip install TkWebPage

----------
How to use
----------

 * IE:

	 - def __init__(self,name,url="http://www.baidu.com",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):

		Use it to init

		 - Use：name = IE(name)

		 - self：Don't need

		 - name：name（after this sentence will use it），format：str or list

		 - url：URL

		 - geometry：size

		 - title：the name of the webpage

		 - dictionary：format：name:[url,geometry,title]（The default does not need to be provided, because don't add it will  report error so add）

	 - def url(self,name,url,dictionary=dictionary):

		Usse it to change the url

		 - Use：name.url(name，url)

		 - self：Don't need

		 - name：name（Need the same as the name before）

		 - url：url

	 - def geometry(self,name,geometry,dictionary=dictionary):

		Use it to change the size

		 - Use：name.geometry(name，size，example"1200x600+100+10")

		 - name：name

		 - geometry：size（height x width + height + width）Note：X is a lowercase X, not a multiplication sign * 

	 - def title(self,name,title,dictionary=dictionary):

		Use it to change the title

		 - Use：name.title(name，title)

		 - name：name

		 - title：title

	 - def run(self,name,dictionary=dictionary):

		Use it to run the programme

		 - Use：name.run(nsme)

		 - name：name

 * HTML:

	 - Note: HTML use the IE kernel

	 - def __init__(self,name,html="<h1>Browser</h1>",geometry="1200x600+100+10",title="Browser",dictionary=dictionary):

		Use it to init

		 - Use：name = IE(name)

		 - self：Don't need

		 - name：name（after this sentence will use it），format：str or list

		 - html：HTML

		 - geometry：size

		 - title：the name of the webpage

		 - dictionary：format：name:[url,geometry,title]（The default does not need to be provided, because don't add it will  report error so add）

	 - def html(self,name,html,dictionary=dictionary):

		Usse it to change the html

		 - Use：name.html(name，html)

		 - self：Don't need

		 - name：name（Need the same as the name before）

		 - html：html

	 - def geometry(self,name,geometry,dictionary=dictionary):

		Use it to change the size

		 - Use：name.geometry(name，size，example"1200x600+100+10")

		 - name：name

		 - geometry：size（height x width + height + width）Note：X is a lowercase X, not a multiplication sign * 

	 - def title(self,name,title,dictionary=dictionary):

		Use it to change the title

		 - Use：name.title(name，title)

		 - name：name

		 - title：title

	 - def run(self,name,dictionary=dictionary):

		Use it to run the programme

		 - Use：name.run(nsme)

		 - name：name

 * Chromium:
	 - def __init__(self,name,url="http://www.baidu.com",title="Browser",dictionary=dictionary):

		Use it to init

		 - Use：name = IE(name)

		 - self：Don't need

		 - name：name（after this sentence will use it），format：str or list

		 - url：URL

		 - title：the name of the webpage

		 - dictionary：format：name:[url,geometry,title]（The default does not need to be provided, because don't add it will  report error so add）

	 - def url(self,name,url,dictionary=dictionary):

		Usse it to change the url

		 - Use：name.url(name，url)

		 - self：Don't need

		 - name：name（Need the same as the name before）

		 - url：url

	 - def title(self,name,title,dictionary=dictionary):

		Use it to change the title

		 - Use：name.title(name，title)

		 - name：name

		 - title：title

	 - def run(self,name,dictionary=dictionary):

		Use it to run the programme

		 - Use：name.run(nsme)

		 - name：name

========
打算Plan
========

 * 添加scipy以及requests

 * add scripy and requests

 * 添加完整版的双核浏览器（miniblink有一个）

 * add a perfect two-kenel-browser (miniblink has one)

 * 创建TkWebPage2（包含MBPython, tkwebview2, win32, win32gui以及其他依赖库）

 * create TkWebPage2 (that has MBPython, tkwebview2, win32, win32gui and other packages that need)

===============
历史版本History
===============

 * TkWebPage1.1.2

     - 创建了WebPage，并改名为TkWebPage

     - create a package named 'WebPage' and change the name to 'TkWebPage'

     - 完成了基本的浏览器双内核的安装

     - finish the simple two-kernel-browser

 * TkWebPage1.1.3

     - 添加齐全了文件（上个版本上传错了文件）

     - upload the whole document ( last package upload wrong document )

 * TkWebPage1.1.4

      - 添加齐全了python版本

      - add the whole python verion

 * TkWebPage1.1.5

      - 修复了安装方式

      - fix the download

      - 添加了日志

      - add the package update log

 * TkWebPage1.1.6

      - 添加齐全了文件（像1.1.3一样）

      - add the whole project(like 1.1.3)

 * TkWebPage1.1.7

      - 用了新的方法上传

      - use a new way to upload

 * TkWebPage1.1.8

      - 重新制定了zip

      - refresh the project zip

 * TkWebPage1.2.0

      - 完善了TkWebPage

      - finish the upload

      - 修复了无法下载.dll的问题

      - fix the warning that can't download .dll document
    """,
    author='CharlesCai',
    author_email='517639194@qq.com',
    maintainer='蔡沐含',
    maintainer_email='517639194@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://pypi.org/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        "tkwebview2>=1.2.0",
        "MBpython>=0.2.2",
    ],
    python_requires='>=3',
    include_package_data=True,
    py_modules=["TkWebPage"]
)
