## ASTOR

**Astor**：基于`Python3.x`和`Django2.x`

项目尽量使用Django内部提供的API，后台管理为Django自带的管理系统django-admin。

## 在线样例：

### 在线地址

[http://astor.eveneko.com](http://astor.eveneko.com)

账号：eveneko

密码：241106

### 管理人员入口

[http://astor.eveneko.com/admin](http://astor.eveneko.com/admin)

账号：eveneko

密码：rootroot


## 预览：

## 安装：

### 依赖包安装

下载文件进入项目目录之后，使用pip安装依赖包

`pip3 install -r requirements.txt`

### 数据库配置

数据库默认使用`Django`项目生成时自动创建的小型数据库`sqlite`

也可自行配置连接使用MySQL

现成数据库地址：[db.sqlite][http://share.eveneko.com/db.sqlite3]

### 创建超级用户

终端下执行:

`./python manage.py createsuperuser`

然后输入相应的超级用户名以及密码，邮箱即可。

### 开始运行

终端下执行:

`./python manage.py runserver`

浏览器打开: `http://127.0.0.1/` 即可进入普通用户入口

浏览器打开: `http://127.0.0.1/admin` 即可进入超级用户入口


[]: http://share.eveneko.com/db.sqlite3