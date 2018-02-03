# pythonMySQL使用文档

---

## 写在前面
来源：将之前写的 [PHP操作MySQL类（2017.12.05版）][1] ，使用python重写。<br>
依赖：开发时使用的python3.6(理论上只要python3.x都可以)，需要mysql.connector模块（mysql-connector-python驱动）。
>mysql-connector-python驱动安装命令：<br>
`pip install mysql-connector-python --allow-external mysql-connector-python`<br>
如果上面的命令安装失败，可以试试另一个驱动：<br>
`pip install mysql-connector`

## 更新注记
### 2017.12.05更新

 - 将2017.12.05版的 [PHP操作MySQL类][1] 使用python重写而产生了这个东西

### 2018.01.05更新
 - 考完试把文档补上


## 使用文档
注：由于 [PHP操作MySQL类][1] 是根据ThinkPHP3.2.3“模型”部分的语法来仿写的，可结合ThinkPHP3.2.3的文档参考使用。（别当真，红红火火恍恍惚惚）
### 1.初始化
首先填好配置文件config.py，然后在代码文件import pythonMySQL：
```
from pythonMySQL import *
```
配置文件初始化
```
# 默认使用数据库默认配置信息，索引为0
link = M('users') # users表示默认对users数据表进行操作
# 使用配置文件中其他配置信息，比如声明了"otherConfig"键的配置信息
link = M('users', 'otherConfig')
```
字典参数初始化
```
dbConfig = {
    'host' : '127.0.0.1',
    'port' : '3306',
    'user' : 'root',
    'password' : 'password', # 如无，程序会使用配置文件声明的数据库密码
    'database' : 'db_name', # 必需
    'charset' : 'utf8',
    'autocommit' : True,
    'DB_DEBUG' : True,
}
# 此处的1为配置代号，支持字符串代号，之后可直接使用配置代号切换数据表
link = M('users', 1, dbConfig)
```
**推荐使用配置文件的方法**，支持的配置信息：
```
"host"       => '127.0.0.1', # 可选，服务器地址，默认127.0.0.1
"user"       => 'root',      # 可选，数据库用户名，默认root
'password'   => 'pwd',       # 必选，数据库密码
'database'   => 'db_name',   # 必选，数据库名
'port'       => '3306',      # 可选，端口号，默认3306
'dbms'       => 'mysql',     # 可选，数据库类型，默认mysql
'charset'    => 'utf8',      # 可选，数据库编码格式
'DB_DEBUG'   => True,        # 可选，是否开启DEBUG模式，请在系统上线后关闭DEBUG模式
'autocommit' => True         # 可选，开启自动提交事务
```

### 2.支持的连贯操作
#### 1.WHERE
##### 1.字符串条件
使用字符串条件直接查询和操作,例如:
```
User = M("User") # 实例化User对象
User.where('type=1 AND status=1').select()
```
最后生成的SQL语句是
```
SELECT * FROM think_user WHERE type=1 AND status=1
```
使用字符串条件的时候,建议配合预处理机制,确保更加安全,例如:
```
Model.where("id=%d and username='%s' and xx='%f'", id, username, xx)).select()
Model.where("id=%d and username='%s' and xx='%f'", (id, username, xx)).select()
Model.where("id=%d and username='%s' and xx='%f'", [id, username, xx]).select()
```

##### 2.字典条件
推荐用法。

