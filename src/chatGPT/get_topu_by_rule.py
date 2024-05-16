maps = {'A': 'Kiting', 'B': 'scattered', 'C': 'concentrated', 'D': 'alternate'}

def get_topu_by_rule(summary_gpt_res):
    topo = []
    index_A = -1
    index_B = -1
    index_C = -1
    index_D = -1
    if 'Kiting' in summary_gpt_res or 'kiting' in summary_gpt_res:
        index_1, index_2 = 999999, 999999
        if 'Kiting' in summary_gpt_res:
            index_1 = summary_gpt_res.index("Kiting")
        if 'kiting' in summary_gpt_res:
            index_2 = summary_gpt_res.index("kiting")
        index_A = min(index_1, index_2)
    if 'Scatter' in summary_gpt_res or 'scatter' in summary_gpt_res:
        index_1, index_2 = 999999, 999999
        if 'Scatter' in summary_gpt_res:
            index_1 = summary_gpt_res.index("Scatter")
        if 'scatter' in summary_gpt_res:
            index_2 = summary_gpt_res.index("scatter")
        index_B = min(index_1, index_2)
    if 'Concentrate' in summary_gpt_res or 'concentrate' in summary_gpt_res:
        index_1, index_2 = 999999, 999999
        if 'Concentrate' in summary_gpt_res:
            index_1 = summary_gpt_res.index("Concentrate")
        if 'concentrate' in summary_gpt_res:
            index_2 = summary_gpt_res.index("concentrate")
        index_C = min(index_1, index_2)
    if 'Alternate' in summary_gpt_res or 'alternate' in summary_gpt_res:
        index_1, index_2 = 999999, 999999
        if 'Alternate' in summary_gpt_res:
            index_1 = summary_gpt_res.index("Alternate")
        if 'alternate' in summary_gpt_res:
            index_2 = summary_gpt_res.index("alternate")
        index_D = min(index_1, index_2)

    indices = {'A': index_A, 'B': index_B, 'C': index_C, 'D': index_D}
    # 过滤掉值为-1的条目
    filtered_indices = {k: v for k, v in indices.items() if v != -1}
    filtered_indices = {k: v for k, v in filtered_indices.items() if v != 999999}
    # 按值排序
    sorted_indices = sorted(filtered_indices.items(), key=lambda item: item[1])
    # 提取排序后的键
    order = [i[0] for i in sorted_indices]

    topo = order

    return topo

if __name__ == '__main__':
    summary_gpt_res = 'Micromanagement usage: Concentrated Attack Micromanagement is used.'
    print(get_topu_by_rule(summary_gpt_res))