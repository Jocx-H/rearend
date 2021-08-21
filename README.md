[TOC]

# rearend

> 暑假实训项目的后端部分。

## 功能实现

<img src="img/image-20210820144457307.png" alt="image-20210820144457307" style="zoom:80%;" />

待讨论。

## 运行环境

> 仅列出主要安装的库。

```
# Name                    Version                   Build  Channel
python                    3.7.11               h6244533_0    defaults
aiofiles                  0.7.0                    pypi_0    pypi
fastapi                   0.68.0                   pypi_0    pypi
PyMySQL                   1.0.2                    pypi_0    pypi
uvicorn                   0.15.0                   pypi_0    pypi
```

## 开发者须知

### 文件存放

- `api`存放各功能模块需要调用的接口，即控制层。
- `assert`存放静态资源。
- `dao`存放与数据库有关的操作，即数据层。
- `service`存放与数据处理、行为逻辑有关的操作，即逻辑层。
- `model`存放自定义类等，即模型层。
- `img`存放readme中使用到的图片。

### 代码规范

- 使用pep8编码规范，vscode的话可以通过在`setting.json`文件中设置`"python.formatting.provider": "autopep8"`从而使默认的格式化文档风格为pep8，**写完代码后保持格式化文档一下的习惯**，下面说的是只靠格式化解决不了的问题。
- 引入第三方库别用`from ... import *`，用`import`或者要用啥引啥，比如`from PyQt5 import QWidget`，引用自己写的模块视情况而定。尽量不要将所有的内容全引入了，这样会很臃肿。引入内容按照__字典序排列__。
- 正式内容与引入内容间隔两行，类外函数两两间间隔两行，内类函数两两间间隔一行。

以下几点点均可以在编辑器中设置<img src="img/image-20210820151023689.png" alt="image-20210820151023689" style="zoom:80%;" />，修改可以参考https://www.cxyzjd.com/article/github_38851471/85268075（记得git的也要改，这是为了避免：https://github.com/cssmagic/blog/issues/22）。

- 使用 **4 空格缩进**，禁用任何 TAB 符号（编辑器或者idle可以设置自动将tab转成空格）。
- 源码文件使用 **UTF-8 无 BOM 编码格式（UTF-8）**。
- 总是使用 **Unix \n 风格换行符（LF）**。

- 在每一个 py 文件头，都添加如下内容：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 描述w
```

#### 函数规范

- 函数名使用小写单词命名，多个单词之间用下划线连接，保护函数以下划线开头，私有函数以下双下划线开头（继承父类来的比如`paintEvent`来的就没办法了）：

```python
def demo_function():
	pass
def _private_function():
	pass
```

下面两点的语法可参考：https://docs.python.org/zh-cn/3/library/typing.html

- 自定义函数要表明返回值类型（接口可以省了反正都是一样的）

```python
def heihei(): -> None
    pass
def hah(): -> bool
    return True
```

- 函数参数需要注明类型

```python
def getusers(uname: str):
    return userService.getUserInfos(uname)
```

- 函数的开头要写功能**注释**，并且给出参数解释，特殊情况下给出__返回值解释__和__示例__

```python
def hhh():
    r"""balabala
    """
    pass

def hhh2(para_1: str, para_2: int):
    r"""
    balabala
    
    Args:
    	para_1(str): balabala
    				balabala
	    para_2(int): balabala
    """
    pass
```

- 代码块中的注释可写可不写，但尽量写块注释而不是行注释：

```python
# 我是块注释
pass
pass

pass # 我是行注释
```

#### 文件命名规范

- 文件和文件夹使用**小写单词**命名，多个单词之间用下划线连接：

```python
demo_module
demo_do_something.py
```

#### 类命名规范

- 类名：（大驼峰原则）

每个单词的首字母大写，私有类以下划线开头，后面也是每个单词的首字母大写，多个单词拼接：

```python
class DemoClass():
	pass
class _PrivateClass():
	pass
```

#### 变量规范

- 变量名：

  使用小写单词命名，多个单词之间用下划线连接：

```python
demo_variable = "Hello Python"
```

- 常量：

  使用大写单词命名，多个单词之间用下划线连接：

```python
DEMO_CONSTANT = 100
```

* 全局变量位置：

  在引入内容下方，正式内容上方。与引入内容间隔一行，与正式内容间隔两行

```python
from somefile import something

