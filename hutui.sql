-- Схема и начальные данные SQLite для бота взаимопиара

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Таблица advertising (реклама в рассылке)
-- ----------------------------
DROP TABLE IF EXISTS `advertising`;
CREATE TABLE `advertising` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `titel` TEXT DEFAULT NULL, -- Заголовок рекламы
  `url` TEXT DEFAULT NULL, -- Ссылка рекламы
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP -- Время создания рекламы
);

BEGIN TRANSACTION;
INSERT INTO `advertising` VALUES (6, 'Взаимопиар 2', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
INSERT INTO `advertising` VALUES (7, 'Взаимопиар', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
INSERT INTO `advertising` VALUES (9, 'Взаимопиар 3', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
COMMIT;

-- ----------------------------
-- Таблица bot_blacklist (чёрный список ботов)
-- ----------------------------
DROP TABLE IF EXISTS `bot_blacklist`;
CREATE TABLE `bot_blacklist` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `bot_name` TEXT DEFAULT NULL, -- Юзернейм бота
  `state` INTEGER DEFAULT 0,
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP
);

BEGIN TRANSACTION;
INSERT INTO `bot_blacklist` VALUES (3, '@hutui01bot', 0, '2023-10-31 15:37:15');
INSERT INTO `bot_blacklist` VALUES (4, '@hutui1bot', 0, '2023-10-31 15:37:23');
INSERT INTO `bot_blacklist` VALUES (5, '@TGMFHTbot', 0, '2023-10-31 15:37:29');
INSERT INTO `bot_blacklist` VALUES (6, '@haloukt1_bot', 0, '2023-10-31 15:37:36');
INSERT INTO `bot_blacklist` VALUES (7, '@hutuiZSbot', 0, '2023-10-31 15:37:48');
INSERT INTO `bot_blacklist` VALUES (8, '@zyehtbot', 0, '2023-10-31 15:37:58');
INSERT INTO `bot_blacklist` VALUES (9, '@tkhutuibot', 0, '2023-10-31 15:38:07');
COMMIT;

-- ----------------------------
-- Таблица chat_user (пользователи)
-- ----------------------------
DROP TABLE IF EXISTS `chat_user`;
CREATE TABLE `chat_user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `chat_id` TEXT DEFAULT NULL, -- ID пользователя
  `username` TEXT DEFAULT NULL, -- Юзернейм
  `full_name` TEXT DEFAULT NULL, -- Полное имя
  `state` INTEGER DEFAULT 0, -- Статус аккаунта
  `admin` INTEGER DEFAULT 0, -- Права администратора: 0 — пользователь, 1 — админ, 2 — суперадмин
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP
);

BEGIN TRANSACTION;
INSERT INTO `chat_user` VALUES (612, '5692641141', 'mao_zong', 'MaoZong', 0, 2, '2023-09-27 00:34:44');
INSERT INTO `chat_user` VALUES (616, '1471417837', 'lmmppll', 'Призрак', 0, 1, '2023-10-18 23:50:04');
INSERT INTO `chat_user` VALUES (617, '5966721929', 'Нет', 'B𝗼', 0, 1, '2023-10-21 22:41:36');
INSERT INTO `chat_user` VALUES (618, '6148737329', 'Нет', '🥹😆', 1, 0, '2023-10-22 03:27:43');
INSERT INTO `chat_user` VALUES (622, '936592623', 'Slee_mao', 'SleepyCat', 0, 2, '2023-10-22 10:05:57');
INSERT INTO `chat_user` VALUES (623, '1295', 'Нет', 'Тестовый пользователь', 0, 0, '2023-10-22 17:17:03');
INSERT INTO `chat_user` VALUES (624, '6698677206', 'YWN888999', 'Вечность', 0, 0, '2023-10-31 23:52:24');
INSERT INTO `chat_user` VALUES (625, '6042901473', 'agent47promo', 'Agent47', 0, 1, '2023-11-06 23:37:08');
COMMIT;

-- ----------------------------
-- Таблица config (настройки бота)
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT DEFAULT NULL,
  `comm` TEXT DEFAULT NULL
);

BEGIN TRANSACTION;
INSERT INTO `config` VALUES (1, 'botName', 'Бот взаимопиара 1');
INSERT INTO `config` VALUES (2, 'botUserName', '@FlashCloudBot');
INSERT INTO `config` VALUES (8, 'indexTxt', 'Добро пожаловать в бота взаимопиара');
INSERT INTO `config` VALUES (11, 'adminGroup', '-1001977340890');
INSERT INTO `config` VALUES (12, 'publicGroup', '@sepigzs');
INSERT INTO `config` VALUES (16, 'msgGroup', '-');
INSERT INTO `config` VALUES (17, 'video', '');
INSERT INTO `config` VALUES (19, 'restrict_limit', '30');
INSERT INTO `config` VALUES (20, 'notifyType', '0');
INSERT INTO `config` VALUES (22, 'rejectText', 'В этой подборке больше нет мест, подайте заявку в другую');
INSERT INTO `config` VALUES (23, 'rejectText', 'Недостаточно активности');
INSERT INTO `config` VALUES (24, 'rejectText', 'Низкое качество контента');
INSERT INTO `config` VALUES (25, 'rejectText', 'Недостаточно просмотров');
COMMIT;

-- ----------------------------
-- Таблица fleet_list (подборки)
-- ----------------------------
DROP TABLE IF EXISTS `fleet_list`;
CREATE TABLE `fleet_list` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` TEXT DEFAULT NULL, -- Название подборки
  `introduce` TEXT DEFAULT NULL, -- Описание подборки
  `fleet_type` INTEGER DEFAULT 0, -- Тип подборки: 0 — канал, 1 — группа, 2 — своя
  `state` INTEGER DEFAULT 0, -- Статус: 0 — остановлена, 1 — запущена
  `sign` TEXT DEFAULT NULL, -- Метка сортировки: abcd
  `total` INTEGER DEFAULT 20, -- Макс. участников взаимопиара
  `count` INTEGER DEFAULT 1, -- Период рассылки
  `mi_member` INTEGER DEFAULT 1, -- Мин. подписчиков
  `mi_read` INTEGER DEFAULT 1, -- Мин. средних просмотров
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP -- Время создания
);

BEGIN TRANSACTION;
INSERT INTO `fleet_list` VALUES (8, 'Группа A1', NULL, 0, 1, NULL, 20, 1, 1, 1, '2023-10-25 11:23:03');
COMMIT;

-- ----------------------------
-- Таблица group_list (каналы и группы)
-- ----------------------------
DROP TABLE IF EXISTS `group_list`;
CREATE TABLE `group_list` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `group_id` TEXT DEFAULT NULL, -- ID группы/канала
  `username` TEXT DEFAULT NULL, -- Юзернейм группы/канала
  `title` TEXT DEFAULT NULL, -- Название группы/канала
  `type` TEXT DEFAULT NULL, -- Тип: канал / группа
  `total_people` INTEGER DEFAULT NULL, -- Всего участников
  `url` TEXT DEFAULT NULL, -- Основная ссылка
  `msg_id` INTEGER DEFAULT 0, -- ID сообщения взаимопиара
  `out_fan` INTEGER DEFAULT 0, -- Исходящий трафик
  `input_fan` INTEGER DEFAULT 0, -- Входящий трафик
  `state` INTEGER DEFAULT 0, -- Статус: 0 — свободен, 1 — на проверке, 2 — одобрен, 10 — заблокирован
  `fleet_list` INTEGER DEFAULT 0, -- Текущая подборка
  `chat_id` INTEGER DEFAULT NULL, -- ID владельца
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP
);

