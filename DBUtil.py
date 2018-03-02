from pythonMySQL import *
import csv


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


class PoiTypeDAO(CRUD_DAO):
    def __init__(self, table_name, newConfig=0):
        super(PoiTypeDAO, self).__init__(table_name, newConfig)

    def findAllPoitype(self):
        where_param = {}
        where_param['level'] = 3
        res = self.dao.where(where_param).select()
        return res


if __name__ == '__main__':
    userDao = UserDAO()
    res = userDao.findDetailinfoById(11)
    userDao.printDebugSql()
    print(res)
    # poitypeDao = PoiTypeDAO('poi_type')
    # res = poitypeDao.findById('01')
    # poitypeDao.printDebugSql()
    # poitypeDao.printSql()
    # print(len(res))
    # f = r'D:\work\03\poitype\poitype1.csv'
    # inlist = []
    # with open(f, newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for e in reader:
    #         inlist.append(e)
    #     csvfile.close()
    # print(len(inlist))
    # for e in inlist:
    #     poitypeDao.addOne(e)
    # userDao = UserDAO('t_user')
    # res = userDao.findByName('jim')
    # print(res)
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
