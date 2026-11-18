/*
 Navicat Premium Data Transfer

 Source Server         : 本地WP数据库
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : hutui

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 11/11/2023 20:52:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for advertising
-- ----------------------------
DROP TABLE IF EXISTS `advertising`;
CREATE TABLE `advertising` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titel` varchar(255) DEFAULT NULL COMMENT '广告标题',
  `url` varchar(255) DEFAULT NULL COMMENT '广告链接',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '广告创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of advertising
-- ----------------------------
BEGIN;
INSERT INTO `advertising` VALUES (6, '互推2', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
INSERT INTO `advertising` VALUES (7, '互推', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
INSERT INTO `advertising` VALUES (9, '互推3', 'https://t.me/+oYUJoUkMlfphN2M1', NULL);
COMMIT;

-- ----------------------------
-- Table structure for bot_blacklist
-- ----------------------------
DROP TABLE IF EXISTS `bot_blacklist`;
CREATE TABLE `bot_blacklist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bot_name` varchar(255) DEFAULT NULL COMMENT '机器人用户名',
  `state` int DEFAULT '0',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of bot_blacklist
-- ----------------------------
BEGIN;
INSERT INTO `bot_blacklist` VALUES (3, '@hutui01bot', 0, '2023-10-31 15:37:15');
INSERT INTO `bot_blacklist` VALUES (4, '@hutui1bot', 0, '2023-10-31 15:37:23');
INSERT INTO `bot_blacklist` VALUES (5, '@TGMFHTbot', 0, '2023-10-31 15:37:29');
INSERT INTO `bot_blacklist` VALUES (6, '@haloukt1_bot', 0, '2023-10-31 15:37:36');
INSERT INTO `bot_blacklist` VALUES (7, '@hutuiZSbot', 0, '2023-10-31 15:37:48');
INSERT INTO `bot_blacklist` VALUES (8, '@zyehtbot', 0, '2023-10-31 15:37:58');
INSERT INTO `bot_blacklist` VALUES (9, '@tkhutuibot', 0, '2023-10-31 15:38:07');
COMMIT;

-- ----------------------------
-- Table structure for chat_user
-- ----------------------------
DROP TABLE IF EXISTS `chat_user`;
CREATE TABLE `chat_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户ID',
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账号',
  `full_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '昵称全名',
  `state` int DEFAULT '0' COMMENT '账号状态',
  `admin` int DEFAULT '0' COMMENT '管理员权限 0普通用户1管理员',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=626 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of chat_user
-- ----------------------------
BEGIN;
INSERT INTO `chat_user` VALUES (612, '5692641141', 'mao_zong', 'MaoZong', 0, 2, '2023-09-27 00:34:44');
INSERT INTO `chat_user` VALUES (616, '1471417837', 'lmmppll', '鬼怪', 0, 1, '2023-10-18 23:50:04');
INSERT INTO `chat_user` VALUES (617, '5966721929', '无', 'B𝗼', 0, 1, '2023-10-21 22:41:36');
INSERT INTO `chat_user` VALUES (618, '6148737329', '无', '🥹😆', 1, 0, '2023-10-22 03:27:43');
INSERT INTO `chat_user` VALUES (622, '936592623', 'Slee_mao', 'SleepyCat', 0, 2, '2023-10-22 10:05:57');
INSERT INTO `chat_user` VALUES (623, '1295', '无', '@Huaren【华人在外】灰云 收款地址10个y', 0, 0, '2023-10-22 17:17:03');
INSERT INTO `chat_user` VALUES (624, '6698677206', 'YWN888999', '一万年', 0, 0, '2023-10-31 23:52:24');
INSERT INTO `chat_user` VALUES (625, '6042901473', 'agent47promo', 'Agent47', 0, 1, '2023-11-06 23:37:08');
COMMIT;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `comm` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of config
-- ----------------------------
BEGIN;
INSERT INTO `config` VALUES (1, 'botName', '互推机器人1');
INSERT INTO `config` VALUES (2, 'botUserName', '@FlashCloudBot');
INSERT INTO `config` VALUES (8, 'indexTxt', '欢迎使用互推机器人');
INSERT INTO `config` VALUES (11, 'adminGroup', '-1001977340890');
INSERT INTO `config` VALUES (12, 'publicGroup', '@sepigzs');
INSERT INTO `config` VALUES (16, 'msgGroup', '-');
INSERT INTO `config` VALUES (17, 'video', '');
INSERT INTO `config` VALUES (19, 'restrict_limit', '30');
INSERT INTO `config` VALUES (20, 'notifyType', '0');
INSERT INTO `config` VALUES (22, 'rejectText', '该小组成员已满，申请其他小组不');
INSERT INTO `config` VALUES (23, 'rejectText', '安德森');
INSERT INTO `config` VALUES (24, 'rejectText', '质量太差');
INSERT INTO `config` VALUES (25, 'rejectText', '阅读不足');
COMMIT;

-- ----------------------------
-- Table structure for fleet_list
-- ----------------------------
DROP TABLE IF EXISTS `fleet_list`;
CREATE TABLE `fleet_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '车队标题',
  `introduce` varchar(255) DEFAULT NULL COMMENT '车队介绍',
  `fleet_type` int DEFAULT '0' COMMENT '车队类型：0频道，1群组，2自定义',
  `state` int DEFAULT '0' COMMENT '状态:0未开车，1已开车',
  `sign` varchar(255) DEFAULT NULL COMMENT '排序标记:abcd',
  `total` int DEFAULT '20' COMMENT '最大互推成员数',
  `count` int DEFAULT '1' COMMENT '开车周期',
  `mi_member` int DEFAULT '1' COMMENT '最少订阅人数',
  `mi_read` int DEFAULT '1' COMMENT '最低平均阅读',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of fleet_list
-- ----------------------------
BEGIN;
INSERT INTO `fleet_list` VALUES (8, 'A组1', NULL, 0, 1, NULL, 20, 1, 1, 1, '2023-10-25 11:23:03');
COMMIT;

-- ----------------------------
-- Table structure for group_list
-- ----------------------------
DROP TABLE IF EXISTS `group_list`;
CREATE TABLE `group_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) DEFAULT NULL COMMENT '群组id',
  `username` varchar(255) DEFAULT NULL COMMENT '群组账号',
  `title` varchar(255) DEFAULT NULL COMMENT '群组标题',
  `type` varchar(64) DEFAULT NULL COMMENT '类型/频道/群组',
  `total_people` int DEFAULT NULL COMMENT '群频总人数',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '主url',
  `msg_id` int DEFAULT '0' COMMENT '互推消息id',
  `out_fan` int DEFAULT '0' COMMENT '输出粉丝',
  `input_fan` int DEFAULT '0' COMMENT '输入粉丝',
  `state` int DEFAULT '0' COMMENT '状态:0未加入,1审核中,2已审核,99禁用',
  `fleet_list` int DEFAULT '0' COMMENT '当前车队',
  `chat_id` int DEFAULT NULL COMMENT '所属用户',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=215 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of group_list
-- ----------------------------
BEGIN;
INSERT INTO `group_list` VALUES (212, '-1001926767085', 'anniutes', '频道测试', 'CHANNEL', 85, 'https://t.me/+K4HlbH17FFhhOGNl', 0, 0, 0, 1, 8, 612, '2023-10-25 11:24:08');
INSERT INTO `group_list` VALUES (213, '-1001977340890', '', '测试群组', 'SUPERGROUP', 4, 'https://t.me/+zK1UylU7DvtlNDc1', 0, 0, 0, 0, 0, 612, '2023-10-25 11:24:44');
INSERT INTO `group_list` VALUES (214, '-1001909433562', '', '测试频道2', 'CHANNEL', 20, 'https://t.me/+aYU-bOyGsDlmMGM1', 0, 0, 0, 0, 8, 612, '2023-10-28 17:53:45');
COMMIT;

-- ----------------------------
-- Table structure for notify_msg
-- ----------------------------
DROP TABLE IF EXISTS `notify_msg`;
CREATE TABLE `notify_msg` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '所属用户',
  `group_id` int DEFAULT NULL COMMENT '所属组',
  `msg` varchar(255) DEFAULT NULL COMMENT '消息',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=350 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of notify_msg
-- ----------------------------
BEGIN;
INSERT INTO `notify_msg` VALUES (57, 612, 156, '待审核', '2023-10-18 11:07:18');
INSERT INTO `notify_msg` VALUES (58, 612, 159, '待审核', '2023-10-18 11:17:50');
INSERT INTO `notify_msg` VALUES (59, 612, 160, '待审核', '2023-10-18 11:18:34');
INSERT INTO `notify_msg` VALUES (60, 612, 156, '待审核', '2023-10-18 13:47:05');
INSERT INTO `notify_msg` VALUES (61, 612, 160, '审核成功', '2023-10-18 16:58:39');
INSERT INTO `notify_msg` VALUES (62, 612, 159, '审核成功', '2023-10-18 17:00:17');
INSERT INTO `notify_msg` VALUES (63, 612, 156, '审核成功', '2023-10-18 17:18:43');
INSERT INTO `notify_msg` VALUES (64, 612, 156, '待审核', '2023-10-18 18:42:36');
INSERT INTO `notify_msg` VALUES (65, 612, 156, '审核成功', '2023-10-18 19:29:31');
INSERT INTO `notify_msg` VALUES (66, 612, 156, '待审核', '2023-10-18 19:30:50');
INSERT INTO `notify_msg` VALUES (67, 612, 156, '审核成功', '2023-10-18 19:30:55');
INSERT INTO `notify_msg` VALUES (68, 612, 159, '待审核', '2023-10-18 19:31:17');
INSERT INTO `notify_msg` VALUES (69, 612, 159, '审核失败:无邀请权限', '2023-10-18 19:32:05');
INSERT INTO `notify_msg` VALUES (70, 612, 159, '审核失败:无邀请权限', '2023-10-18 19:32:27');
INSERT INTO `notify_msg` VALUES (71, 612, 159, '审核失败:无邀请权限', '2023-10-18 19:32:41');
INSERT INTO `notify_msg` VALUES (72, 612, 160, '待审核', '2023-10-18 19:33:38');
INSERT INTO `notify_msg` VALUES (73, 612, 159, '待审核', '2023-10-18 19:33:41');
INSERT INTO `notify_msg` VALUES (74, 612, 160, '审核失败:无邀请权限', '2023-10-18 19:33:48');
INSERT INTO `notify_msg` VALUES (75, 612, 159, '审核成功', '2023-10-18 19:34:07');
INSERT INTO `notify_msg` VALUES (76, 612, 159, '待审核', '2023-10-18 19:38:25');
INSERT INTO `notify_msg` VALUES (77, 612, 159, '审核失败:车队不存在', '2023-10-18 19:38:33');
INSERT INTO `notify_msg` VALUES (78, 612, 159, '审核失败:车队不存在', '2023-10-18 19:38:37');
INSERT INTO `notify_msg` VALUES (79, 612, 160, '待审核', '2023-10-18 19:40:52');
INSERT INTO `notify_msg` VALUES (80, 612, 160, '审核失败:该小组成员已满，申请其他小组不', '2023-10-18 19:46:13');
INSERT INTO `notify_msg` VALUES (81, 612, 156, '待审核', '2023-10-18 21:34:49');
INSERT INTO `notify_msg` VALUES (82, 612, 159, '待审核', '2023-10-18 21:34:51');
INSERT INTO `notify_msg` VALUES (83, 612, 160, '待审核', '2023-10-18 21:34:53');
INSERT INTO `notify_msg` VALUES (84, 612, 160, '审核失败:该小组成员已满，申请其他小组不', '2023-10-18 22:36:02');
INSERT INTO `notify_msg` VALUES (85, 612, 159, '审核失败:安德森', '2023-10-18 22:36:09');
INSERT INTO `notify_msg` VALUES (86, 612, 156, '审核失败:质量太差', '2023-10-18 22:36:16');
INSERT INTO `notify_msg` VALUES (87, 612, 156, '待审核', '2023-10-18 22:38:02');
INSERT INTO `notify_msg` VALUES (88, 612, 159, '待审核', '2023-10-19 00:02:29');
INSERT INTO `notify_msg` VALUES (89, 612, 160, '待审核', '2023-10-19 00:03:36');
INSERT INTO `notify_msg` VALUES (90, 612, 160, '审核失败:安德森', '2023-10-19 00:06:09');
INSERT INTO `notify_msg` VALUES (91, 612, 160, '审核失败:质量太差', '2023-10-19 00:06:54');
INSERT INTO `notify_msg` VALUES (92, 612, 160, '审核失败:安德森', '2023-10-19 00:07:15');
INSERT INTO `notify_msg` VALUES (93, 612, 160, '待审核', '2023-10-19 00:12:21');
INSERT INTO `notify_msg` VALUES (94, 612, 160, '审核失败:啦啦啦', '2023-10-19 00:13:42');
INSERT INTO `notify_msg` VALUES (95, 612, 160, '审核失败:阿斯顿', '2023-10-19 00:14:41');
INSERT INTO `notify_msg` VALUES (96, 612, 160, '待审核', '2023-10-19 00:16:36');
INSERT INTO `notify_msg` VALUES (97, 612, 160, '审核失败:该小组成员已满，申请其他小组不', '2023-10-19 00:17:07');
INSERT INTO `notify_msg` VALUES (98, 612, 160, '审核失败:质量太差', '2023-10-19 00:17:26');
INSERT INTO `notify_msg` VALUES (99, 612, 160, '待审核', '2023-10-19 00:17:44');
INSERT INTO `notify_msg` VALUES (100, 612, 160, '审核失败:质量太差', '2023-10-19 00:17:51');
INSERT INTO `notify_msg` VALUES (101, 612, 160, '审核失败:质量太差', '2023-10-19 00:18:08');
INSERT INTO `notify_msg` VALUES (102, 612, 160, '待审核', '2023-10-19 00:44:25');
INSERT INTO `notify_msg` VALUES (103, 612, 160, '审核失败:质量太差', '2023-10-19 00:45:28');
INSERT INTO `notify_msg` VALUES (104, 612, 160, '待审核', '2023-10-19 00:45:33');
INSERT INTO `notify_msg` VALUES (105, 612, 160, '审核失败:已被管理员禁用', '2023-10-19 00:47:02');
INSERT INTO `notify_msg` VALUES (106, 612, 160, '审核失败:已被管理员禁用', '2023-10-19 00:48:44');
INSERT INTO `notify_msg` VALUES (107, 612, 156, '待审核', '2023-10-19 00:49:17');
INSERT INTO `notify_msg` VALUES (108, 612, 156, '审核失败:质量太差', '2023-10-19 00:50:16');
INSERT INTO `notify_msg` VALUES (109, 612, 156, '待审核', '2023-10-19 00:50:23');
INSERT INTO `notify_msg` VALUES (110, 612, 156, '审核失败:已被管理员禁用', '2023-10-19 00:50:30');
INSERT INTO `notify_msg` VALUES (111, 612, 159, '待审核', '2023-10-19 00:52:39');
INSERT INTO `notify_msg` VALUES (112, 612, 159, '审核失败:hahdf', '2023-10-19 00:52:51');
INSERT INTO `notify_msg` VALUES (113, 612, 159, '审核失败:了多少咖啡馆', '2023-10-19 00:54:45');
INSERT INTO `notify_msg` VALUES (114, 612, 159, '您的频道已被管理员禁用', '2023-10-19 00:55:30');
INSERT INTO `notify_msg` VALUES (115, 612, 159, '您的频道已解除禁用', '2023-10-19 01:52:32');
INSERT INTO `notify_msg` VALUES (116, 612, 159, '您的频道已解除禁用', '2023-10-19 01:52:36');
INSERT INTO `notify_msg` VALUES (117, 612, 159, '您的频道已解除禁用', '2023-10-19 01:53:02');
INSERT INTO `notify_msg` VALUES (118, 612, 159, '您的频道已解除禁用', '2023-10-19 01:53:28');
INSERT INTO `notify_msg` VALUES (119, 612, 159, '您的频道已被管理员禁用', '2023-10-19 01:58:30');
INSERT INTO `notify_msg` VALUES (120, 612, 159, '您的频道已解除禁用', '2023-10-19 01:58:35');
INSERT INTO `notify_msg` VALUES (121, 612, 159, '您的频道已被管理员禁用', '2023-10-19 01:58:45');
INSERT INTO `notify_msg` VALUES (122, 612, 159, '您的频道已解除禁用', '2023-10-19 01:58:45');
INSERT INTO `notify_msg` VALUES (123, 612, 156, '您的频道已解除禁用', '2023-10-19 01:59:25');
INSERT INTO `notify_msg` VALUES (124, 612, 156, '您的频道已被管理员禁用', '2023-10-19 01:59:25');
INSERT INTO `notify_msg` VALUES (125, 612, 156, '您的频道已解除禁用', '2023-10-19 01:59:25');
INSERT INTO `notify_msg` VALUES (126, 612, 156, '您的频道已被管理员禁用', '2023-10-19 01:59:25');
INSERT INTO `notify_msg` VALUES (127, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:01:05');
INSERT INTO `notify_msg` VALUES (128, 612, 156, '您的频道已解除禁用', '2023-10-19 02:01:49');
INSERT INTO `notify_msg` VALUES (129, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:01:55');
INSERT INTO `notify_msg` VALUES (130, 612, 159, '您的频道已解除禁用', '2023-10-19 02:01:57');
INSERT INTO `notify_msg` VALUES (131, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:01:59');
INSERT INTO `notify_msg` VALUES (132, 612, 159, '您的频道已解除禁用', '2023-10-19 02:02:00');
INSERT INTO `notify_msg` VALUES (133, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:02:01');
INSERT INTO `notify_msg` VALUES (134, 612, 159, '您的频道已解除禁用', '2023-10-19 02:02:02');
INSERT INTO `notify_msg` VALUES (135, 612, 156, '您的频道已解除禁用', '2023-10-19 02:02:04');
INSERT INTO `notify_msg` VALUES (136, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:02:05');
INSERT INTO `notify_msg` VALUES (137, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:02:07');
INSERT INTO `notify_msg` VALUES (138, 612, 156, '您的频道已解除禁用', '2023-10-19 02:03:41');
INSERT INTO `notify_msg` VALUES (139, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:03:44');
INSERT INTO `notify_msg` VALUES (140, 612, 156, '您的频道已解除禁用', '2023-10-19 02:03:45');
INSERT INTO `notify_msg` VALUES (141, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:03:46');
INSERT INTO `notify_msg` VALUES (142, 612, 156, '您的频道已解除禁用', '2023-10-19 02:03:50');
INSERT INTO `notify_msg` VALUES (143, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:03:52');
INSERT INTO `notify_msg` VALUES (144, 612, 156, '您的频道已解除禁用', '2023-10-19 02:03:55');
INSERT INTO `notify_msg` VALUES (145, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:03:58');
INSERT INTO `notify_msg` VALUES (146, 612, 159, '您的频道已解除禁用', '2023-10-19 02:04:01');
INSERT INTO `notify_msg` VALUES (147, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:04:03');
INSERT INTO `notify_msg` VALUES (148, 612, 159, '您的频道已解除禁用', '2023-10-19 02:06:55');
INSERT INTO `notify_msg` VALUES (149, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:06:56');
INSERT INTO `notify_msg` VALUES (150, 612, 156, '您的频道已解除禁用', '2023-10-19 02:06:58');
INSERT INTO `notify_msg` VALUES (151, 612, 156, '您的频道已被管理员禁用', '2023-10-19 02:06:59');
INSERT INTO `notify_msg` VALUES (152, 612, 159, '您的频道已解除禁用', '2023-10-19 02:19:37');
INSERT INTO `notify_msg` VALUES (153, 612, NULL, '您的账号已被禁用', '2023-10-19 02:41:43');
INSERT INTO `notify_msg` VALUES (154, 612, 159, '待审核', '2023-10-19 02:48:11');
INSERT INTO `notify_msg` VALUES (155, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:48:26');
INSERT INTO `notify_msg` VALUES (156, 612, 159, '您的频道已解除禁用', '2023-10-19 02:48:30');
INSERT INTO `notify_msg` VALUES (157, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:49:24');
INSERT INTO `notify_msg` VALUES (158, 612, 159, '您的频道已解除禁用', '2023-10-19 02:50:08');
INSERT INTO `notify_msg` VALUES (159, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:50:12');
INSERT INTO `notify_msg` VALUES (160, 612, 159, '您的频道已解除禁用', '2023-10-19 02:50:18');
INSERT INTO `notify_msg` VALUES (161, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:50:46');
INSERT INTO `notify_msg` VALUES (162, 612, 159, '您的频道已解除禁用', '2023-10-19 02:50:49');
INSERT INTO `notify_msg` VALUES (163, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:51:27');
INSERT INTO `notify_msg` VALUES (164, 612, 159, '您的频道已解除禁用', '2023-10-19 02:51:28');
INSERT INTO `notify_msg` VALUES (165, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:52:14');
INSERT INTO `notify_msg` VALUES (166, 612, 159, '您的频道已解除禁用', '2023-10-19 02:52:16');
INSERT INTO `notify_msg` VALUES (167, 612, 159, '您的频道已被管理员禁用', '2023-10-19 02:52:18');
INSERT INTO `notify_msg` VALUES (168, 612, 160, '待审核', '2023-10-19 02:52:35');
INSERT INTO `notify_msg` VALUES (169, 612, 160, '审核失败:安德森', '2023-10-19 02:52:42');
INSERT INTO `notify_msg` VALUES (170, 612, 160, '待审核', '2023-10-19 02:54:27');
INSERT INTO `notify_msg` VALUES (171, 612, 160, '审核失败:电饭锅', '2023-10-19 02:54:35');
INSERT INTO `notify_msg` VALUES (172, 612, 160, '您的频道已被管理员禁用', '2023-10-19 02:54:45');
INSERT INTO `notify_msg` VALUES (173, 612, 160, '您的频道已解除禁用', '2023-10-19 02:54:48');
INSERT INTO `notify_msg` VALUES (174, 612, 159, '您的频道已解除禁用', '2023-10-19 02:55:10');
INSERT INTO `notify_msg` VALUES (175, 612, 209, '待审核', '2023-10-20 04:08:01');
INSERT INTO `notify_msg` VALUES (176, 612, 210, '待审核', '2023-10-20 04:09:19');
INSERT INTO `notify_msg` VALUES (177, 612, 210, '审核成功', '2023-10-20 04:09:29');
INSERT INTO `notify_msg` VALUES (178, 612, 209, '待审核', '2023-10-20 04:10:18');
INSERT INTO `notify_msg` VALUES (179, 612, 209, '审核成功', '2023-10-20 04:10:23');
INSERT INTO `notify_msg` VALUES (180, 612, 209, '待审核', '2023-10-20 04:20:37');
INSERT INTO `notify_msg` VALUES (181, 612, 209, '审核成功', '2023-10-20 04:20:38');
INSERT INTO `notify_msg` VALUES (182, 612, 210, '待审核', '2023-10-20 04:20:41');
INSERT INTO `notify_msg` VALUES (183, 612, 210, '审核成功', '2023-10-20 04:20:42');
INSERT INTO `notify_msg` VALUES (184, 612, 209, '待审核', '2023-10-20 04:23:15');
INSERT INTO `notify_msg` VALUES (185, 612, 210, '待审核', '2023-10-20 04:23:18');
INSERT INTO `notify_msg` VALUES (186, 612, 210, '审核成功', '2023-10-20 04:24:10');
INSERT INTO `notify_msg` VALUES (187, 612, 209, '审核成功', '2023-10-20 04:24:12');
INSERT INTO `notify_msg` VALUES (188, 612, 210, '待审核', '2023-10-20 04:43:35');
INSERT INTO `notify_msg` VALUES (189, 612, 209, '待审核', '2023-10-20 04:43:36');
INSERT INTO `notify_msg` VALUES (190, 612, 209, '审核成功', '2023-10-20 04:43:41');
INSERT INTO `notify_msg` VALUES (191, 612, 210, '审核成功', '2023-10-20 04:43:42');
INSERT INTO `notify_msg` VALUES (192, 612, 209, '您的频道已被管理员下车', '2023-10-20 04:48:39');
INSERT INTO `notify_msg` VALUES (193, 612, 209, '待审核', '2023-10-20 05:15:35');
INSERT INTO `notify_msg` VALUES (194, 612, 209, '审核成功', '2023-10-20 05:15:49');
INSERT INTO `notify_msg` VALUES (195, 612, 209, '您的频道已被管理员下车', '2023-10-20 06:00:53');
INSERT INTO `notify_msg` VALUES (196, 612, 209, '待审核', '2023-10-20 06:01:37');
INSERT INTO `notify_msg` VALUES (197, 612, 210, '待审核', '2023-10-20 06:01:39');
INSERT INTO `notify_msg` VALUES (198, 612, 210, '审核成功', '2023-10-20 06:01:47');
INSERT INTO `notify_msg` VALUES (199, 612, 209, '审核成功', '2023-10-20 06:01:48');
INSERT INTO `notify_msg` VALUES (200, 612, 209, '待审核', '2023-10-21 14:46:34');
INSERT INTO `notify_msg` VALUES (201, 612, 210, '待审核', '2023-10-21 14:48:08');
INSERT INTO `notify_msg` VALUES (202, 612, 210, '审核成功', '2023-10-21 14:48:16');
INSERT INTO `notify_msg` VALUES (203, 612, 209, '待审核', '2023-10-21 14:48:30');
INSERT INTO `notify_msg` VALUES (204, 612, 209, '审核失败:无邀请权限', '2023-10-21 14:54:10');
INSERT INTO `notify_msg` VALUES (205, 612, 209, '待审核', '2023-10-21 14:54:51');
INSERT INTO `notify_msg` VALUES (206, 612, 210, '待审核', '2023-10-21 14:54:55');
INSERT INTO `notify_msg` VALUES (207, 612, 210, '待审核', '2023-10-21 14:55:00');
INSERT INTO `notify_msg` VALUES (208, 612, 210, '审核失败:无邀请权限', '2023-10-21 15:04:35');
INSERT INTO `notify_msg` VALUES (209, 612, 210, '审核失败:无邀请权限', '2023-10-21 15:04:37');
INSERT INTO `notify_msg` VALUES (210, 612, 209, '待审核', '2023-10-21 15:05:20');
INSERT INTO `notify_msg` VALUES (211, 612, 209, '审核成功', '2023-10-21 15:05:34');
INSERT INTO `notify_msg` VALUES (212, 612, 209, '待审核', '2023-10-21 15:05:42');
INSERT INTO `notify_msg` VALUES (213, 612, 209, '待审核', '2023-10-21 15:05:46');
INSERT INTO `notify_msg` VALUES (214, 612, 210, '待审核', '2023-10-21 15:06:01');
INSERT INTO `notify_msg` VALUES (215, 612, 209, '待审核', '2023-10-21 15:06:16');
INSERT INTO `notify_msg` VALUES (216, 612, 210, '待审核', '2023-10-21 15:06:18');
INSERT INTO `notify_msg` VALUES (217, 612, 210, '审核失败:无邀请权限', '2023-10-21 15:18:10');
INSERT INTO `notify_msg` VALUES (218, 612, 209, '审核失败:无邀请权限', '2023-10-21 15:18:14');
INSERT INTO `notify_msg` VALUES (219, 612, 209, '您的频道已被管理员下车', '2023-10-21 23:10:45');
INSERT INTO `notify_msg` VALUES (220, 612, 210, '您的频道已被管理员禁用', '2023-10-21 23:40:01');
INSERT INTO `notify_msg` VALUES (221, 612, 209, '待审核', '2023-10-22 10:15:42');
INSERT INTO `notify_msg` VALUES (222, 612, 209, '待审核', '2023-10-22 10:16:11');
INSERT INTO `notify_msg` VALUES (223, 612, 209, '待审核', '2023-10-22 10:17:12');
INSERT INTO `notify_msg` VALUES (224, 612, 209, '审核成功', '2023-10-22 10:17:20');
INSERT INTO `notify_msg` VALUES (225, 612, 212, '待审核', '2023-10-25 11:27:30');
INSERT INTO `notify_msg` VALUES (226, 612, 212, '审核成功', '2023-10-25 11:27:41');
INSERT INTO `notify_msg` VALUES (227, 612, 212, '您的频道已被管理员禁用', '2023-10-25 11:27:45');
INSERT INTO `notify_msg` VALUES (228, 612, 212, '您的频道已解除禁用', '2023-10-25 11:27:47');
INSERT INTO `notify_msg` VALUES (229, 612, 212, '待审核', '2023-10-25 11:28:07');
INSERT INTO `notify_msg` VALUES (230, 612, 212, '审核成功', '2023-10-25 11:28:16');
INSERT INTO `notify_msg` VALUES (231, 612, 212, '您的频道已被管理员禁用', '2023-10-25 16:30:45');
INSERT INTO `notify_msg` VALUES (232, 612, 212, '您的频道已解除禁用', '2023-10-25 17:26:04');
INSERT INTO `notify_msg` VALUES (233, 612, 212, '待审核', '2023-10-26 01:04:44');
INSERT INTO `notify_msg` VALUES (234, 612, 212, '待审核', '2023-10-28 17:54:08');
INSERT INTO `notify_msg` VALUES (235, 612, 214, '待审核', '2023-10-28 17:54:11');
INSERT INTO `notify_msg` VALUES (236, 612, 212, '审核成功', '2023-10-28 17:54:33');
INSERT INTO `notify_msg` VALUES (237, 612, 212, '您的频道已被管理员下车', '2023-10-28 17:54:35');
INSERT INTO `notify_msg` VALUES (238, 612, 212, '您的频道已被管理员禁用', '2023-10-28 17:54:37');
INSERT INTO `notify_msg` VALUES (239, 612, 212, '您的频道已解除禁用', '2023-10-28 17:54:39');
INSERT INTO `notify_msg` VALUES (240, 612, 212, '待审核', '2023-10-28 20:55:19');
INSERT INTO `notify_msg` VALUES (241, 612, 214, '待审核', '2023-10-28 20:55:21');
INSERT INTO `notify_msg` VALUES (242, 612, 214, '审核成功', '2023-10-28 20:55:57');
INSERT INTO `notify_msg` VALUES (243, 612, 212, '审核失败:质量太差', '2023-10-28 20:56:46');
INSERT INTO `notify_msg` VALUES (244, 612, 212, '待审核', '2023-10-28 21:20:43');
INSERT INTO `notify_msg` VALUES (245, 612, 214, '待审核', '2023-10-28 21:20:45');
INSERT INTO `notify_msg` VALUES (246, 612, 214, '审核失败:123', '2023-10-28 21:23:28');
INSERT INTO `notify_msg` VALUES (247, 612, 212, '审核成功', '2023-10-28 21:23:44');
INSERT INTO `notify_msg` VALUES (248, 612, 212, '待审核', '2023-10-28 21:25:18');
INSERT INTO `notify_msg` VALUES (249, 612, 214, '待审核', '2023-10-28 21:25:21');
INSERT INTO `notify_msg` VALUES (250, 612, 212, '审核失败:阿斯顿发', '2023-10-28 21:25:38');
INSERT INTO `notify_msg` VALUES (251, 612, 212, '您的频道已被管理员禁用', '2023-10-28 21:25:40');
INSERT INTO `notify_msg` VALUES (252, 612, 212, '您的频道已解除禁用', '2023-10-28 21:25:41');
INSERT INTO `notify_msg` VALUES (253, 612, 212, '您的频道已被管理员禁用', '2023-10-28 21:26:22');
INSERT INTO `notify_msg` VALUES (254, 612, 212, '您的频道已解除禁用', '2023-10-28 21:26:26');
INSERT INTO `notify_msg` VALUES (255, 612, 212, '您的频道已被管理员禁用', '2023-10-28 21:27:36');
INSERT INTO `notify_msg` VALUES (256, 612, 212, '您的频道已解除禁用', '2023-10-28 21:27:37');
INSERT INTO `notify_msg` VALUES (257, 612, 214, '审核成功', '2023-10-28 21:27:45');
INSERT INTO `notify_msg` VALUES (258, 612, 214, '您的频道已被管理员下车', '2023-10-28 21:27:47');
INSERT INTO `notify_msg` VALUES (259, 612, 214, '您的频道已被管理员禁用', '2023-10-28 21:27:50');
INSERT INTO `notify_msg` VALUES (260, 612, 214, '您的频道已解除禁用', '2023-10-28 21:27:54');
INSERT INTO `notify_msg` VALUES (261, 612, 212, '待审核', '2023-10-28 21:29:56');
INSERT INTO `notify_msg` VALUES (262, 612, 214, '待审核', '2023-10-28 21:29:58');
INSERT INTO `notify_msg` VALUES (263, 612, 212, '审核成功', '2023-10-28 21:30:04');
INSERT INTO `notify_msg` VALUES (264, 612, 214, '审核成功', '2023-10-28 21:30:05');
INSERT INTO `notify_msg` VALUES (265, 612, 212, '您的频道已被管理员下车', '2023-10-29 00:55:16');
INSERT INTO `notify_msg` VALUES (266, 612, 212, '您的频道已被管理员下车', '2023-10-29 00:55:43');
INSERT INTO `notify_msg` VALUES (267, 612, 212, '您的频道已被管理员下车', '2023-10-29 00:56:49');
INSERT INTO `notify_msg` VALUES (268, 612, 214, '您的频道已被管理员下车', '2023-10-29 00:57:45');
INSERT INTO `notify_msg` VALUES (269, 612, 212, '您的频道已被管理员下车', '2023-10-29 00:59:13');
INSERT INTO `notify_msg` VALUES (270, 612, 214, '您的频道已被管理员下车', '2023-10-29 01:00:08');
INSERT INTO `notify_msg` VALUES (271, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:03:20');
INSERT INTO `notify_msg` VALUES (272, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:03:23');
INSERT INTO `notify_msg` VALUES (273, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:05:13');
INSERT INTO `notify_msg` VALUES (274, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:05:39');
INSERT INTO `notify_msg` VALUES (275, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:06:19');
INSERT INTO `notify_msg` VALUES (276, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:06:21');
INSERT INTO `notify_msg` VALUES (277, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:06:22');
INSERT INTO `notify_msg` VALUES (278, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:07:13');
INSERT INTO `notify_msg` VALUES (279, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:07:15');
INSERT INTO `notify_msg` VALUES (280, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:07:20');
INSERT INTO `notify_msg` VALUES (281, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:07:21');
INSERT INTO `notify_msg` VALUES (282, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:08:02');
INSERT INTO `notify_msg` VALUES (283, 612, 212, '您的频道已被管理员下车', '2023-10-29 01:08:04');
INSERT INTO `notify_msg` VALUES (284, 612, 212, '频道已被管理员上车', '2023-10-29 01:08:37');
INSERT INTO `notify_msg` VALUES (285, 612, 212, '频道已被管理员下车', '2023-10-29 01:08:38');
INSERT INTO `notify_msg` VALUES (286, 612, 212, '频道已被管理员上车', '2023-10-29 01:08:40');
INSERT INTO `notify_msg` VALUES (287, 612, 212, '频道已被管理员下车', '2023-10-29 01:08:42');
INSERT INTO `notify_msg` VALUES (288, 612, 212, '🟢 频道已被管理员上车', '2023-10-29 01:10:02');
INSERT INTO `notify_msg` VALUES (289, 612, 212, '🔴 频道已被管理员下车', '2023-10-29 01:10:04');
INSERT INTO `notify_msg` VALUES (290, 612, 214, '🟢 频道已被管理员禁用', '2023-10-29 01:14:29');
INSERT INTO `notify_msg` VALUES (291, 612, 214, '🚫 频道已解除禁用', '2023-10-29 01:14:35');
INSERT INTO `notify_msg` VALUES (292, 612, 214, '🟢 频道已被管理员禁用', '2023-10-29 01:14:38');
INSERT INTO `notify_msg` VALUES (293, 612, 214, '🟢 频道已解除禁用', '2023-10-29 01:15:19');
INSERT INTO `notify_msg` VALUES (294, 612, 214, '🚫 频道已被管理员禁用', '2023-10-29 01:15:21');
INSERT INTO `notify_msg` VALUES (295, 612, 214, '🟢 频道已解除禁用', '2023-10-29 01:15:25');
INSERT INTO `notify_msg` VALUES (296, 612, 214, '🟢 频道已被管理员上车', '2023-10-29 01:15:27');
INSERT INTO `notify_msg` VALUES (297, 612, 214, '🔴 频道已被管理员下车', '2023-10-29 01:15:29');
INSERT INTO `notify_msg` VALUES (298, 612, 214, '🚫 频道已被管理员禁用', '2023-10-29 01:15:31');
INSERT INTO `notify_msg` VALUES (299, 612, 214, '🟢 频道已解除禁用', '2023-10-29 01:15:32');
INSERT INTO `notify_msg` VALUES (300, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 01:27:28');
INSERT INTO `notify_msg` VALUES (301, 612, 212, '🟢 频道已解除禁用', '2023-10-29 01:27:29');
INSERT INTO `notify_msg` VALUES (302, 612, 212, '🟢 频道已被管理员上车', '2023-10-29 01:27:31');
INSERT INTO `notify_msg` VALUES (303, 612, 212, '🔴 频道已被管理员下车', '2023-10-29 01:27:32');
INSERT INTO `notify_msg` VALUES (304, 612, 212, '🟢 频道已被管理员上车', '2023-10-29 01:27:34');
INSERT INTO `notify_msg` VALUES (305, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 01:34:24');
INSERT INTO `notify_msg` VALUES (306, 612, 212, '🟢 频道已解除禁用', '2023-10-29 01:34:50');
INSERT INTO `notify_msg` VALUES (307, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 01:34:54');
INSERT INTO `notify_msg` VALUES (308, 612, 214, '🔴 频道已被管理员下车', '2023-10-29 01:35:50');
INSERT INTO `notify_msg` VALUES (309, 612, 214, '🟢 频道已被管理员上车', '2023-10-29 01:36:02');
INSERT INTO `notify_msg` VALUES (310, 612, 214, '🚫 频道已被管理员禁用', '2023-10-29 01:36:15');
INSERT INTO `notify_msg` VALUES (311, 612, 214, '🟢 频道已解除禁用', '2023-10-29 01:36:15');
INSERT INTO `notify_msg` VALUES (312, 612, 214, '🚫 频道已被管理员禁用', '2023-10-29 01:36:23');
INSERT INTO `notify_msg` VALUES (313, 612, 214, '🟢 频道已解除禁用', '2023-10-29 01:36:27');
INSERT INTO `notify_msg` VALUES (314, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 23:20:22');
INSERT INTO `notify_msg` VALUES (315, 612, 212, '🟢 频道已解除禁用', '2023-10-29 23:20:43');
INSERT INTO `notify_msg` VALUES (316, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 23:22:40');
INSERT INTO `notify_msg` VALUES (317, 612, 212, '🟢 频道已解除禁用', '2023-10-29 23:23:19');
INSERT INTO `notify_msg` VALUES (318, 612, 212, '🚫 频道已被管理员禁用', '2023-10-29 23:23:26');
INSERT INTO `notify_msg` VALUES (319, 612, 212, '🟢 频道已解除禁用', '2023-10-29 23:23:36');
INSERT INTO `notify_msg` VALUES (320, 612, 212, '🚫 频道已被管理员禁用', '2023-10-30 10:49:39');
INSERT INTO `notify_msg` VALUES (321, 612, 212, '🟢 频道已解除禁用', '2023-10-30 10:49:42');
INSERT INTO `notify_msg` VALUES (322, 612, 212, '待审核', '2023-10-31 22:03:02');
INSERT INTO `notify_msg` VALUES (323, 612, 214, '待审核', '2023-10-31 22:40:30');
INSERT INTO `notify_msg` VALUES (324, 612, 212, '审核成功', '2023-10-31 22:40:41');
INSERT INTO `notify_msg` VALUES (325, 612, 212, '您的频道已被管理员下车', '2023-10-31 22:40:44');
INSERT INTO `notify_msg` VALUES (326, 612, 212, '您的频道已被管理员禁用', '2023-10-31 22:40:47');
INSERT INTO `notify_msg` VALUES (327, 612, 212, '您的频道已解除禁用', '2023-10-31 22:40:48');
INSERT INTO `notify_msg` VALUES (328, 612, 214, '审核失败:头阿里斯顿看风景', '2023-10-31 22:41:04');
INSERT INTO `notify_msg` VALUES (329, 612, 214, '待审核', '2023-10-31 22:41:15');
INSERT INTO `notify_msg` VALUES (330, 612, 214, '审核成功', '2023-10-31 22:41:21');
INSERT INTO `notify_msg` VALUES (331, 612, 212, '待审核', '2023-10-31 22:41:30');
INSERT INTO `notify_msg` VALUES (332, 612, 212, '审核成功', '2023-10-31 22:41:34');
INSERT INTO `notify_msg` VALUES (333, 612, 212, '🔴 频道已被管理员下车', '2023-10-31 22:41:56');
INSERT INTO `notify_msg` VALUES (334, 612, 214, '待审核', '2023-10-31 22:53:29');
INSERT INTO `notify_msg` VALUES (335, 612, 212, '待审核', '2023-10-31 22:53:32');
INSERT INTO `notify_msg` VALUES (336, 612, 212, '审核成功', '2023-10-31 22:53:39');
INSERT INTO `notify_msg` VALUES (337, 612, 214, '审核成功', '2023-10-31 22:53:40');
INSERT INTO `notify_msg` VALUES (338, 612, 212, '🔴 频道已被管理员下车', '2023-10-31 22:54:01');
INSERT INTO `notify_msg` VALUES (339, 612, 212, '🟢 频道已被管理员上车', '2023-10-31 22:54:04');
INSERT INTO `notify_msg` VALUES (340, 612, 214, '🔴 频道已被管理员下车', '2023-10-31 22:54:11');
INSERT INTO `notify_msg` VALUES (341, 612, 212, '🚫 频道已被管理员禁用', '2023-10-31 22:54:18');
INSERT INTO `notify_msg` VALUES (342, 612, 212, '🟢 频道已解除禁用', '2023-10-31 22:55:13');
INSERT INTO `notify_msg` VALUES (343, 612, 212, '待审核', '2023-10-31 22:55:27');
INSERT INTO `notify_msg` VALUES (344, 612, 214, '待审核', '2023-10-31 22:55:31');
INSERT INTO `notify_msg` VALUES (345, 612, 214, '审核成功', '2023-10-31 22:55:44');
INSERT INTO `notify_msg` VALUES (346, 612, 212, '审核成功', '2023-10-31 22:55:45');
INSERT INTO `notify_msg` VALUES (347, 612, 214, '🚫 频道已被管理员禁用', '2023-10-31 22:56:02');
INSERT INTO `notify_msg` VALUES (348, 612, 212, '待审核', '2023-10-31 22:56:12');
INSERT INTO `notify_msg` VALUES (349, 612, 214, '🟢 频道已解除禁用', '2023-10-31 23:53:35');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
