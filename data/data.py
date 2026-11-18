from mysql.connector import connect,Error
from mysql.connector.pooling import MySQLConnectionPool
from config import *
class Card:
    def __init__(self):
        self.pool = None
        self.connect = None
        self.create_connection_pool()
    def create_connection_pool(self):
        try:
            # 创建数据库连接池
            self.pool = MySQLConnectionPool(
                pool_name='my_pool',
                pool_size=32,
                user='root',
                password='mysql_aFhhFx',
                host='172.18.0.5',
                database='hutui6'
            )
        except Error as err:
            print(f"create_connection_pool-Failed to create connection pool: {err}")
    def get_connection(self):
        try:
            # 从连接池获取数据库连接
            connection = self.pool.get_connection()
            if connection.is_connected():
                self.connect = connection
                return True
            else:
                return False
        except Error as err:
            print(f"Failed to get database connection: {err}")
            return False
    def close_connection(self):
        if self.connect:
            self.connect.close()
    def execute_query(self, query, data=None):
        try:
            self.get_connection()
            with self.connect.cursor() as cursor:
                cursor.execute(query, data)
                results = cursor.fetchall()
                return results
        except Error as err:
            print(f"execute_query-Failed to execute query: {err}")
            self.connect.rollback()
            return []
        finally:
            self.close_connection()
    def execute_update(self, query, data=None):
        try:
            self.get_connection()
            with self.connect.cursor() as cursor:
                cursor.execute(query, data)
                self.connect.commit()
            return True
        except Error as err:
            print(f"execute_update-Failed to execute update: {err}")
            self.connect.rollback()
            return False
        finally:
            self.close_connection()
    def select(self, query, data=None):
        return self.execute_query(query, data)
    def update(self, query, data=None):
        return self.execute_update(query, data)
    def insert(self, query, data=None):
        return self.execute_update(query, data)
    def delete(self, query, data=None):
        return self.execute_update(query, data)
db = Card()

class ChatUser:
    '''用户表操作类'''

    def __init__(self, Msg: Message = None):
        self.msg = Msg
    def get(self,from_user):
        '''查询用户'''
        user= db.select("SELECT * FROM chat_user WHERE chat_id=%s",(from_user.id,))
        if user:
            return user[0]
        return []
    def post(self,from_user):
        msg =self.msg
        full_name = f"{from_user.first_name or ''}{from_user.last_name or ''}"
        aad = "INSERT INTO chat_user (chat_id,username,full_name) " \
              "VALUES(%s,%s,%s)"
        data = (from_user.id, from_user.username or '无', full_name)
        if db.insert(aad, data):
            return self.get(from_user=from_user)
        return []
    def get_or_create(self,from_user):
        user = self.get(from_user=from_user)
        if user:
            return user
        else:
            return self.post(from_user=from_user)
class ConfigData:
    def get_config_list(self):
        data = db.select("SELECT * FROM config")
        if data:
            return data
        return []
    async def put_config(self,comm,name):
        data=db.update("UPDATE config SET comm=%s WHERE name=%s",(comm,name))
        return data
    async def get_rejectText_list(self):
        data = db.select("SELECT * FROM config WHERE name='rejectText'")
        if data:
            return data
        return []
    async def del_rejectText(self,id):
        data=db.delete("DELETE FROM config WHERE id=%s",(id,))
        return data
    async def post_rejectText(self,text):
        data = db.insert("INSERT INTO config (name,comm) VALUES(%s,%s)",('rejectText',text))
        return data
    async def put_rejectText(self,id,text):
        data = db.update("UPDATE config SET comm=%s WHERE id=%s AND name='rejectText'"
                         ,(text,id))
        return data

class AdvertisingData:
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    async def get_advertising_list(self):
        data = db.select("SELECT * FROM advertising")
        if data:
            return data
        return []
    async def del_advertising(self,id):
        data=db.delete("DELETE FROM advertising WHERE id=%s",(id,))
        return data
    async def post_advertising(self,titel,url):
        data = db.insert("INSERT INTO advertising (titel,url) VALUES(%s,%s)",(titel,url))
        return data
    async def put_advertising(self,id,titel,url):
        data = db.update("UPDATE advertising SET titel=%s,url=%s WHERE id=%s"
                         ,(titel,url,id))
        return data
