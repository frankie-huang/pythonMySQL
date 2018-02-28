from pythonMySQL import *


class CRUD_DAO(object):
    def __init__(self, table_name, newConfig=0):
        self.cur_table = table_name
        self.dao = M(table_name, newConfig)

    def findById(self, primary_key_value):
        res = self.dao.find(primary_key_value)
        return res

    def addOne(self, data):
        id = self.dao.add(data)
        return id

    def save(self, data):
        '''
        根据id查找更新
        :param data:
        :return:
        '''
        res = self.dao.table(self.cur_table).save(data)  # 返回更新影响数或false
        return res

    def updateOneField(self, field_name, field_val, save_where={}):
        res = self.dao.table(self.cur_table).where(save_where).setField(field_name, field_val)  # 返回更新影响行数
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


class UserDAO(CRUD_DAO):
    def __init__(self, table_name, newConfig=0):
        super(UserDAO, self).__init__(table_name, newConfig)

    def findByName(self, name):
        where_param = {}
        where_param['name'] = ('eq', name, '', 'e')
        res = self.dao.where(where_param).select()
        return res


if __name__ == '__main__':
    userDao = UserDAO('t_user')
    res = userDao.findByName('jim')
    print(res)
    # poitype_dao = CRUD_DAO('poi_type')
    # res = poitype_dao.deleteById('02')
    # print(res)
    # data = {
    #     'code': '02',
    #     'name': '汽车服务',
    #     'name_en': 'Auto Service',
    #     'primary_code': '',
    #     'level': 1
    # }
    # res = poitype_dao.addOne(data)
    # print(res)
    # user_dao = CRUD_DAO('t_user')
    # data = {
    #     'name':'jim',
    #     'age':10
    # }
    # res = user_dao.addOne(data)
    # print(res)
    # data = {
    #     'name': 'tom',
    #     'age': 10
    # }
    # res = user_dao.addOne(data)
    # print(res)
    # res = user_dao.deleteById(3)
    # print(res)
    # res = user_dao.deleteByIds([9, 10])
    # print(res)
    # data = {
    #     'id': 11,
    #     'name': 'jim',
    #     'age': 100
    # }
    # res = user_dao.save(data)
    # print(res)
