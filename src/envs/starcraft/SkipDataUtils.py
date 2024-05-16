from pymarl2.src import game_config
import numpy as np

def list_remove_duplicates(two_d_list):
    seen = set()
    result = []

    for sublist in two_d_list:
        tuple_representation = tuple(sublist)
        if tuple_representation not in seen:
            seen.add(tuple_representation)
            result.append(sublist)
    return result

def remove_duplicates(positions):
    ret = []
    for step in positions:
        ret.append(list_remove_duplicates(step))
    return ret

def add_null(positions, num):
    ret = []
    for step in positions:
        cur_step = step
        while len(cur_step) < num:
            cur_step.append([-1, -1])
        ret.append(step)
    return ret

def transform_col(position_agent, position_enemy):

    our_side_num, enemy_num = [], []
    if game_config.game_scene == '3s_vs_3z':
        our_side_num, enemy_num = game_config.our_side_num_3s_vs_3z, game_config.enemy_num_3s_vs_3z
    elif game_config.game_scene == '2m_vs_1z':
        our_side_num, enemy_num = game_config.our_side_num_2m_vs_1z, game_config.enemy_num_2m_vs_1z
    DIMENSION = (our_side_num + enemy_num) * 2

    ret = []
    cycle_agents = position_agent
    cycle_enemies = position_enemy
    var = []
    for i in range(DIMENSION):
        var.append([])
    for i in range(game_config.inProcess_judge_steps):
        if game_config.game_scene == '3s_vs_3z':
            var[0].append(cycle_agents[i][0][0])
            var[1].append(cycle_agents[i][0][1])
            var[2].append(cycle_agents[i][1][0])
            var[3].append(cycle_agents[i][1][1])
            var[4].append(cycle_agents[i][2][0])
            var[5].append(cycle_agents[i][2][1])
            var[6].append(cycle_enemies[i][0][0])
            var[7].append(cycle_enemies[i][0][1])
            var[8].append(cycle_enemies[i][1][0])
            var[9].append(cycle_enemies[i][1][1])
            var[10].append(cycle_enemies[i][2][0])
            var[11].append(cycle_enemies[i][2][1])
        elif game_config.game_scene == '2m_vs_1z':
            var[0].append(cycle_agents[i][0][0])
            var[1].append(cycle_agents[i][0][1])
            var[2].append(cycle_agents[i][1][0])
            var[3].append(cycle_agents[i][1][1])
            var[4].append(cycle_enemies[i][0][0])
            var[5].append(cycle_enemies[i][0][1])
    ret = []
    for wd in range(DIMENSION):
        ret.append(var[wd])
    return ret

def parseSeqData(position_agent_origin, position_enemy_origin):
    game_scene = game_config.game_scene
    position_agent = remove_duplicates(position_agent_origin)
    position_enemy = remove_duplicates(position_enemy_origin)
    our_side_num, enemy_num = [], []
    if game_scene == '3s_vs_3z':
        our_side_num, enemy_num = game_config.our_side_num_3s_vs_3z, game_config.enemy_num_3s_vs_3z
    elif game_scene == '2m_vs_1z':
        our_side_num, enemy_num = game_config.our_side_num_2m_vs_1z, game_config.enemy_num_2m_vs_1z
    position_agent = add_null(position_agent, our_side_num)
    position_enemy = add_null(position_enemy, enemy_num)
    format_data = transform_col(position_agent, position_enemy)
    return np.transpose(format_data, axes=(1, 0))