class CarData:
    # 管理后台 车队管理Car类数据
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    async def get_fleet(self,**kwargs):
        LIMIT,OFFSET=kwargs.get('LIMIT'),kwargs.get('OFFSET')
        count = db.select("SELECT COUNT(*) FROM fleet_list WHERE fleet_type =0")
        data = db.select("SELECT fleet_list.*, COUNT(group_list.id) AS group_count FROM fleet_list "
                         "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state=2 "
                         "WHERE fleet_type = 0 GROUP BY fleet_list.id ORDER BY title LIMIT %s  OFFSET %s",(LIMIT,OFFSET) )
        if data:
            return data,count[0][0]
        return [],0
    async def get_fleet_group_list(self,id):
        group = db.select("SELECT * FROM group_list WHERE fleet_list=%s AND state=2",(id,))
        if group:
            return group
        return []
    async def get_fleet_one(self,id):
        fleet = db.select("SELECT fleet_list.*, COUNT(group_list.id) AS group_count "
                          "FROM fleet_list "
                          "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state = 2 "
                          "WHERE fleet_list.id = %s GROUP BY fleet_list.id",(id,))
        if fleet:
            return fleet[0]
        return []
    async def get_user_group_one(self,id):
        my_group = db.select("SELECT * FROM group_list WHERE id=%s",(id,))
        if my_group:
            return my_group[0]
        return []
    async def post_car(self,car_title,car_type):
        data = db.insert("INSERT INTO fleet_list (title,fleet_type) VALUES(%s,%s)",
                         (car_title, car_type))
        return data
    async def put_car_titel(self,id,text):
        data = db.update("UPDATE fleet_list SET title=%s WHERE id=%s",(text,id))
        return data
    async def put_car_introduce(self,id,text):
        data = db.update("UPDATE fleet_list SET introduce=%s WHERE id=%s",(text,id))
        return data
    async def put_car_total(self,id,text):
        data = db.update("UPDATE fleet_list SET total=%s WHERE id=%s",(text,id))
        return data
    async def put_car_mi_memberl(self,id,text):
        data = db.update("UPDATE fleet_list SET mi_member=%s WHERE id=%s",(text,id))
        return data
    async def put_car_mi_mi_read(self,id,text):
        data = db.update("UPDATE fleet_list SET mi_read=%s WHERE id=%s",(text,id))
        return data
    async def put_car_state(self,id,text):
        data = db.update("UPDATE fleet_list SET state=%s WHERE id=%s",(text,id))
        return data
    async def put_car_pass_review(self,group,state,label,url=None,):
        group_d = False
        if url:
            group_d= db.update("UPDATE group_list SET state=%s,url=%s,msg_id=0 WHERE id=%s",(state,url,group[0]))
        else:
            group_d= db.update("UPDATE group_list SET state=%s,msg_id=0 WHERE id=%s",(state,group[0]))
        if group_d:
            await self.post_notify_msg(group=group,label=label)
            return True
        return False
    async def post_notify_msg(self,group,label):
        notify = db.insert("INSERT INTO notify_msg (user_id,group_id,msg) VALUES(%s,%s,%s)",
                           (group[12], group[0], label))
        if notify:
            return True
        return False
    async def get_notify_msg(self,user=None,group=None):
        data = db.select("SELECT * FROM notify_msg WHERE group_id = %s AND user_id = %s ORDER BY id DESC LIMIT 1",
                         (group,user))
        if data:
            return data[0]
        return []
    async def get_user(self,id):
        user= db.select("SELECT * FROM chat_user WHERE id=%s",(id,))
        if user:
            return user[0]
        return []
    async def get_rejectText(self,id):
        data = db.select("SELECT * FROM config WHERE name='rejectText' AND id=%s",(id,))
        if data:
            return data[0]
        return []
