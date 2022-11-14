# 游戏牌类

import random


# 游戏牌
class card:
    def __init__(self, name, color, point, target=None, dis=99):
        self.name = name  # 牌名
        self.color = color  # 花色
        self.point = point  # 点数
        self.target = target  # 目标
        self.dis = dis  # 距离
        self.is_shuxing = False


# 基本牌
class basic_card(card):
    def __init__(self, name, color, point):
        super(basic_card, self).__init__(name, color, point, target=None)
        if '杀' in self.name:
            self.dis = 1
            self.need_shan = 1  # 抵消杀所需闪的数量
            if ('火' or '雷') in self.name:
                self.is_shuxing = True
        if self.name == '酒':
            self.target = ['player']
        elif self.name == '桃':
            self.target = ['player', 'binsi_player']
        elif self.name == '闪':
            self.target = ['杀']


# 锦囊牌
class jinnang_card(card):
    def __init__(self, name, color, point):
        super(jinnang_card, self).__init__(name, color, point, target=None)


# 普通锦囊牌
class common_jinnang_card(jinnang_card):
    def __init__(self, name, color, point):
        super(common_jinnang_card, self).__init__(name, color, point)
        if self.name == '顺手牵羊':
            self.dis = 1
        elif self.name == '万箭齐发' or self.name == '南蛮入侵':  # 万箭齐发和南蛮入侵的目标为所有其他角色
            self.target = ['all other players']
        elif self.name == '五谷丰登' or self.name == '桃园结义':  # 桃园结义的目标为所有角色
            self.target = ['all players']
        elif self.name == '无中生有':
            self.target = ['player']
        elif self.name == '火攻':
            self.is_shuxing = True
            self.target = ['one player']


# 延时锦囊牌
class yanshi_jinnang_card(jinnang_card):
    def __init__(self, name, color, point):
        super(yanshi_jinnang_card, self).__init__(name, color, point)
        if name == '兵粮寸断':
            self.dis = 1
        elif name == '闪电':
            self.target = 'player'


# 装备牌
class equipment_card(card):
    def __init__(self, name, color, point):
        super(equipment_card, self).__init__(name, color, point, target='current_player')
        self.dis = 0
        self.player = None


# 武器牌
class weapon_card(equipment_card):
    def __init__(self, name, color, point, dis):
        super(weapon_card, self).__init__(name, color, point)
        self.dis = dis


# 防具牌
class armour_card(equipment_card):
    def __init__(self, name, color, point):
        super(armour_card, self).__init__(name, color, point)


# 进攻坐骑
class attack_horse_card(equipment_card):
    def __init__(self, name, color, point):
        super(attack_horse_card, self).__init__(name, color, point)


# 防守坐骑
class defense_horse_card(equipment_card):
    def __init__(self, name, color, point):
        super(defense_horse_card, self).__init__(name, color, point)


# 宝物牌
class treasure_card(equipment_card):
    def __init__(self, name, color, point):
        super(treasure_card, self).__init__(name, color, point)


class Get_Card_Heap:  # 摸牌堆
    def __init__(self):
        self.card_list = card_list

    def init_card_heap(self):  # 初始化摸牌堆
        card_heap_cache = []  # 创建一个缓存区用于存放牌
        for i in range(len(card_list)):
            idx = random.randint(0, len(self.card_list) - 1)
            card_heap_cache.append(self.card_list[idx])
            del self.card_list[idx]
        self.card_list = card_heap_cache.copy()
        del card_heap_cache

    def shuffle(self, left_card_heap):  # 洗牌
        card_heap_cache = []  # 创建一个缓存区用于存放牌
        for i in range(len(left_card_heap.card_list)):
            idx = random.randint(0, len(left_card_heap.card_list) - 1)
            card_heap_cache.append(left_card_heap.card_list[idx])
            del left_card_heap.card_list[idx]
        self.card_list = card_heap_cache.copy()
        del card_heap_cache

    def get_card(self, num, left_card_heap):  # 摸n张牌
        """

        num: 摸牌数量

        """
        return_card = []
        if len(self.card_list) >= num:
            return_card = self.card_list[:num]
            del self.card_list[:num]
        else:
            return_card = self.card_list
            self.shuffle(left_card_heap)
            return_card = return_card + self.get_card(num - len(return_card), left_card_heap)
        return return_card


