import numpy as np
from typing import List
from player import Player
from skill import Skill
import process


def check_skill(time, current_player, target_player, Items):  # 检查是否有技能能发动
    # 先将场上全部武将技能放在列表中
    AllSkills: List[Skill] = []
    for p in Items.PlayerList:
        for skill in p.skills:
            AllSkills.append(skill)
    for s in AllSkills:
        if s.check_time(time) and s.check_con(Items) and s.state():
            s.trigger(Items)


def wuxie(Items, card, wuxie_count):
    for j in Items.PlayerList:
        if '无懈可击' not in [w.name for w in j.HandCards_area]:
            continue
        print('{}号位手牌为{}'.format(j.idx, [[card.name, card.color, card.point] for card in j.HandCards_area]))
        wuxie = eval(input('{}号位是否使用无懈可击, 0表示不使用无懈可击, i表示使用第i张牌'.format(j.idx)))
        if not wuxie:
            continue
        wuxie = j.HandCards_area[wuxie - 1]
        if wuxie.name == '无懈可击':
            wuxie.target = card
            wuxie_count += process.use_card_process(wuxie, j, Items)
            if wuxie_count:
                return 0
    return 1


def isAreaEmpty(player: Player) -> bool:  # 判断玩家区域内是否有牌
    return len(player.HandCards_area) == 0 and len(player.pandin_area) == 0 and np.array(
        [v.name for k, v in player.equipment_area.items()]).all() is None


def cal_dis(player, player_list):  # 计算距离
    res_next = {}
    res_pre = {}
    res = {}
    player_tmp = player
    dis = 0
    delta = 0
    if player.equipment_area['进攻坐骑'].name is not None:
        delta -= 1
    while player_tmp.next != player:
        dis += 1
        if player_tmp.next.equipment_area['防御坐骑'].name is not None:
            res_next[player_tmp.next.idx] = max(dis + 1 - delta, 1)
        else:
            res_next[player_tmp.next.idx] = max(dis - delta, 1)
        player_tmp = player_tmp.next

    player_tmp = player
    dis = 0
    while player_tmp.pre != player:
        dis += 1
        if player_tmp.pre.equipment_area['防御坐骑'].name is not None:
            res_pre[player_tmp.pre.idx] = max(dis + 1 - delta, 1)
        else:
            res_pre[player_tmp.pre.idx] = max(dis - delta, 1)
        player_tmp = player_tmp.pre

    for key in res_next.keys():
        res[player_list[key - 1]] = min(res_next[key], res_pre[key])

    return res


def PrintPlayer(player):  # 打印玩家信息
    hengzhi_dic = {True: '是', False: '否'}
    print('{}号位'.format(player.idx))
    print('武将为:{}'.format(player.commander.name))
    print('技能为:{}'.format([skill.name for skill in player.skills]))
    print('当前体力值为:{}/{}'.format(player.current_HP, player.max_HP))
    print('是否被横置:{}'.format(hengzhi_dic[player.hengzhi]))
    print('装备区有武器牌:{},防具牌:{}, 进攻坐骑:{}, 防御坐骑:{},宝物:{}'.format(player.equipment_area['武器'].name,
                                                                                 player.equipment_area['防具'].name,
                                                                                 player.equipment_area['进攻坐骑'].name,
                                                                                 player.equipment_area['防御坐骑'].name,
                                                                                 player.equipment_area['宝物'].name))


# 检查是否满足游戏胜利条件
def check_vic(dead_player: Player, player_list) -> int:
    """

    dead_player: 死亡角色
    return: 1: 主公和忠臣获胜
            2: 反贼获胜
            3: 内奸获胜
    """
    if dead_player.identity == '主公':
        if len(player_list) == 1 and player_list[0].identity == '内奸':
            return 3
        else:
            return 2
    elif (dead_player.identity != '主公') and ('反贼' not in [player.identity for player in player_list]) and (
            '内奸' not in [player.identity for player in player_list]):
        return 1
    else:
        return 0