BEGIN TRANSACTION;
INSERT INTO `group_list` VALUES (212, '-1001926767085', 'anniutes', 'Тестовый канал', 'CHANNEL', 85, 'https://t.me/+K4HlbH17FFhhOGNl', 0, 0, 0, 1, 8, 612, '2023-10-25 11:24:08');
INSERT INTO `group_list` VALUES (213, '-1001977340890', '', 'Тестовая группа', 'SUPERGROUP', 4, 'https://t.me/+zK1UylU7DvtlNDc1', 0, 0, 0, 0, 0, 612, '2023-10-25 11:24:44');
INSERT INTO `group_list` VALUES (214, '-1001909433562', '', 'Тестовый канал 2', 'CHANNEL', 20, 'https://t.me/+aYU-bOyGsDlmMGM1', 0, 0, 0, 0, 8, 612, '2023-10-28 17:53:45');
COMMIT;

-- ----------------------------
-- Таблица notify_msg (история уведомлений)
-- ----------------------------
DROP TABLE IF EXISTS `notify_msg`;
CREATE TABLE `notify_msg` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INTEGER DEFAULT NULL, -- ID пользователя
  `group_id` INTEGER DEFAULT NULL, -- ID ресурса
  `msg` TEXT DEFAULT NULL, -- Сообщение
  `creation_time` DATETIME DEFAULT CURRENT_TIMESTAMP
);

BEGIN TRANSACTION;
INSERT INTO `notify_msg` VALUES (57, 612, 156, 'На проверке', '2023-10-18 11:07:18');
INSERT INTO `notify_msg` VALUES (58, 612, 159, 'На проверке', '2023-10-18 11:17:50');
INSERT INTO `notify_msg` VALUES (59, 612, 160, 'На проверке', '2023-10-18 11:18:34');
INSERT INTO `notify_msg` VALUES (61, 612, 160, 'Одобрено', '2023-10-18 16:58:39');
INSERT INTO `notify_msg` VALUES (62, 612, 159, 'Одобрено', '2023-10-18 17:00:17');
INSERT INTO `notify_msg` VALUES (63, 612, 156, 'Одобрено', '2023-10-18 17:18:43');
COMMIT;