class Identity_Card_Heap:  # 身份牌堆
    def __init__(self):
        self.card_dic = {2: ['主公', '反贼'],
                         4: ['主公', '忠臣', '内奸', '反贼'],
                         5: ['主公', '忠臣', '内奸', '反贼', '反贼'],
                         }
        self.card_list = []

    def init_card_heap(self, player_num):  # 初始化身份牌堆
        card_heap_cache = []  # 创建一个缓存区用于存放牌
        for i in range(len(self.card_dic[player_num])):
            idx = random.randint(0, len(self.card_dic[player_num]) - 1)
            card_heap_cache.append(self.card_dic[player_num][idx])
            del self.card_dic[player_num][idx]
        self.card_list = card_heap_cache.copy()
        del card_heap_cache

    def get_identity(self):
        return_card = self.card_list[0]
        del self.card_list[0]
        return return_card


class Left_Card_Heap:  # 弃牌堆
    def __init__(self):
        self.card_list = []


card_list = [basic_card('普通杀', '黑桃', 7),
             basic_card('普通杀', '黑桃', 8),
             basic_card('普通杀', '黑桃', 8),
             basic_card('普通杀', '黑桃', 9),
             basic_card('普通杀', '黑桃', 9),
             basic_card('普通杀', '黑桃', 10),
             basic_card('普通杀', '黑桃', 10),
             basic_card('普通杀', '红桃', 10),
             basic_card('普通杀', '红桃', 10),
             basic_card('普通杀', '红桃', 11),
             basic_card('普通杀', '梅花', 2),
             basic_card('普通杀', '梅花', 3),
             basic_card('普通杀', '梅花', 4),
             basic_card('普通杀', '梅花', 5),
             basic_card('普通杀', '梅花', 6),
             basic_card('普通杀', '梅花', 7),
             basic_card('普通杀', '梅花', 8),
             basic_card('普通杀', '梅花', 8),
             basic_card('普通杀', '梅花', 9),
             basic_card('普通杀', '梅花', 9),
             basic_card('普通杀', '梅花', 10),
             basic_card('普通杀', '梅花', 10),
             basic_card('普通杀', '梅花', 11),
             basic_card('普通杀', '梅花', 11),
             basic_card('普通杀', '方块', 6),
             basic_card('普通杀', '方块', 7),
             basic_card('普通杀', '方块', 8),
             basic_card('普通杀', '方块', 9),
             basic_card('普通杀', '方块', 10),
             basic_card('普通杀', '方块', 13),

             basic_card('火杀', '红桃', 4),
             basic_card('火杀', '红桃', 7),
             basic_card('火杀', '红桃', 10),
             basic_card('火杀', '方块', 4),
             basic_card('火杀', '方块', 5),

             basic_card('雷杀', '黑桃', 4),
             basic_card('雷杀', '黑桃', 5),
             basic_card('雷杀', '黑桃', 6),
             basic_card('雷杀', '黑桃', 7),
             basic_card('雷杀', '黑桃', 8),
             basic_card('雷杀', '梅花', 5),
             basic_card('雷杀', '梅花', 6),
             basic_card('雷杀', '梅花', 7),
             basic_card('雷杀', '梅花', 8),

             basic_card('闪', '红桃', 2),
             basic_card('闪', '红桃', 2),
             basic_card('闪', '红桃', 8),
             basic_card('闪', '红桃', 9),
             basic_card('闪', '红桃', 11),
             basic_card('闪', '红桃', 12),
             basic_card('闪', '红桃', 13),
             basic_card('闪', '方块', 2),
             basic_card('闪', '方块', 2),
             basic_card('闪', '方块', 3),
             basic_card('闪', '方块', 4),
             basic_card('闪', '方块', 5),
             basic_card('闪', '方块', 6),
             basic_card('闪', '方块', 6),
             basic_card('闪', '方块', 7),
             basic_card('闪', '方块', 7),
             basic_card('闪', '方块', 8),
             basic_card('闪', '方块', 8),
             basic_card('闪', '方块', 9),
             basic_card('闪', '方块', 10),
             basic_card('闪', '方块', 10),
             basic_card('闪', '方块', 11),
             basic_card('闪', '方块', 11),
             basic_card('闪', '方块', 11),

             basic_card('桃', '红桃', 3),
             basic_card('桃', '红桃', 4),
             basic_card('桃', '红桃', 5),
             basic_card('桃', '红桃', 6),
             basic_card('桃', '红桃', 6),
             basic_card('桃', '红桃', 7),
             basic_card('桃', '红桃', 8),
             basic_card('桃', '红桃', 9),
             basic_card('桃', '红桃', 12),
             basic_card('桃', '方块', 2),
             basic_card('桃', '方块', 3),
             basic_card('桃', '方块', 12),

             basic_card('酒', '黑桃', 3, ),
             basic_card('酒', '黑桃', 9, ),
             basic_card('酒', '梅花', 3, ),
             basic_card('酒', '梅花', 9, ),
             basic_card('酒', '方块', 9, ),

             weapon_card('诸葛连弩', '梅花', 1, 1),
             weapon_card('诸葛连弩', '方块', 1, 1),
             weapon_card('雌雄双股剑', '黑桃', 2, 2),
             weapon_card('寒冰剑', '黑桃', 2, 2),
             weapon_card('青釭剑', '黑桃', 2, 2),
             weapon_card('古锭刀', '黑桃', 2, 2),
             weapon_card('青龙偃月刀', '黑桃', 5, 3),
             weapon_card('贯石斧', '方块', 5, 3),
             weapon_card('丈八蛇矛', '黑桃', 12, 3),
             weapon_card('方天画戟', '方块', 12, 4),
             weapon_card('朱雀羽扇', '方块', 1, 4),
             weapon_card('麒麟弓', '红桃', 5, 5),

             armour_card('八卦阵', '黑桃', 2),
             armour_card('八卦阵', '梅花', 2),
             armour_card('白银狮子', '梅花', 1),
             armour_card('仁王盾', '梅花', 2),
             armour_card('藤甲', '黑桃', 2),
             armour_card('藤甲', '梅花', 2),

             attack_horse_card('大宛', '黑桃', 13),
             attack_horse_card('赤兔', '红桃', 5),
             attack_horse_card('紫骍', '黑桃', 13),

             defense_horse_card('绝影', '黑桃', 5),
             defense_horse_card('爪黄飞电', '红桃', 13),
             defense_horse_card('的卢', '梅花', 5),
             defense_horse_card('骅骝', '方块', 13),

             treasure_card('木牛流马', '方块', 5),

             common_jinnang_card('决斗', '黑桃', 1),
             common_jinnang_card('决斗', '梅花', 1),
             common_jinnang_card('决斗', '方块', 1),

             common_jinnang_card('无中生有', '红桃', 7),
             common_jinnang_card('无中生有', '红桃', 8),
             common_jinnang_card('无中生有', '红桃', 9),
             common_jinnang_card('无中生有', '红桃', 11),

             common_jinnang_card('过河拆桥', '黑桃', 3),
             common_jinnang_card('过河拆桥', '黑桃', 4),
             common_jinnang_card('过河拆桥', '黑桃', 12),
             common_jinnang_card('过河拆桥', '红桃', 12),
             common_jinnang_card('过河拆桥', '梅花', 3),
             common_jinnang_card('过河拆桥', '梅花', 4),

             common_jinnang_card('顺手牵羊', '黑桃', 3),
             common_jinnang_card('顺手牵羊', '黑桃', 4),
             common_jinnang_card('顺手牵羊', '黑桃', 11),
             common_jinnang_card('顺手牵羊', '方块', 3),
             common_jinnang_card('顺手牵羊', '方块', 4),

             common_jinnang_card('借刀杀人', '梅花', 12),
             common_jinnang_card('借刀杀人', '梅花', 13),

             common_jinnang_card('南蛮入侵', '黑桃', 7),
             common_jinnang_card('南蛮入侵', '黑桃', 12),
             common_jinnang_card('南蛮入侵', '梅花', 7),

             common_jinnang_card('万箭齐发', '红桃', 1),

             common_jinnang_card('桃园结义', '红桃', 1),

             common_jinnang_card('五谷丰登', '红桃', 3),
             common_jinnang_card('五谷丰登', '红桃', 4),

             common_jinnang_card('无懈可击', '黑桃', 11),
             common_jinnang_card('无懈可击', '黑桃', 13),
             common_jinnang_card('无懈可击', '梅花', 12),
             common_jinnang_card('无懈可击', '梅花', 13),
             common_jinnang_card('无懈可击', '方块', 12),
             common_jinnang_card('无懈可击', '红桃', 1),
             common_jinnang_card('无懈可击', '红桃', 12),

             common_jinnang_card('火攻', '红桃', 2),
             common_jinnang_card('火攻', '红桃', 3),
             common_jinnang_card('火攻', '方块', 12),

             common_jinnang_card('铁索连环', '黑桃', 11),
             common_jinnang_card('铁索连环', '黑桃', 12),
             common_jinnang_card('铁索连环', '梅花', 10),
             common_jinnang_card('铁索连环', '梅花', 11),
             common_jinnang_card('铁索连环', '梅花', 12),
             common_jinnang_card('铁索连环', '梅花', 13),

             yanshi_jinnang_card('乐不思蜀', '黑桃', 6),
             yanshi_jinnang_card('乐不思蜀', '红桃', 6),
             yanshi_jinnang_card('乐不思蜀', '梅花', 6),

             yanshi_jinnang_card('闪电', '黑桃', 1),
             yanshi_jinnang_card('闪电', '红桃', 12),

             yanshi_jinnang_card('兵粮寸断', '黑桃', 10),
             yanshi_jinnang_card('兵粮寸断', '梅花', 4),

             ]