file_path = "balabalabala"


def get():
    pass
```

* 列表书写格式：
  仅有单行数值可以在同一行表示，其他均需换行表示

```python
list_1 = [1, 2, 3, 4]

list_2 = [
    "sdf", "sdf", "sdf"
]

list_3 = [
    [1, 1, 1, 1],
    [2, 2, 2, 2],
    [3, 3, 3, 3]
]
```

* 字典书写格式：
  内容均需要换行

```python
dict_1 = {
    "key": value,
    "key_2": value
}
```

### Github上传规则

多人协作的工作模式通常是这样：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功！

如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

详见：https://www.liaoxuefeng.com/wiki/896043488029600/900375748016320

如果你不想你的工作被别人的push打扰，可以自己开一个分支，比如`git branch lxh`在上面提交，然后之后再将`lxh`和`main`合并。

## 接口设计

### 控制层

数据库里面的数据自诞生起位置在数据库中就是固定的。若要对数据进行排序等操作，必须先将满足条件的数据取到后端，再进行操作。

* 增：

  接收来自前端的数据，添加新的数据对到数据库中

  ```python
  def add(d_name: str, data: dict)
  ```

  说明：

  1. `d_name`：数据库的名字
  2. `data`：需要存储的数据，键值对与数据库表单内容一一对应

* 删：
  接收前端的信号，删除特定数据库中的某个特定数据

  ```python
  def remove(d_name: str, **kargs)
  ```

  说明：

  1. `d_name`：数据库的名字
  2. `kargs`：可选参数字典，但是二者必须有其一，里面包括的有效键为：
     * `doc: str`：需要删除数据的键
     * `where: bool`：删除满足该判别式的数据

* 改：
  根据前端的数据更改数据库

  ```python
  def updata(d_name: str, doc: str, data: dict)
  ```

  说明：

  1. `d_name`：数据库的名字
  2. `doc`：需要删除数据的键
  3. `data`：需要更新的

* 查：
  获取数据

  ```python
  def get(d_name: str, **kargs)
  ```

  说明：

  1. `d_name`：数据库名字
  2. `kargs`：可选参数字典，里面的有效键值为：
     * `doc: str`：数据的键
     * `where: bool`：获得满足该判别式的数据
     * `limit: int`：返回前端的数据条目，最多为20条
     * `skip: int`：跳过多少条数据库中的数据

### 服务层

### 数据层

数据层利用PyMySQL包直接于数据库进行交互

* 增

  ```python
  def add_to_db(d_name: str, data: dict) -> bool
  ```

  1. `d_name`：数据库名字
  2. `data`：需要增加的数据
  3. 返回值：如果添加成功返回`True`，否则`False`

* 删——通过键

  ```python
  def delete_to_db(d_name: str, doc: str) -> bool
  ```

  1. `d_name`：数据库名字
  2. `doc`：需要删除的数据的识别键
  3. 返回值：如果删除成功返回`True`，否则`False`

* 删——通过条件

  ```python
  def delete_to_db(d_name: str, where: bool) -> bool
  ```

  1. `d_name`：数据库名字
  2. `where`：所删数据所满足的判别式
  3. 返回值：如果删除成功返回`True`，否则`False`

* 改

  ```python
  def updata_to_db(d_name: str, doc: str, data: dict) -> bool
  ```

  1. `d_name`：数据库名字
  2. `doc`：需要修改的数据的识别键
  3. `data`：需要修改的数据
  4. 返回值：如果修改成功返回`True`，否则`False`

* 查——通过键

  ```python
  def get_from_db(d_name: str, doc: str) -> dict
  ```

  1. `d_name`：数据库名字
  2. `doc`：需要查找的数据的识别键
  3. 返回值：获得的数据

* 查——通过条件

  ```python
  def get_from_db(d_name: str, where: bool) -> list
  ```

  1. `d_name`：数据库名字
  2. `where`：所查数据所满足的判别式
  3. 返回值：多条数据

