import aiosqlite
from config import *


class Card:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as conn:
                await conn.execute("PRAGMA journal_mode=WAL")
                await conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS advertising (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titel TEXT DEFAULT NULL,
                        url TEXT DEFAULT NULL,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS bot_blacklist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bot_name TEXT DEFAULT NULL,
                        state INTEGER DEFAULT 0,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS chat_user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id TEXT DEFAULT NULL,
                        username TEXT DEFAULT NULL,
                        full_name TEXT DEFAULT NULL,
                        state INTEGER DEFAULT 0,
                        admin INTEGER DEFAULT 0,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT DEFAULT NULL,
                        comm TEXT DEFAULT NULL
                    );
                    CREATE TABLE IF NOT EXISTS fleet_list (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT DEFAULT NULL,
                        introduce TEXT DEFAULT NULL,
                        fleet_type INTEGER DEFAULT 0,
                        state INTEGER DEFAULT 0,
                        sign TEXT DEFAULT NULL,
                        total INTEGER DEFAULT 20,
                        count INTEGER DEFAULT 1,
                        mi_member INTEGER DEFAULT 1,
                        mi_read INTEGER DEFAULT 1,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS group_list (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_id TEXT DEFAULT NULL,
                        username TEXT DEFAULT NULL,
                        title TEXT DEFAULT NULL,
                        type TEXT DEFAULT NULL,
                        total_people INTEGER DEFAULT NULL,
                        url TEXT DEFAULT NULL,
                        msg_id INTEGER DEFAULT 0,
                        out_fan INTEGER DEFAULT 0,
                        input_fan INTEGER DEFAULT 0,
                        state INTEGER DEFAULT 0,
                        fleet_list INTEGER DEFAULT 0,
                        chat_id INTEGER DEFAULT NULL,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS notify_msg (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER DEFAULT NULL,
                        group_id INTEGER DEFAULT NULL,
                        msg TEXT DEFAULT NULL,
                        creation_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
                async with conn.execute("SELECT COUNT(*) FROM config") as cursor:
                    row = await cursor.fetchone()
                if row and row[0] == 0:
                    await conn.executemany(
                        "INSERT INTO config (name, comm) VALUES (?, ?)",
                        [
                            ("botName", "Бот взаимопиара"),
                            ("botUserName", "@GetTandem_bot"),
                            ("indexTxt", "Добро пожаловать в бота взаимопиара"),
                            ("adminGroup", "1"),
                            ("publicGroup", "Не указан"),
                            ("msgGroup", "-"),
                            ("video", ""),
                            ("restrict_limit", "30"),
                            ("notifyType", "0"),
                            ("rejectText", "В этой подборке больше нет мест, подайте заявку в другую"),
                            ("rejectText", "Недостаточно активности"),
                            ("rejectText", "Низкое качество контента"),
                            ("rejectText", "Недостаточно просмотров"),
                        ],
                    )
                await conn.commit()
        except aiosqlite.Error as err:
            print(f"init_db-Ошибка инициализации базы данных: {err}")

    async def execute_query(self, query, data=()):
        try:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as conn:
                async with conn.execute(query, data or ()) as cursor:
                    results = await cursor.fetchall()
                    return results
        except aiosqlite.Error as err:
            print(f"execute_query-Ошибка выполнения запроса: {err}")
            return []

    async def execute_update(self, query, data=()):
        try:
            async with aiosqlite.connect(self.db_path, timeout=30.0) as conn:
                await conn.execute(query, data or ())
                await conn.commit()
                return True
        except aiosqlite.Error as err:
            print(f"execute_update-Ошибка обновления данных: {err}")
            return False

    async def select(self, query, data=()):
        return await self.execute_query(query, data)

    async def update(self, query, data=()):
        return await self.execute_update(query, data)

    async def insert(self, query, data=()):
        return await self.execute_update(query, data)

    async def delete(self, query, data=()):
        return await self.execute_update(query, data)


db = Card()


class ChatUser:
    '''Класс для работы с таблицей пользователей'''

    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def get(self, from_user):
        '''Поиск пользователя'''
        user = await db.select("SELECT * FROM chat_user WHERE chat_id=?", (str(from_user.id),))
        if user:
            return user[0]
        return []

    async def post(self, from_user):
        full_name = f"{from_user.first_name or ''}{from_user.last_name or ''}"
        aad = "INSERT INTO chat_user (chat_id,username,full_name) VALUES(?,?,?)"
        data = (str(from_user.id), from_user.username or 'Нет', full_name)
        if await db.insert(aad, data):
            return await self.get(from_user=from_user)
        return []

    async def get_or_create(self, from_user):
        user = await self.get(from_user=from_user)
        if user:
            return user
        return await self.post(from_user=from_user)


class ConfigData:
    async def get_config_list(self):
        data = await db.select("SELECT * FROM config")
        if data:
            return data
        return []

    async def put_config(self, comm, name):
        return await db.update("UPDATE config SET comm=? WHERE name=?", (comm, name))

    async def get_rejectText_list(self):
        data = await db.select("SELECT * FROM config WHERE name='rejectText'")
        if data:
            return data
        return []

    async def del_rejectText(self, id):
        return await db.delete("DELETE FROM config WHERE id=?", (id,))

    async def post_rejectText(self, text):
        return await db.insert("INSERT INTO config (name,comm) VALUES(?,?)", ('rejectText', text))

    async def put_rejectText(self, id, text):
        return await db.update("UPDATE config SET comm=? WHERE id=? AND name='rejectText'", (text, id))


class AdvertisingData:
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def get_advertising_list(self):
        data = await db.select("SELECT * FROM advertising")
        if data:
            return data
        return []

    async def del_advertising(self, id):
        return await db.delete("DELETE FROM advertising WHERE id=?", (id,))

    async def post_advertising(self, titel, url):
        return await db.insert("INSERT INTO advertising (titel,url) VALUES(?,?)", (titel, url))

    async def put_advertising(self, id, titel, url):
        return await db.update("UPDATE advertising SET titel=?,url=? WHERE id=?", (titel, url, id))


class CarData:
    # Данные раздела управления подборками (админ-панель)
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def get_fleet(self, **kwargs):
        LIMIT, OFFSET = kwargs.get('LIMIT'), kwargs.get('OFFSET')
        count = await db.select("SELECT COUNT(*) FROM fleet_list WHERE fleet_type =0")
        data = await db.select(
            "SELECT fleet_list.*, COUNT(group_list.id) AS group_count FROM fleet_list "
            "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state=2 "
            "WHERE fleet_type = 0 GROUP BY fleet_list.id ORDER BY title LIMIT ? OFFSET ?",
            (LIMIT, OFFSET),
        )
        if data:
            return data, count[0][0]
        return [], 0

    async def get_fleet_group_list(self, id):
        group = await db.select("SELECT * FROM group_list WHERE fleet_list=? AND state=2", (id,))
        if group:
            return group
        return []

    async def get_fleet_one(self, id):
        fleet = await db.select(
            "SELECT fleet_list.*, COUNT(group_list.id) AS group_count "
            "FROM fleet_list "
            "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state = 2 "
            "WHERE fleet_list.id = ? GROUP BY fleet_list.id",
            (id,),
        )
        if fleet:
            return fleet[0]
        return []

    async def get_user_group_one(self, id):
        my_group = await db.select("SELECT * FROM group_list WHERE id=?", (id,))
        if my_group:
            return my_group[0]
        return []

    async def post_car(self, car_title, car_type):
        return await db.insert("INSERT INTO fleet_list (title,fleet_type) VALUES(?,?)", (car_title, car_type))

    async def put_car_titel(self, id, text):
        return await db.update("UPDATE fleet_list SET title=? WHERE id=?", (text, id))

    async def put_car_introduce(self, id, text):
        return await db.update("UPDATE fleet_list SET introduce=? WHERE id=?", (text, id))

    async def put_car_total(self, id, text):
        return await db.update("UPDATE fleet_list SET total=? WHERE id=?", (text, id))

    async def put_car_mi_memberl(self, id, text):
        return await db.update("UPDATE fleet_list SET mi_member=? WHERE id=?", (text, id))

    async def put_car_mi_mi_read(self, id, text):
        return await db.update("UPDATE fleet_list SET mi_read=? WHERE id=?", (text, id))

    async def put_car_state(self, id, text):
        return await db.update("UPDATE fleet_list SET state=? WHERE id=?", (text, id))

    async def put_car_pass_review(self, group, state, label, url=None):
        if url:
            group_d = await db.update("UPDATE group_list SET state=?,url=?,msg_id=0 WHERE id=?", (state, url, group[0]))
        else:
            group_d = await db.update("UPDATE group_list SET state=?,msg_id=0 WHERE id=?", (state, group[0]))
        if group_d:
            await self.post_notify_msg(group=group, label=label)
            return True
        return False

    async def post_notify_msg(self, group, label):
        notify = await db.insert(
            "INSERT INTO notify_msg (user_id,group_id,msg) VALUES(?,?,?)",
            (group[12], group[0], label),
        )
        return bool(notify)

    async def get_notify_msg(self, user=None, group=None):
        data = await db.select(
            "SELECT * FROM notify_msg WHERE group_id = ? AND user_id = ? ORDER BY id DESC LIMIT 1",
            (group, user),
        )
        if data:
            return data[0]
        return []

    async def get_user(self, id):
        user = await db.select("SELECT * FROM chat_user WHERE id=?", (id,))
        if user:
            return user[0]
        return []

    async def get_rejectText(self, id):
        data = await db.select("SELECT * FROM config WHERE name='rejectText' AND id=?", (id,))
        if data:
            return data[0]
        return []


class GroupData:
    # Данные раздела управления группами и каналами
    async def get_group_list(self, **kwargs):
        LIMIT, OFFSET = kwargs.get('LIMIT'), kwargs.get('OFFSET')
        search = kwargs.get('search')
        if search:
            data = await db.select(
                "SELECT * FROM group_list WHERE title LIKE ? ORDER BY id LIMIT ? OFFSET ?",
                (f"%{search}%", LIMIT, OFFSET),
            )
        else:
            data = await db.select("SELECT * FROM group_list ORDER BY id LIMIT ? OFFSET ?", (LIMIT, OFFSET))
        if data:
            return data
        return []

    async def get_group_index_count(self, **kwargs):
        count = await db.select(
            "SELECT (SELECT COUNT(*) FROM group_list) AS total_count,"
            "(SELECT COUNT(*) FROM group_list WHERE type='CHANNEL') AS CHANNEL_count,"
            "(SELECT COUNT(*) FROM group_list WHERE type='CHANNEL' AND state=2) AS CHANNEL_state_count,"
            "(SELECT COUNT(*) FROM group_list WHERE type='SUPERGROUP') AS SUPERGROUP_count,"
            "(SELECT COUNT(*) FROM group_list WHERE type='SUPERGROUP' AND state=2) AS SUPERGROUP_state_count"
        )
        if count:
            return count[0]
        return (0, 0, 0, 0, 0)

    async def get_group_info(self, id):
        data = await db.select("SELECT * FROM group_list WHERE id=?", (id,))
        if data:
            return data[0]
        return []

    async def get_fleet_one(self, id):
        fleet = await db.select("SELECT * FROM fleet_list WHERE id=?", (id,))
        if fleet:
            return fleet[0]
        return []

    async def get_user(self, id):
        user = await db.select("SELECT * FROM chat_user WHERE id=?", (id,))
        if user:
            return user[0]
        return []


class ChannelFleetList:
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def get(self, **kwargs):
        data = await db.select("SELECT * FROM fleet_list ORDER BY sign")
        if data:
            return data
        return []

    async def get_fleet(self, **kwargs):
        LIMIT, OFFSET = kwargs.get('LIMIT'), kwargs.get('OFFSET')
        count = await db.select("SELECT COUNT(*) FROM fleet_list WHERE fleet_type =0")
        data = await db.select(
            "SELECT fleet_list.*, COUNT(group_list.id) AS group_count FROM fleet_list "
            "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state=2 "
            "WHERE fleet_type = 0 AND fleet_list.state=1 GROUP BY fleet_list.id ORDER BY title LIMIT ? OFFSET ?",
            (LIMIT, OFFSET),
        )
        if data:
            return data, count[0][0]
        return [], 0

    async def get_group_count(self, **kwargs):
        count = await db.select("SELECT COUNT(*) FROM group_list WHERE type='CHANNEL' AND state=2")
        if count:
            return count[0][0]
        return 0

    async def get_fleet_one(self, id):
        fleet = await db.select(
            "SELECT fleet_list.*, COUNT(group_list.id) AS group_count "
            "FROM fleet_list "
            "LEFT JOIN group_list ON fleet_list.id = group_list.fleet_list AND group_list.state = 2 "
            "WHERE fleet_list.id = ? GROUP BY fleet_list.id",
            (id,),
        )
        if fleet:
            return fleet[0]
        return []

    async def get_fleet_group_list(self, id):
        group = await db.select("SELECT * FROM group_list WHERE fleet_list=? AND state=2", (id,))
        if group:
            return group
        return []

    async def get_user_group_list(self, id, member):
        my_group = await db.select(
            "SELECT * FROM group_list WHERE chat_id=? AND type=? AND total_people>=?",
            (id, "CHANNEL", member),
        )
        if my_group:
            return my_group
        return []

    async def get_user_group_one(self, id):
        my_group = await db.select("SELECT * FROM group_list WHERE id=?", (id,))
        if my_group:
            return my_group[0]
        return []

    async def put_group_one(self, id, fieet):
        upData = await db.update("UPDATE group_list SET state=1,fleet_list=?,msg_id=0 WHERE id=?", (fieet, id))
        return bool(upData)

    async def get_admini_list(self):
        admin = await db.select("SELECT * FROM chat_user WHERE admin IN (1,2)")
        if admin:
            return admin
        return []


class BotBlacklistDate:
    async def get_bot_blacklist_list(self):
        data = await db.select("SELECT * FROM bot_blacklist")
        if data:
            return data
        return []

    async def del_bot_blacklist(self, id):
        return await db.delete("DELETE FROM bot_blacklist WHERE id=?", (id,))

    async def post_bot_blacklist(self, titel):
        return await db.insert("INSERT INTO bot_blacklist (bot_name) VALUES(?)", (titel,))

    async def put_bot_blacklist(self, id, titel):
        print(titel, id)
        return await db.update("UPDATE bot_blacklist SET bot_name=? WHERE id=?", (titel, id))
