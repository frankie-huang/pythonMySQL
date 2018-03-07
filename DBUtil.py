from pythonMySQL import *


class CRUD_DAO(object):
    def __init__(self, table_name, newConfig=0):
        self.cur_table = table_name
        self.dao = M(table_name, newConfig)

    def findById(self, primary_key_value):
        res = self.dao.find(primary_key_value)
        return res

    def addOne(self, data):
        id = self.dao.add(data)  # 返回lastID,如果pk 为字符串，返回0
        return id

    def saveById(self, data):
        '''
        根据pk查找更新,pk为空，报错
        :param data:
        :return:
        '''
        res = self.dao.table(self.cur_table).save(data)  # 返回更新影响数或false
        return res

    def updateOneField(self, field_name, field_val, save_where={}):
        res = self.dao.table(self.cur_table).where(save_where).setField(field_name, field_val)  # 返回更新影响行数
        return res

    def updateFields(self, f_v_dict, save_where={}):
        res = self.dao.table(self.cur_table).where(save_where).setField(f_v_dict)  # 返回更新影响行数
        return res

    def deleteById(self, primary_key_value):
        res = self.dao.deleteById(primary_key_value)
        return res

    def deleteByIds(self, primary_key_values):
        where_param = {}
        self.dao.set_columns(self.cur_table)
        primary_col = self.dao.columns[0]
        where_param[primary_col] = ('in', primary_key_values, '', 'e')
        res = self.dao.where(where_param).delete()
        return res

    def printDebugSql(self):
        print(self.dao.getLastSql())

    def printSql(self):
        print(self.dao._sql())




class UserDAO(CRUD_DAO):
    def __init__(self, table_name='t_user', newConfig=0):
        super(UserDAO, self).__init__(table_name, newConfig)

    def findByName(self, name):
        where_param = {}
        where_param['name'] = ('eq', name, '', 'e')
        res = self.dao.where(where_param).select()
        return res

    def findDetailinfoById(self, id):
        '''
        内连接,
        :param id:
        :return:
        '''
        field = {
            'a.id': '',
            'a.name': 'name',
            'a.age': 'age',
            'b.nickname': 'nickname',
            'b.lastlogintime': 'lastlogintime'
        }
        where_param = {}
        where_param['a.id'] = id
        res = self.dao.table('t_user as a,chat_user as b').field(field).where('a.id = b.id').where(where_param).select()
        return res

'''
user表
CREATE TABLE t_user(
id int(20) AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) not null ,
age int(3)
)ENGINE = INNODB DEFAULT CHARSET=utf8

chat表
CREATE TABLE chat_users (
id INT(20) AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) not null ,
nickname VARCHAR(50) not null,
lastlogintie datetime
)ENGINE = INNODB DEFAULT CHARSET=utf8

'''

if __name__ == '__main__':
    userDao = UserDAO()
    # userDao = UserDAO('t_user') 封装UserDao后
    '''
    findbyName
    return userlist
    '''
    res = userDao.findByName('jim')
    print(res)

    '''
    与chat表关联查询
    return list
    '''
    res = userDao.findDetailinfoById(11)
    userDao.printDebugSql()
    print('the result is: ',res)

    '''
    插入一条
    :return id
    '''
    data = {
        'name':'jim',
        'age':10
    }
    res = userDao.addOne(data)
    print(res)

    '''
    根据id列表删除对应数据
    :return 影响条数
    '''
    res = userDao.deleteByIds([9, 10])
    print(res)

    '''
    根据id，更新数据
    :return 影响条数
    '''
    data = {
        'id': 11,
        'name': 'jim',
        'age': 100
    }
    res = userDao.save(data)
    print(res)