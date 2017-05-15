import psycopg2 as pg


def get_connection():
    try:
        conn = pg.connect(
            database='umnsntob',
            user='umnsntob',
            password='H7mI1xL-pv2MqfDsJNOG4SVDgxkRJJYq',
            host='stampy.db.elephantsql.com',
            port=5432)
        return conn
    except Exception as e:
        raise e


def create_db():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            '''CREATE TABLE rec (
            ID  SERIAL PRIMARY KEY,
            USERID     TEXT   REFERENCES user_rec(USERID)  NOT Null,
            messages   TEXT
            );'''
        )
        connection.commit()
        connection.close()
    except Exception as error:
        return error


def post_messages(USER, MESSAGES):
    connection = get_connection()
    cursor = connection.cursor()
    query = """INSERT INTO rec(USERID,MESSAGES) VALUES('%s', '%s');"""
    query = query % (
        USER, MESSAGES)
    cursor.execute(query)
    connection.commit()
    connection.close()


def process_create_user(USER, NAME, ROLE, EMAIL, PASSWORD):
    BLOCK = False
    connection = get_connection()
    cursor = connection.cursor()
    query = """INSERT INTO user_rec(
    USERID,NAME,ROLE,BLOCK,EMAIL,PASSWORD,COUNT
    ) VALUES('%s', '%s', '%s', '%s', '%s', '%s', 0);"""
    query = query % (
        USER, NAME, ROLE, BLOCK, EMAIL, PASSWORD)
    cursor.execute(query)
    connection.commit()
    connection.close()


def create_user(USER, NAME, ROLE, EMAIL, PASSWORD):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid from user_rec where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    try:
        if len(rows) == 0:
            process_create_user(USER, NAME, ROLE, EMAIL, PASSWORD)
        else:
            return 1
    except Exception as error:
        return error
    connection.close()


def message_show():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT * from rec;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
    connection.close()


def users():
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid, name, email, role, block from user_rec;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
    connection.close()


def message_delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = """DELETE FROM rec WHERE ID = %s;"""
    query = query % id
    cursor.execute(query)
    connection.commit()
    connection.close()
    return "Deleted"


def block(block, userid):
    connection = get_connection()
    cursor = connection.cursor()
    query = """UPDATE user_rec SET block = '%s' WHERE userid = '%s';"""
    query = query % (block, userid)
    cursor.execute(query)
    connection.commit()
    connection.close()
    return "DONE"


def update(role, userid, password, email, name):
    connection = get_connection()
    cursor = connection.cursor()
    if role and userid and password and email and name:
        query = """UPDATE user_rec SET role = '%s', name = '%s', password = '%s', email = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, name, password, email, userid)
    elif userid and role:
        query = """UPDATE user_rec SET role = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, userid)
    elif userid and password:
        query = """UPDATE user_rec SET password = '%s' WHERE userid = '%s';""" # noqa
        query = query % (password, userid)
    elif userid and email:
        query = """UPDATE user_rec SET email = '%s' WHERE userid = '%s';""" # noqa
        query = query % (email, userid)
    elif userid and name:
        query = """UPDATE user_rec SET role = '%s', name = '%s' WHERE userid = '%s';""" # noqa
        query = query % (name, userid)
    elif userid and role and password:
        query = """UPDATE user_rec SET role = '%s', password = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, password, userid)
    elif userid and role and email:
        query = """UPDATE user_rec SET role = '%s', email = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, email, userid)
    elif userid and role and name:
        query = """UPDATE user_rec SET role = '%s', name = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, name, userid)
    elif role and userid and password and email:
        query = """UPDATE user_rec SET role = '%s', password = '%s', email = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, password, email, userid)
    elif role and userid and password and name:
        query = """UPDATE user_rec SET role = '%s', name = '%s', password = '%s' WHERE userid = '%s';""" # noqa
        query = query % (role, name, password, userid)
    else:
        return 0
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
        return 1
    except Exception as error:
        raise error


def get_info(userid):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT userid, name, email, role, block from user_rec where userid = '%s';"""  # noqa
    query = query % userid
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
    connection.close()


def count_show(userid):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT count from user_rec where userid = '%s';"""
    query = query % userid
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
    connection.close()


def count_add(userid, count):
    connection = get_connection()
    cursor = connection.cursor()
    query = """UPDATE user_rec SET count = '%s' WHERE userid = '%s';"""
    query = query % (count, userid)
    cursor.execute(query)
    connection.commit()
    connection.close()
    return 'done'
