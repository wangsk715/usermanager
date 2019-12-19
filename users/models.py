#encoding: utf-8
import json
from django.db import models
import MySQLdb
# Create your models here.

#导入数据
data_user = "user.data.json"
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'redhat'
MYSQL_DB = 'cmdb'
CHARSET = 'utf8'
# conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='redhat', db='cmdb',charset='utf8')
# daya_user = conn.cursor()
sql_login = "select id,name,age,sex,tel from users where name=%s and password=%s limit 1;"
sql_list = '''
            select id,name,age,sex,tel
            from users;
            '''
sql_delete = '''
                delete from users where id=%s;
            '''
sql_update = '''
            select id,name,sex,age,tel
            from users
            where id=%s;
    '''
def get_users():
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB, charset=CHARSET)
    cur = conn.cursor()
    print(cur)
    cur.execute(sql_list)
    resutl = cur.fetchall()
    print(resutl)
    cur.close()
    conn.close()
    return [{'id': line[0], 'name':line[1], 'sex':line[2], 'age':line[3], 'tel':line[4]} for line in resutl]

def get_user(uid):
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,
                           charset=CHARSET)
    cur = conn.cursor()
    print(cur)
    cur.execute(sql_update, (uid))
    resutl = cur.fetchall()
    print(resutl)
    cur.close()
    conn.close()
    return [{'id': line[0], 'name': line[1], 'sex': line[2], 'age': line[3], 'tel': line[4]} for line in resutl]

def users_dump(users):
    with open(data_user, 'wt') as f:
        f.write(json.dumps(users))
    return True



def vaild_login(username, passwd):
    conn = MySQLdb.connect(host= MYSQL_HOST, port = MYSQL_PORT, user = MYSQL_USER, passwd = MYSQL_PASSWD, db = MYSQL_DB, charset = CHARSET)
    print("查询成功")
    cur = conn.cursor()
    print(cur)
    print('test')
    cur.execute(sql_login,(username, passwd))
    resutl = cur.fetchone()
    cur.close()
    conn.close()
    return {"id": resutl[0], 'name': resutl[0]}  if resutl else None

def delete_user(uid):
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,charset=CHARSET)
    print("查询成功")
    cur = conn.cursor()
    print(cur)
    print('test')
    cur.execute(sql_delete, (uid))
    conn.commit()
    cur.close()
    conn.close()

    return True

def vaild_update_user(params):
    uid = params.get('id', '')
    name = params.get('name', '')
    age = params.get('age', '')
    sex = params.get('sex', '')
    tel = params.get('tel', '')


    is_valid = True
    user = {}  #{id,name,age,sex,tel}
    errors = {}
    users = get_users()

    #判断用户id是否存在
    user['id'] = uid.strip()
    if users.get(user['id']) is None:
        errors['id'] = '输入用户信息不存在'
        is_valid = False

    user['name'] = name
    for id, cname in users.items():
        if cname['name'] == user['name'] and id != user['id']:
            errors['name'] = "用户名存在"
            is_valid = False

    user['age'] = age
    if not user['age'].isdigit():
        errors['age'] = "年龄格式错误"
        is_valid = False

    user['tel'] = tel
    if not user['tel'].isdigit():
        errors['tel'] = '电话格式错误'
        is_valid  = False

    user['sex']  = sex


    return is_valid, user, errors


def update_user(user):
    uid = user.pop('id') #获取id的值
    users = get_users()
    users[uid].update(user)
    return users_dump(users)

def get_user_data(params):

        name = params.get('name', '')
        age = params.get('age', '')
        sex = params.get('sex', '')
        tel = params.get('tel', '')
        password = params.get('password', '')

        is_valid = True
        user = {}  # {id,name,age,sex,tel}
        errors = {}
        users = get_users()


        user['name'] = name
        print(user)
        for id, cname in users.items():
            if cname['name'] == user['name'] :
                errors['name'] = "用户名存在"
                is_valid = False

        user['age'] = age
        if not user['age'].isdigit():
            errors['age'] = "年龄格式错误"
            is_valid = False

        user['tel'] = tel
        if not user['tel'].isdigit():
            errors['tel'] = '电话格式错误'
            is_valid = False

        user['sex'] = sex
        user['password'] = password
        print(user)
        return is_valid, errors, user

def add_user(user):
    users = get_users()
    max = 0
    for k,v in users.items():
        if int(k) > max:
            max = int(k)
    print(user)

    users[max + 1] = user

    return users_dump(users)

def passwd(uid, pd):
    users = get_users()

    for k, value in users.items():
        if k == uid:
            value['password'] = pd

    users_dump(users)
    return True

if __name__ == '__main__':
    get_user()