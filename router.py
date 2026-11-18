# Маршрутизация
from public.method import Router
from views.client import *
from views.admin import *

router = Router()
router.add_route('r/главная', Index, 'index')
router.add_route('r/каналы', Channel, 'index')
router.add_route('r/подборка', Channel, 'fleet_info')
router.add_route('r/заявка', Channel, 'add_fleet')
router.add_route('r/отправка', Channel, 'submit_fleet')

router.add_route('a/админ', Admin, 'index')
router.add_route('a/меню', Admin, 'initialization')
router.add_route('a/настройки', Admin, 'config')
router.add_route('a/ред_настр', Admin, 'modifBot')
router.add_route('a/отказы', Admin, 'reviewRejectionWords')
router.add_route('a/доб_отказ', Admin, 'delReviewRejectionWords')
router.add_route('a/уд_отказ', Admin, 'delReviewRejectionWords')

router.add_route('a/рекл', Advertising, 'index')
router.add_route('a/ввод_рекл', Advertising, 'adInput')
router.add_route('a/уд_рекл', Advertising, 'delAdvertising')

router.add_route('a/подб', Car, 'index')
router.add_route('a/ввод_подб', Car, 'inputBot')
router.add_route('a/подб_кан', Car, 'channel_car')
router.add_route('a/детали_п', Car, 'channel_fleet_info')
router.add_route('a/кан_подб', Car, 'channel_info')
router.add_route('a/статус_п', Car, 'channel_fleet_state')
router.add_route('a/состав_п', Car, 'downGroup')
router.add_route('a/бан_п', Car, 'banGroup')


router.add_route('a/одобрить', Review, 'passReview')
router.add_route('a/отклонить', Review, 'rejectReview')
router.add_route('a/причина', Review, 'rejectReason')
router.add_route('a/своя_прич', Review, 'inputBot')
router.add_route('a/возврат', Review, 'rejectBack')
router.add_route('a/бан_мод', Review, 'banGroup')
router.add_route('a/снять_мод', Review, 'downGroup')

router.add_route('a/группы', Group, 'index')
router.add_route('a/ввод_гр', Group, 'inputBot')
router.add_route('a/инфо_гр', Group, 'groupInfo')
router.add_route('a/бан_гр', Group, 'banGroup')

router.add_route('a/юзеры', User, 'getUser')# Выборка пользователей
router.add_route('a/ввод_юз', User, 'inputBot')
router.add_route('a/инфо_юз', User, 'userInfo')# Карточка пользователя
router.add_route('a/адм_юз', User, 'setAdmin')
router.add_route('a/бан_юз', User, 'banUser')
router.add_route('a/назад', User, 'backReview')
router.add_route('a/удалить', User, 'backReview')

router.add_route('a/чс_ботов', BotBlacklist, 'index')
router.add_route('a/ввод_чс', BotBlacklist, 'botInput')
router.add_route('a/уд_чс', BotBlacklist, 'delBotBlacklist')