支持普通查询
```
User = M("User") # 实例化User对象
map = {}
map['name'] = 'thinkphp'
map['status'] = 1
# 把查询条件传入查询方法
User.where(map).select()	
```
最后生成的SQL语句是
```
SELECT * FROM think_user WHERE `name`='thinkphp' AND status=1
```
支持[表达式查询](#expression)
```
map['字段1'] = ('表达式', '查询条件1', '逻辑符，可为空字符串，默认AND，或OR和XOR', 'e')
map['字段2'] = ('表达式', '查询条件2', '逻辑符，可为空字符串，默认AND，或OR和XOR', 'e')
Model.where(map).select()
```
支持多次调用。
#### 2.TABLE
除了数据表前缀，支持ThinkPHP支持的所有table用法。
**建议：在CURD链式调用放于首位。**
#### 3.ALIAS
支持ThinkPHP支持的所有alias用法。
#### 4.FIELD
用于查询
```
Model.field('id,title,content').select()
```
可以给某个字段设置别名，例如：
```
Model.field('id,nickname as name').select()
```
使用SQL函数
```
Model.field('id,SUM(score)').select()
```
使用字典参数，可以为某些字段定义别名
```
Model.field({'id':'','nickname':'name'}).select()
```
对于一些更复杂的字段要求，字典的优势则更加明显，例如：
```
Model.field({'id':'','concat(name,"-",id)':'truename','LEFT(title,7)':'sub_title'}).select()
```
执行的SQL相当于：
```
SELECT id,concat(name,"-",id) as truename,LEFT(title,7) as sub_title FROM table
```
支持获取所有字段和过滤字段(详见ThinkPHP3.2.3文档)。
#### 5.ORDER
用法与ThinkPHP相同
#### 6.LIMIT
用法与ThinkPHP相同
#### 7.PAGE
只支持两个数字参数的写法：
```
page(2,10)  # 表示单页量为10，取第二页，即取出符合条件的第11-20条数据
```
#### 8.GROUP
用法与ThinkPHP相同
#### 9.HAVING
用法与ThinkPHP相同
#### 10.JOIN
（跟ThinkPHP有较大区别）
只传一个字符串，默认INNER JOIN
```
M('t1').join('t2 on t1.id=t2.id').select()
# 相当于select * from t1 INNER JOIN t2 on t1.id=t2.id
```
传数组（list或tuple）
（前两个元素必须是字符串，第二个元素须是"INNER","LEFT","RIGHT","FULL"之一）
```
M('t1').join(('t2 on t1.id=t2.id', 'LEFT')).select()
# 相当于select * from t1 LEFT JOIN t2 on t1.id=t2.id
```
支持多次调用。
>注：MySQL其实不支持FULL JOIN，建议用 left join + union(可去除重复数据)+ right join 作为替代方案。
#### 11.fetchSql
用法与ThinkPHP相同
### 3.支持的CURD操作（增删查改）
失败都返回False，可调用成员函数`showError()`打印SQL错误信息。
#### 1.数据读取
##### find()
读取数据（仅一条）
```
data = User.where('status=1 AND name="thinkphp"').find()
```
查询成功返回字典，如果无数据返回None
##### select()
读取数据集
```
list = User.where('status=1').order('create_time').limit(10).select()
```
查询成功返回由字典组成的列表，如果无数据返回空列表
#### 2.数据插入
##### add()
传入字典
```
User = M("User") # 实例化User对象
data = {}
data['name'] = 'ThinkPHP'
data['email'] = 'ThinkPHP@gmail.com'
User.add(data)
```
插入成功返回插入数据的ID/lastID（如果无ID将返回0）
##### addAll()
批量写入（须传入由字典组成的列表或元组）
```
dataList = [
    {'name':'thinkphp','email':'thinkphp@gamil.com'},
    {'name':'onethink','email':'onethink@gamil.com'}
]
User.addAll(dataList)
```
插入成功返回其中第一条插入数据的ID（如果无ID将返回0）
#### 3.数据更新
返回值都是影响的记录数（如果更新前的数据和更新后的没有变化，则返回0）
##### save()
```
User = M("User") # 实例化User对象
data = {}
# 要修改的数据对象属性赋值
data['name'] = 'ThinkPHP'
data['email'] = 'ThinkPHP@gmail.com'
User.where('id=5').save(data) # 根据条件更新记录
```
为了保证数据库的安全，避免出错更新整个数据表，如果没有任何更新条件，数据对象本身也不包含主键字段的话，save方法不会更新任何数据库的记录。
除非使用下面的方式：
```
User = M("User") # 实例化User对象
data = {}
# 要修改的数据对象属性赋值
data['id'] = 5
data['name'] = 'ThinkPHP'
data['email'] = 'ThinkPHP@gmail.com'
User.save(data) # 根据条件保存修改的数据
```
如果id是数据表的主键的话，系统自动会把主键的值作为更新条件来更新其他字段的值
##### setField()
如果只是更新个别字段的值，可以使用setField 方法：
```
User = M("User") # 实例化User对象
# 更改用户的name值
User.where('id=5').setField('name','ThinkPHP')
```
setField方法支持同时更新多个字段，只需要传入字典即可(这将与save相同)
```
User = M("User") # 实例化User对象
# 更改用户的name和email的值
data = {'name':'ThinkPHP','email':'ThinkPHP@gmail.com'}
User.where('id=5').setField(data)
```
而对于统计字段（通常指的是数字类型）的更新，还提供了setInc 和setDec 方法。
```
User = M("User") # 实例化User对象
User.where('id=5').setInc('score',3) # 用户的积分加3
User.where('id=5').setInc('score') # 用户的积分加1
User.where('id=5').setDec('score',5) # 用户的积分减5
User.where('id=5').setDec('score') # 用户的积分减1
```
不支持延迟更新。
#### 4.数据删除
返回是删除的记录数

不支持传入主键删除数据（与ThinkPHP有区别）

普通用法：
```
User.where('status=0').delete() # 删除所有状态为0的用户数据
```
高级用法，delete与join的结合使用：
```
User=M('t1')
User.join('t2 on t2.id = t1.id').delete('t1')
# DELETE t1 FROM `t1` INNER JOIN t2 on t2.id = t1.id
# 表示删除t1表中id与t2的id相同的数据
# delete方法中的参数用于指定删除哪个表中符合条件的数据
```
### 4.查询语言
与ThinkPHP最大的不同在于使用了"s""m""e"关键词：
>**"s"**：进行单条件对应查询，示例：<br>
`map['status&title'] =('1','thinkphp')`或者`map['status&title'] =('1','thinkphp','','s')`<br>
即`status=1 AND title='thinkphp'`<br/>
**"m"**：单字段进行多条件查询，示例：<br>
`map['name'] = ('ThinkPHP',('like','%a%','','e'),'or','m')`<br>
即`name='ThinkPHP' OR name LIKE '%a%'`

其中"m"和"e"关键词主要是为了与表达式查询做区分。
>举个例子：
`map['name'] = ('ThinkPHP','is null')`和`map['name'] = ('exp','is null')`
后者本来是表达式查询，但是还可以被辨别为`name='exp' AND name='is null'`；
所以干脆给前者加个`"m"`表示非表达式查询，解析为`name='ThinkPHP' AND name='is null'`。
后者没有"m"关键词，解析为`name is null`。

#### 1.查询方法
支持字符串查询和字典查询。
以及**推荐使用字典查询**，因为where查询直接传字符串不做任何检查（不安全所以不支持）

<h4 id="expression">2.表达式查询</h4>
`('表达式', '查询条件', '逻辑符', 'e')`

参数解释：
>表达式：EQ、NEQ、GT、LIKE、BETWEEN、IN、EXP等，详见ThinkPHP文档<br>
查询条件：接在表达式后面，比如`EQ 1`或`LIKE "%s%"`，则应将 1 或 "%s%" 填入此参数位置<br>
逻辑符：此参数在表达式查询中无意义，仅作占位用（因须与多条件查询对应），所以其实此处填什么都无所谓<br>
'e'：此处用于标识这是表达式查询

示例：
```
# name LIKE '%ank%'
map['name'] = ('like', '%ank%', '', 'e')
```

#### 3.快捷查询
需要用's'或'm'标识单字段对应查询或是单字段对应多条件查询，如无，默认's'

单字段对应查询
```
# status=1 AND title='thinkphp'
map['status&title'] =('1','thinkphp')
map['status&title'] =('1','thinkphp','','s')
```
单字段对应多条件查询
```
# (status=1 AND status='thinkphp') AND (title=1 AND title='thinkphp')
map['status&title'] =('1','thinkphp','','m')
# (status=1 AND status='thinkphp') OR (title=1 AND title='thinkphp')
map['status&title'] =('1','thinkphp','or','m')
```
#### 4.区间查询
文档原文：
>区间查询的条件可以支持普通查询的所有表达式，也就是说类似LIKE、GT和EXP这样的表达式都可以支
持。另外区间查询还可以支持更多的条件，只要是针对一个字段的条件都可以写到一起，例如：
`map['name'] = array(array('like','%a%'), array('like','%b%'), array('like','%c%'), 'ThinkPHP','or');`

这里的写法：
```
map['name'] = (('like','%a%','','e'), ('like','%b%','','e'), ('like','%c%','','e'), 'ThinkPHP','or','m')
```
最后的查询条件是：
```
( name LIKE '%a%') OR ( name LIKE '%b%') OR ( name LIKE '%c%') OR ( name = 'ThinkPHP')
```

#### 5.组合查询
字符串模式查询：
`map['_string'] = 'status=1 AND score>10'`
请求字符串查询方式：
`map['_query'] = 'status=1&score=100&_logic=or'`

复合查询（复合查询相当于封装了一个新的查询条件，然后并入原来的查询条件之中，所以可以完成比较复杂的查询条件组装）：
```
# (`id` > 5 OR `status` <> 0 ) AND `subject` = 2
main = {}
submain = {}
submain['id'] = ('gt', 5, '', 'e')
submain['status'] = ('neq', 0, '', 'e')
submain['_logic'] = 'or'
main['_complex'] = submain
main['subject'] = 2
```

#### 6.统计查询
`Count` `Max` `Min` `Avg` `Sum`<br>
获取用户数：<br>
`userCount = User.count()`<br>
或者根据字段统计：<br>
`userCount = User.count("id")`<br>
获取用户的最大积分：<br>
`maxScore = User.max('score')`<br>
获取积分大于0的用户的最小积分：<br>
`minScore = User.where('score>0').min('score')`<br>
获取用户的平均积分：<br>
`avgScore = User.avg('score')`<br>
统计用户的总成绩：<br>
`sumScore = User.sum('score')`<br>
并且所有的统计查询均支持连贯操作的使用。
#### 7.SQL查询
原生的SQL查询和执行操作支持。

QUERY方法（返回查询结果数据集）：<br>
`Model.query("select * from think_user where status=1")`<br>
EXECUTE方法（返回影响的记录数）：<br>
`Model.execute("update think_user set name='thinkPHP' where status=1")`

#### 8.动态查询
不支持动态查询（感觉没什么必要）

#### 9.子查询
1.使用select方法 当select方法的参数为False的时候，表示不进行查询只是返回构建SQL，例如：
```
# 首先构造子查询SQL
subQuery = Model.field('id,name').table('tablename').where(where).select(False)
```
2.使用buildSql方法
```
subQuery = Model.field('id,name').table('tablename').where(where).buildSql()
```
调用buildSql方法后不会进行实际的查询操作，而只是生成该次查询的SQL语句（为了避免混淆，会在SQL两边加上括号），然后直接在后续的查询中直接调用。
```
# 利用子查询进行查询
Model.table(subQuery + ' AS a').join('t on t.id = a.id').select()
```
### 5.事务驱动
**仅对支持事务的数据库驱动起作用。**

 1. 开启事务/startTrans
 2. 检查是否在一个事务内/inTrans
 3. 事务回滚/rollback
 4. 事务提交/commit

使用示例：
```
link = M("test")
print(link.inTrans()) # 输出False
link.startTrans()
print(link.inTrans()) # 输出True
link.where('id=4').save({'status':('exp','status+100','','e')})
link.rollback() # 事务回滚，事务内的更新无效
print(link.inTrans()) # 输出False
link.where('id=5').save({'status':('exp','status+100','','e')}) # 处于事务外，更新立即生效
```

### 6.其他
#### 1.M函数
用于初始化对一个数据表的连接。
```
# 连接users数据表，如无table方法切换数据表，默认对此表进行操作。
link = M("users")
```
#### 2.(TO DO) I函数
暂时只支持get和post（需要再说）
使用htmlspecialchars()对数据进行预处理
#### 3.(TO DO) get_client_ip()
获取客户端IP地址
#### 4.getLastSql() / _sql()
`getLastSql()`和`_sql()`等效，用于打印最后一条执行的**SQL语句**

其中，当且仅当DEBUG模式开启，以上方法才会输出详细信息。
#### 5.showError()
当SQL语句执行出错时可调用`showError()`打印详细的错误信息；

当然，也可以通过类成员变量`SQLerror`（字典，有如下的key）自行取错误信息：
>errno：error number<br/>
sqlstate：SQLSTATE value<br/>
msg：error message<br/>
sql：发生错误的SQL语句

其中，当且仅当DEBUG模式开启，以上方法才会输出详细信息。
#### 6.(TO DO) html_encode()和html_decode()
PHP的html解码/解码函数

## TO DO list
 - field之字段过滤目前仅支持单表查询

## Github永久更新地址
[frankie-huang/pythonMySQL][2]

## PHP版
[PDO_MYSQL_MODEL][1]

## 参考链接
[ThinkPHP3.2.3完全开发手册在线文档][3]


  [1]: https://github.com/frankie-huang/PDO_MYSQL_MODEL
  [2]: https://github.com/frankie-huang/pythonMySQL
  [3]: https://www.kancloud.cn/manual/thinkphp/1678