import openai
from pymarl2.src import game_config
from pymarl2.src.chatGPT.ChatConfig import generate_prompts, model_name, temperature
from pymarl2.src.chatGPT.get_topu_by_rule import get_topu_by_rule
from pymarl2.src.game_config import LLM_type
openai.api_key = ''
IN_PROCESS_MODE = 1
END_MODE = 2

def query_micro(user_input, mode, max_retries=1):
    """
    query方法,用于对话
    :param user_input: 用户输入
    :return: 机器人回复
    """

    system_prompt, example_input_prompt_list, example_output_prompt_list = generate_prompts(mode)
    # system_prompt: 系统提示语
    # example_prompt: 例子, 用于初始化对话

    # 重置 messages 列表
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": example_input_prompt_list[0]},
                {"role": "assistant", "content": example_output_prompt_list[0]},
                {"role": "user", "content": example_input_prompt_list[1]},
                {"role": "assistant", "content": example_output_prompt_list[1]},
                {"role": "user", "content": example_input_prompt_list[2]},
                {"role": "assistant", "content": example_output_prompt_list[2]},
                {"role": "user", "content": example_input_prompt_list[3]},
                {"role": "assistant", "content": example_output_prompt_list[3]},
                {"role": "user", "content": example_input_prompt_list[4]},
                {"role": "assistant", "content": example_output_prompt_list[4]},
                {"role": "user", "content": user_input}]

    # 尝试发送请求并获取回复
    if LLM_type == 'zhipuai':
        return post_query_Zhipu(messages)
    elif LLM_type == 'openai':
        return post_query_chatGPT(messages)

def query_topology(user_input, ways):
    if ways == 'rule':
        return get_topu_by_rule(user_input)

    """
    query方法,用于对话gpt_sentence_results_end
    :param user_input: 用户输入
    :return: 机器人回复
    """
    system_prompt = r"""
You already know that there are the following four types of micromanagement, and the mapping relationship is as follows: A refers to Kiting, B refers to scattered attack, C refers to concentrated attack, D refers to alternate attack micromanagement.
You will get a paragraph and get the execution order of these micromanagement based on this paragraph. 
If none of the micro-operations are executed, an empty list will be output, like [].
    """

    example_input_prompt = r"""
1. Micromanagement usage: The combat units on our side use multiple types of micromanagement techniques.
   - The initial actions of our combat units indicate the usage of Concentrated Attack Micromanagement. They start with a coordinated attack on the enemy units.
   - As the game progresses, our combat units switch to Kiting Micromanagement. They continuously move and attack, maintaining their maximum range and minimizing damage taken.
   - Towards the end of the game, our combat units switch to Alternate Attack Micromanagement. They swiftly move after attacking to maximize their effective output and reduce damage taken.
The order of micromanagement techniques used by our combat units is: Concentrated Attack Micromanagement -> Kiting Micromanagement -> Alternate Attack Micromanagement.
    """

    example_output_prompt = r"""
[B, A, D]
    """

    # system_prompt: 系统提示语
    # example_prompt: 例子, 用于初始化对话, 格式为[用户输入, 机器人回复]
    example_prompt = [example_input_prompt, example_output_prompt]

    # 重置 messages 列表
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": example_prompt[0]},
                {"role": "assistant", "content": example_prompt[1]}, {"role": "user", "content": user_input}]

    # 尝试发送请求并获取回复
    if LLM_type == 'zhipuai':
        return post_query_Zhipu(messages)
    elif LLM_type == 'openai':
        return post_query_chatGPT(messages)

def build_user_input(position_agents, position_enemies, actions_agents):
    game_scenery = game_config.maps[game_config.mapId]
    user_input_prompt = ''
    if game_scenery == '3s_vs_3z':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.(need first Scatter and then Kiting)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
    """
    elif game_scenery == '2m_vs_1z':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is two Marines, the opponent is one Zealot.(need first Scatter and then Alternate Attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
    """
    elif game_scenery == '3m':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is three Marines, the opponent is three Marines.(need Concentrated attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
    """
    elif game_scenery == '8m':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is eight Marines, the opponent is eight Marines.(need Concentrated attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
    """
    elif game_scenery == 'so_many_baneling':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is seven Zealots, the opponent is thirty-two Banelings.(need Scatter attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
    """
    return user_input_prompt.format(position_agents=position_agents, position_enemies=position_enemies, actions_agents=actions_agents)

def build_user_input_with_inProcessInfo(position_agents, position_enemies, actions_agents, in_process_topo):
    game_scenery = game_config.maps[game_config.mapId]
    user_input_prompt = ''
    if game_scenery == '3s_vs_3z':
        user_input_prompt = r"""
--- example input ---
--- StarCraft II Game Summary ---
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The following micromanagement execution results are our previous analysis results, which you can use as a reference: {in_process_topo}
    """
    elif game_scenery == '2m_vs_1z':
        user_input_prompt = r"""
--- example input ---
--- StarCraft II Game Summary ---
The two sides fighting: our side is two Marines, the opponent is one Zealot.(need first Scatter and then Alternate Attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The following micromanagement execution results are our previous analysis results, which you can use as a reference: {in_process_topo}
    """
    elif game_scenery == '3m':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is three Marines, the opponent is three Marines.(need Concentrated attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The following micromanagement execution results are our previous analysis results, which you can use as a reference: {in_process_topo}
    """
    elif game_scenery == '8m':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is eight Marines, the opponent is eight Marines.(need Concentrated attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The following micromanagement execution results are our previous analysis results, which you can use as a reference: {in_process_topo}
    """
    elif game_scenery == 'so_many_baneling':
        user_input_prompt = r"""
--- StarCraft II Game Summary ---
The two sides fighting: our side is seven Zealots, the opponent is thirty-two Banelings.(need Scatter attack)
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: {position_agents}.
The coordinate position sequence of enemy combat units: {position_enemies}.
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: {actions_agents}.
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The following micromanagement execution results are our previous analysis results, which you can use as a reference: {in_process_topo}
    """
    return user_input_prompt.format(position_agents=position_agents, position_enemies=position_enemies, actions_agents=actions_agents, in_process_topo=in_process_topo)

def query_gpt_end(position_agents, position_enemies, actions_agents, in_process_topo_analysis):
    if in_process_topo_analysis != '':
        user_input_with_inProcessInfo = build_user_input_with_inProcessInfo(position_agents, position_enemies, actions_agents, in_process_topo_analysis)
        return query_micro(user_input_with_inProcessInfo, END_MODE)
    user_input = build_user_input(position_agents, position_enemies, actions_agents)
    return query_micro(user_input, END_MODE)

def query_gpt_in_process(position_agents, position_enemies, actions_agents):
    user_input = build_user_input(position_agents, position_enemies, actions_agents)
    return query_micro(user_input, IN_PROCESS_MODE)



def post_query_chatGPT(messages):
    try:
        output = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=temperature
        )
        answer = output["choices"][0]["message"]["content"]
        return answer
    except Exception as e:
        # 输出错误信息
        print(f"Error when calling the OpenAI API: {e}")
        return "I'm sorry, but I am unable to provide a response at this time due to technical difficulties."

def post_query_Zhipu(messages):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key="")  # 填写您自己的APIKey
    output = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
    )
    return output.choices [0].message.content