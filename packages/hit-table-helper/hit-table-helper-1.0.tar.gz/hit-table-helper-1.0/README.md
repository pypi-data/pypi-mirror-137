# HIT课程表服务

### 特色

1. 课程表求交集
2. 蹭课课程表查询
3. 选择与自己课表不冲突的课程往往比较困难，程序可以自动完成
4. 导出到Excel
5. 陪对象可是当代大学生生活的一部分，所以最好的蹭课时机是对象在上课而你不上课。软件低耦合的支持了这项功能。
6. 陪对象可是当代大学生生活的一部分，你有课但是对象没课，那就可以试图把课调整到和对象一样。
7. 5和6都可以通过简单的集合运算实现

### 快速上手

### 安装
`pip install hit-table-helper`

在本项目目录下创建main.py，写下如下内容

如果顺利的话，你就会得到"我都能蹭的课.xlsx"
```python
from itertools import chain

from hit_table_helper.course_set import CourseSet
from hit_table_helper.id_generators import *

if __name__ == '__main__':
    # 4表示第四周，输入一个学期中间一点的周就行
    # 第二个参数传入None表示全部，传入某个字符串表示匹配
    cs = CourseSet.fromIteratorSearch(4, None, it=chain(wuLi(),  # 物院
                                                        shuXue(),  # 数院
                                                        yingCai(),  # 英才
                                                        gongKeShiYanBan()))  # 所有的“工科实验班”
    r = (cs - "我的学号")  # 改成你自己的学号就行，表示扣除你上的课。
    print(r.toExcel('我都能蹭的课.xlsx'))

```

### 更多使用方法

通常来讲我们需要将大表保存一下，这样方便我们之后使用。

多次使用学校的接口可能会炸掉，建议不要用本程序压测学校。

```python
from itertools import chain

from hit_table_helper.course_set import CourseSet
from hit_table_helper.id_generators import *

if __name__ == '__main__':
    # 4表示第四周，输入一个学期中间一点的周就行
    # 第二个参数传入None表示全部，传入某个字符串表示匹配
    cs = CourseSet.fromIteratorSearch(4, None, it=chain(wuLi(),  # 物院
                                                        shuXue(),  # 数院
                                                        yingCai(),  # 英才
                                                        gongKeShiYanBan()))  # 所有的“工科实验班”
    cs.course_table.to_pickle("all.pck")
```

之后我们可以直接读pickle文件，不勉强学校服务器。

```python
from hit_table_helper.course_set import CourseSet

if __name__ == '__main__':
    # 4表示第四周，输入一个学期中间一点的周就行
    # 第二个参数传入None表示全部，传入某个字符串表示匹配
    all = CourseSet.fromPickle("all.pck")
    I = CourseSet.fromPerson("我的学号")
    MyGirl = CourseSet.fromPerson("她的学号")

    all.filterFromMask(~I.mask & MyGirl.mask).toExcel("她有课我没课.xlsx")
```

这里`I.mask`是指你课表中已经占用的位置，取反表示没有占用的位置`MyGirl.mask`是指你的小姑娘的课表已经占用的位置

这样的话便得到了有一周中有哪些位置是你没课而她有课

`all.filterFromMask`这个代码就可以为你输出你没课她有课的数据表


```python
from hit_table_helper.course_set import CourseSet

if __name__ == '__main__':
    a = CourseSet.fromPerson("成员1")
    b = CourseSet.fromPerson("成员2")
    c = CourseSet.fromPerson("成员3") # 这里都替换成实际的学号
    
    print(~a.mask & ~b.mask & ~c.mask)
```

大创项目约时间找导师总是比较困难，这个代码可以为你输出你们三个人同时没有课的时间。

