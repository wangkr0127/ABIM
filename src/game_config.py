import time

maps = ['2m_vs_1z', '3s_vs_3z', '3m', '8m', 'so_many_baneling']
mapId = 1

code_start_time = time.time()
code_timeout = 1  # 设置超时时间为1秒
code_timeout = code_timeout * 60 * 10  # 设置超时时间为10min
# code_timeout = code_timeout * 60 * 15  # 设置超时时间为15min -- TapNet


action_interval = 5
llm_window_size = 10

LLM_type = 'openai'
# LLM_type = 'zhipuai'

inProcess_judge_steps = 20
game_scene = maps[mapId]
our_side_num_3s_vs_3z, enemy_num_3s_vs_3z = 3, 3
our_side_num_2m_vs_1z, enemy_num_2m_vs_1z = 2, 1
nclass = 2

'''3s_vs_3z:'''
bench_noCrash0_3s_vs_3z = []

'''2m_vs_1z: '''
bench_noCrash0_2m_vs_1z = []

bench_noCrash = bench_noCrash0_2m_vs_1z

if game_scene == '3s_vs_3z':
    bench_noCrash = bench_noCrash0_3s_vs_3z