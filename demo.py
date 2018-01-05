from pythonMySQL import *

# 以下仅为使用示例 

# 配置文件初始化
test = M('users')

# 字典参数初始化
dbConfig = {
    'host' : '127.0.0.1',
    'port' : '3306',
    'user' : 'root',
    'password' : 'password', # 如无，程序会使用配置文件声明的数据库密码
    'database' : 'blog', # 必需
    'charset' : 'utf8',
    'autocommit' : True,
    'DB_DEBUG' : True,
}
test = M('users', 'newConfig', dbConfig)

# 如果需要此配置（上面的dbConfig配置）切换数据表，既可以使用test.table('other_table')，也可以如下使用
other_table = M('other_table', 'newConfig')


## 1. select

# SELECT * FROM `users` WHERE ( ( `degree` = -1 AND `teacher` = 'who' ) OR `id` > 5 OR `status` <> 0 ) AND `subject` = 2 AND `chapter` >= 7
main = {}
submain = {}
subsubmain = {}
subsubmain['degree'] = -1
subsubmain['teacher'] = 'who'
submain['_complex'] = subsubmain
submain['id'] = ('gt', 5, '', 'e')
submain['status'] = ('neq', 0, '', 'e')
submain['_logic'] = 'or'
main['_complex'] = submain
main['subject'] = 2
main['chapter'] = ('egt', 7, '', 'e')
res = test.where(main).select() # 返回得到的字典列表 否则为None

# SELECT fills.id,users.id AS `id_users`,concat(name,'-',id) AS `truename`,LEFT(title,7) AS `sub_title` FROM fills,chat.users
field = {
    'fills.id' : '',
    'users.id' : 'id_users',
    "concat(name,'-',id)" : 'truename',
    'LEFT(title,7)' : 'sub_title'
}
res = test.table('fills,chat.users').field(field).select() # 返回由字典组成的列表 或 None


## 2. find

# SELECT * FROM `fills` WHERE `id` = '4' LIMIT 1
res = test.find(4) # 返回字典 或 None


## 3. add

# INSERT INTO `users` (`email`,`username`,`password`,`sex`,`head`) VALUES ('frankie@qq.com','frankie','root','1','head.jpg')
data = {
    'email':'frankie@qq.com',
    'username':'frankie',
    'password':'root',
    'sex':"1",
    'head':'head.jpg'
}
res = test.add(data) # 返回lastID


## 4. save

# UPDATE users SET `nick` = 'frankie123',`school` = 'scut' WHERE `u_id` = 'abcd1234'
data = {}
data['u_id']='abcd1234';
data['nick']='frankie123';
data['school']='scut';
res = test.table('users').save(data) # 返回更新影响数或false


## 5. setField

# UPDATE users SET `username` = 'test' WHERE `u_id` = 5
save_where = {}
save_where['u_id'] = 5
res = test.table('users').where(save_where).setField('username','test') # 返回更新影响行数


## 6. delete

## DELETE FROM `users` WHERE ( u_id = 6 )
res = test.where('u_id = 6').delete() # 返回删除的行数

# DELETE t2 FROM users as t1 INNER JOIN chat.users as t2 on t1.user_id = t2.user_id
res = test.table('users as t1').join('chat.users as t2 on t1.user_id = t2.user_id').delete('t2')


## 7. 打印当前模型执行的最后一条SQL语句
print(test.getLastSql()) # 打印由Model类拼接填充生成的SQL语句
print(test._sql()) # 打印数据库系统实际执行的SQL语句


## 8. 事务驱动
test.startTrans() # 开启事务
test.inTrans() # 判断事务处于事务中，是则返回True
test.where('u_id=1').delete()
if something == True:
    test.commit()
else:
    test.rollback()
