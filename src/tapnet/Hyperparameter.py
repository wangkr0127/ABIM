Steps = 20
nclass = 2

GPU_USED = False
# GPU_USED = True

game_scene = '3s_vs_3z'
# game_scene = '2m_vs_1z'

our_side_num_3s_vs_3z, enemy_num_3s_vs_3z = 3, 3
threshold_3s_vs_3z = 0.38

our_side_num_2m_vs_1z, enemy_num_2m_vs_1z = 2, 1
threshold_2m_vs_1z = 0.39

'''3s_vs_3z:'''
bench_noCrash0_3s_vs_3z = []

'''2m_vs_1z: '''
bench_noCrash0_2m_vs_1z = []

bench_noCrash = bench_noCrash0_2m_vs_1z

if game_scene == '3s_vs_3z':
    bench_noCrash = bench_noCrash0_3s_vs_3z
