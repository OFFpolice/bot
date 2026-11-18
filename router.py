# 路由
from public.method import Router
from views.client import *
from views.admin import *

router = Router()
router.add_route('r/首页', Index, 'index')
router.add_route('r/频道', Channel, 'index')
router.add_route('r/频道车厢', Channel, 'fleet_info')
router.add_route('r/频道申请', Channel, 'add_fleet')
router.add_route('r/频道申请提交', Channel, 'submit_fleet')

router.add_route('a/管理首页', Admin, 'index')
router.add_route('a/初始化菜单', Admin, 'initialization')
router.add_route('a/机器人配置', Admin, 'config')
router.add_route('a/修改配置', Admin, 'modifBot')
router.add_route('a/审核拒绝词', Admin, 'reviewRejectionWords')
router.add_route('a/增审核拒绝词', Admin, 'delReviewRejectionWords')
router.add_route('a/删审核拒绝词', Admin, 'delReviewRejectionWords')

router.add_route('a/广告管理', Advertising, 'index')
router.add_route('a/广告输入', Advertising, 'adInput')
router.add_route('a/删广告词', Advertising, 'delAdvertising')

router.add_route('a/车队管理', Car, 'index')
router.add_route('a/车队输入', Car, 'inputBot')
router.add_route('a/频道车队管理', Car, 'channel_car')
router.add_route('a/频道车队详情', Car, 'channel_fleet_info')
router.add_route('a/频道车队频道详细', Car, 'channel_info')
router.add_route('a/频道管理频道状态', Car, 'channel_fleet_state')
router.add_route('a/频道管理上下车', Car, 'downGroup')
router.add_route('a/频道管理启禁群', Car, 'banGroup')


router.add_route('a/通过审核', Review, 'passReview')
router.add_route('a/拒绝审核', Review, 'rejectReview')
router.add_route('a/拒绝原因', Review, 'rejectReason')
router.add_route('a/自定义原因', Review, 'inputBot')
router.add_route('a/拒绝返回', Review, 'rejectBack')
router.add_route('a/审核禁群', Review, 'banGroup')
router.add_route('a/审核下车', Review, 'downGroup')

router.add_route('a/群频管理', Group, 'index')
router.add_route('a/群频管理输入', Group, 'inputBot')
router.add_route('a/群频详情', Group, 'groupInfo')
router.add_route('a/群频管理启禁群', Group, 'banGroup')

router.add_route('a/用户管理', User, 'getUser')#数据抓取
router.add_route('a/用户输入', User, 'inputBot')
router.add_route('a/用户详情', User, 'userInfo')#数据抓取
router.add_route('a/设置管理员', User, 'setAdmin')
router.add_route('a/禁用户', User, 'banUser')
router.add_route('a/返回', User, 'backReview')
router.add_route('a/删除当前消息', User, 'backReview')

router.add_route('a/Bot黑名单', BotBlacklist, 'index')
router.add_route('a/Bot输入', BotBlacklist, 'botInput')
router.add_route('a/删Bot黑名单', BotBlacklist, 'delBotBlacklist')