class GroupData:
    # 管理后台Group 类数据
    async def get_group_list(self,**kwargs):
        LIMIT,OFFSET=kwargs.get('LIMIT'),kwargs.get('OFFSET')
        search=kwargs.get('search')
        if search:
            data = db.select(f"SELECT * FROM group_list WHERE title LIKE '%{search}%' ORDER BY id LIMIT %s  OFFSET %s", (LIMIT, OFFSET))
        else:
            data = db.select("SELECT * FROM group_list ORDER BY id LIMIT %s  OFFSET %s",(LIMIT,OFFSET) )
        if data:
            return data
        return []
    async def get_group_index_count(self,**kwargs):
        count = db.select("SELECT (SELECT COUNT(*) FROM group_list) AS total_count,"
                          "(SELECT COUNT(*) FROM group_list WHERE type='CHANNEL') AS CHANNEL_count,"
                          "(SELECT COUNT(*) FROM group_list WHERE type='CHANNEL' AND state=2) AS CHANNEL_state_count,"
                          "(SELECT COUNT(*) FROM group_list WHERE type='SUPERGROUP') AS SUPERGROUP_count,"
                          "(SELECT COUNT(*) FROM group_list WHERE type='SUPERGROUP' AND state=2) AS SUPERGROUP_state_count")
        if count:
            return count[0]
        return (0,0,0,0,0)
    async def get_group_info(self,id):
        data = db.select("SELECT * FROM group_list WHERE id=%s", (id,))
        if data:
            return data[0]
        return []

    async def get_fleet_one(self, id):
        fleet= db.select("SELECT * FROM fleet_list WHERE id=%s",(id,))
        if fleet:
            return fleet[0]
        return []
    async def get_user(self,id):
        user= db.select("SELECT * FROM chat_user WHERE id=%s",(id,))
        if user:
            return user[0]
        return []
class ChannelFleetList:
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    def get(self,**kwargs):
        data = db.select("SELECT * FROM fleet_list ORDER BY sign",)
        if data:
            return data
        return []
    def get_fleet(self,**kwargs):
        LIMIT,OFFSET=kwargs.get('LIMIT'),kwargs.get('OFFSET')
        count = db.select("SELECT COUNT(*) FROM fleet_list WHERE fleet_type =0")
        data = db.select("SELECT fleet_list.*, COUNT(group_list.id) AS group_count FROM fleet_list "
                         "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state=2 "
                         "WHERE fleet_type = 0 AND fleet_list.state=1 GROUP BY fleet_list.id ORDER BY title LIMIT %s  OFFSET %s",(LIMIT,OFFSET) )
        if data:
            return data,count[0][0]
        return [],0
    def get_group_count(self,**kwargs):
        count = db.select("SELECT COUNT(*) FROM group_list WHERE type='CHANNEL' AND state=2")
        if count:
            return count[0][0]
        return 0
    def get_fleet_one(self,id):
        fleet = db.select("SELECT fleet_list.*, COUNT(group_list.id) AS group_count "
                          "FROM fleet_list "
                          "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state = 2 "
                          "WHERE fleet_list.id = %s GROUP BY fleet_list.id",(id,))
        if fleet:
            return fleet[0]
        return []
    def get_fleet_group_list(self,id):
        group = db.select("SELECT * FROM group_list WHERE fleet_list=%s AND state=2",(id,))
        if group:
            return group
        return []
    async def get_user_group_list(self,id,member):
        my_group=db.select("SELECT * FROM group_list WHERE chat_id=%s AND type=%s AND total_people>=%s ",(id,"CHANNEL",member))
        if my_group:
            return my_group
        return []
    async def get_user_group_one(self,id):
        my_group = db.select("SELECT * FROM group_list WHERE id=%s",(id,))
        if my_group:
            return my_group[0]
        return []
    async def put_group_one(self,id,fieet):
        upData = db.update("UPDATE group_list SET state=1,fleet_list=%s,msg_id=0 WHERE id=%s",(fieet,id))
        if upData:
            return True
        return False
    async def get_admini_list(self):
        admin = db.select("SELECT * FROM chat_user WHERE admin IN (1,2)")
        if admin:
            return admin
        return []

class BotBlacklistDate:
    async def get_bot_blacklist_list(self):
        data = db.select("SELECT * FROM bot_blacklist")
        if data:
            return data
        return []
    async def del_bot_blacklist(self,id):
        data=db.delete("DELETE FROM bot_blacklist WHERE id=%s",(id,))
        return data
    async def post_bot_blacklist(self,titel):
        data = db.insert("INSERT INTO bot_blacklist (bot_name) VALUES(%s)",(titel,))
        return data
    async def put_bot_blacklist(self,id,titel):
        print(titel,id)
        data = db.update("UPDATE bot_blacklist SET bot_name=%s WHERE id=%s",(titel,id))
        return data