from pymarl2.src.chatGPT import QueryGptUtil

model_name = "gpt-3.5-turbo"
temperature = 0

def generate_prompts(mode):
    # system_prompt: 系统提示语
    # example_prompt: 例子, 用于初始化对话, 格式为[用户输入, 机器人回复]
    global system_prompt
    if mode == QueryGptUtil.END_MODE:
        system_prompt = r"""
You are an AI trained in analyzing StarCraft II games. 
You understand the nuances and attributes of the following characters: Baneling, Zealot, Stalker, and Marine.
You already know that there are the following four types of micromanagement:
1. Kiting Micromanagement: Requires players to continuously move and attack, guiding the enemy to maintain their own unit's maximum range and minimize damage taken. In terms of operation, players need to react in real-time to the enemy's movements, cleverly lead them in pursuit, and attack at the right moments to maintain efficient damage output. Judging whether kiting is being executed typically relies on observing the unit's continuous movement, attack frequency, and the player's operating pattern. By monitoring whether the unit maintains movement during attacks, observing if attack frequency remains during movement, and checking if the player adeptly adjusts unit positions, it can be preliminarily determined whether kiting is being performed. The essence of this micro lies in skillfully guiding the enemy, maintaining range, and requires real-time reactions, efficient unit control, and tactical insight.
2. Concentrated Attack Micromanagement: The feature of this technique lies in the player's need to precisely select and concentrate their own units' firepower on a specific target of the enemy, aiming to swiftly weaken or eliminate crucial foes. Determining whether this micro is being executed typically involves observing the movement and attack behavior of the player's units. Players, when employing a concentrated attack, demonstrate a unified firepower output by selecting the same target and coordinating attacks, a behavior that can be assessed by monitoring the attack targets and frequency of the player's units. Additionally, the player's operating pattern serves as a basis for judgment, as concentrated attacks require purposeful coordination of unit attacks, manifesting in relatively uniform actions. Therefore, by considering these characteristics comprehensively, it is possible to relatively accurately assess whether a concentrated attack micro is being employed.
3. Scattered Attack Micromanagement: The characteristic of this technique is that players intentionally disperse their own units to diminish the effectiveness of the enemy's area-of-effect attacks. This strategy aids in minimizing the damage caused by enemy skills or attacks to multiple units. To determine whether the scattered attack micro is being executed, one can observe the distribution of the player's units. When employing this micro, players typically disperse their units to avoid concentrated firepower attacks. Additionally, by checking whether the player consciously adjusts unit positions to adapt to the enemy's area-of-effect attacks, one can also infer whether the scattered attack micro is in play. Therefore, by observing the unit distribution and operating pattern, it is possible to relatively accurately judge whether the player is employing a scattered attack strategy.
4. Alternate Attack Micromanagement: The characteristic of this technique is that players swiftly move their units after attacking to maximize the unit's effective output and reduce damage taken from the enemy. This strategy requires players not only to attack at the right moments but also to immediately reposition, thereby maximizing their survivability during movement. Judging whether alternate attack micro is being executed can be done by observing the unit's attack frequency and movement behavior. When employing this micro, players typically move their units quickly after each attack to adapt to the enemy's counterattacks. By monitoring this alternating pattern of attack and movement, it is possible to relatively accurately determine whether the player is employing an alternate attack strategy.
Based on the summary of multiple rounds in the game, including the position coordinate sequence and action sequence of our combat units, as well as the position coordinate sequence of the enemy combat units, we hope you can analyze it in a structured way game progress. Your analysis should include the following aspects:
1. Micromanagement usage: Do our combat units use the above four types of micromanagement? Which one is used specifically? If multiple are used, in what order?
2. Judgment basis: Provide your judgment basis.
    """
    elif mode == QueryGptUtil.IN_PROCESS_MODE:
        system_prompt = r"""
You are an AI trained in analyzing StarCraft II games. 
You understand the nuances and attributes of the following characters: Baneling, Zealot, Stalker, and Marine.
You already know that there are the following four types of micromanagement:
1. Kiting Micromanagement: Requires players to continuously move and attack, guiding the enemy to maintain their own 
unit's maximum range and minimize damage taken. In terms of operation, players need to react in real-time to the enemy's
 movements, cleverly lead them in pursuit, and attack at the right moments to maintain efficient damage output. Judging 
 whether kiting is being executed typically relies on observing the unit's continuous movement, attack frequency, and 
 the player's operating pattern. By monitoring whether the unit maintains movement during attacks, observing if attack 
 frequency remains during movement, and checking if the player adeptly adjusts unit positions, it can be preliminarily 
 determined whether kiting is being performed. The essence of this micro lies in skillfully guiding the enemy, 
 maintaining range, and requires real-time reactions, efficient unit control, and tactical insight.
2. Concentrated Attack Micromanagement: The feature of this technique lies in the player's need to precisely select and 
concentrate their own units' firepower on a specific target of the enemy, aiming to swiftly weaken or eliminate crucial 
foes. Determining whether this micro is being executed typically involves observing the movement and attack behavior of 
the player's units. Players, when employing a concentrated attack, demonstrate a unified firepower output by selecting 
the same target and coordinating attacks, a behavior that can be assessed by monitoring the attack targets and frequency 
of the player's units. Additionally, the player's operating pattern serves as a basis for judgment, as concentrated 
attacks require purposeful coordination of unit attacks, manifesting in relatively uniform actions. Therefore, by 
considering these characteristics comprehensively, it is possible to relatively accurately assess whether a concentrated 
attack micro is being employed.
3. Scattered Attack Micromanagement: The characteristic of this technique is that players intentionally disperse their 
own units to diminish the effectiveness of the enemy's area-of-effect attacks. This strategy aids in minimizing the 
damage caused by enemy skills or attacks to multiple units. To determine whether the scattered attack micro is being 
executed, one can observe the distribution of the player's units. When employing this micro, players typically disperse 
their units to avoid concentrated firepower attacks. Additionally, by checking whether the player consciously adjusts 
unit positions to adapt to the enemy's area-of-effect attacks, one can also infer whether the scattered attack micro is 
in play. Therefore, by observing the unit distribution and operating pattern, it is possible to relatively accurately 
judge whether the player is employing a scattered attack strategy.
4. Alternate Attack Micromanagement: The characteristic of this technique is that players swiftly move their units after 
attacking to maximize the unit's effective output and reduce damage taken from the enemy. This strategy requires players 
not only to attack at the right moments but also to immediately reposition, thereby maximizing their survivability during 
movement. Judging whether alternate attack micro is being executed can be done by observing the unit's attack frequency 
and movement behavior. When employing this micro, players typically move their units quickly after each attack to adapt 
to the enemy's counterattacks. By monitoring this alternating pattern of attack and movement, it is possible to relatively 
accurately determine whether the player is employing an alternate attack strategy.
Based on the summary of multiple rounds in the game, including the position coordinate sequence and action sequence of 
our combat units, as well as the position coordinate sequence of the enemy combat units, we hope you 
can analyze it in a structured way game progress. Your analysis should include the following aspects:
1. Micromanagement usage: Do our combat units use the above four types of micromanagement? If used, please tell me the 
one with the highest probability.
    """


    example_input_prompt0 = r"""
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: [[[13.0, 10.875], [20.125, 12.0]], [[14.125, 10.875], [20.125, 10.875]], [[14.125, 10.875], [20.125, 12.0]], [[14.125, 9.75], [20.125, 10.875]], [[13.0, 9.75], [19.0, 10.875]]].
The coordinate position sequence of enemy combat units: [[[16.44, 17.96], [16.44, 17.96]], [[16.88, 16.93], [16.88, 16.9]], [[17.3, 15.9], [17.3, 15.9]], [[17.9, 14.95], [17.9, 14.95]], [[18.36, 13.9], [18.36, 13.9]]].
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: [['move', 'move'], ['move', 'move'], ['stop', 'move'], ['move', 'move'], ['move', 'move']].
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The basis for analysis: No micromanagement is used.
    """
    example_output_prompt0 = r"""
1. Micromanagement usage: No micromanagement is used.
    """


    example_input_prompt1 = r"""
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: [[[13.0, 10.875], [13, 10]], [[14.125, 10.875], [14, 10]], [[14.125, 10.875], [14, 10]], [[14.125, 9.75], [14, 10]], [[13.0, 9.75], [13, 10]]].
The coordinate position sequence of enemy combat units: [[[11.0, 10.875], [16.44, 17.96]], [[13.125, 10.875], [16.88, 16.9]], [[11.125, 10.875], [17.3, 15.9]], [[13.125, 9.75], [17.9, 14.95]], [[12.0, 9.75], [18.36, 13.9]]].
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: [['attack', 'attack'], ['move', 'move'], ['attack', 'attack'], ['move', 'move'], ['attack', 'attack']].
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The basis for analysis: When the distance is far, use long-range attack, and when the distance is too close, stay away from the enemy for pulling.
    """
    example_output_prompt1 = r"""
1. Micromanagement usage: Kiting Micromanagement is used.
    """


    example_input_prompt2 = r"""
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: [[[13.0, 10.875], [13, 10]], [[14.125, 10.875], [14, 10]], 
[[14.125, 10.875], [14, 10]], [[14.125, 9.75], [14, 10]], [[13.0, 9.75], [13, 10]]].
The coordinate position sequence of enemy combat units: [[[16.44, 17.96], [16.44, 17.96]], [[16.88, 16.93], 
[16.88, 16.9]], [[17.3, 15.9], [17.3, 15.9]], [[17.9, 14.95], [17.9, 14.95]], [[18.36, 13.9], [18.36, 13.9]]].
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time 
steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of 
each combat unit.
Action sequences of our combat units: [['attack123', 'attack123'], ['attack123', 'attack123'], 
['attack123', 'attack123'], ['attack123', 'attack123'], ['attack123', 'attack123']].
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the 
second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, 
stop and heal. The number spliced after attack represents the specific attack target number.
The basis for analysis: Our combat units are all attacking the same target.
    """
    example_output_prompt2 = r"""
1. Micromanagement usage: Concentrated Attack Micromanagement is used.
    """


    example_input_prompt3 = r"""
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: [[[16.44, 17.96], [36.44, 37.96]], [[16.88, 16.93], [36.88, 36.9]], [[17.3, 15.9], [37.3, 35.9]], [[17.9, 14.95], [37.9, 34.95]], [[18.36, 13.9], [38.36, 33.9]]].
The coordinate position sequence of enemy combat units: [[[16.44, 17.96], [16.44, 17.96]], [[16.88, 16.93], [16.88, 16.9]], [[17.3, 15.9], [17.3, 15.9]], [[17.9, 14.95], [17.9, 14.95]], [[18.36, 13.9], [18.36, 13.9]]].
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: [['move', 'move'], ['move', 'move'], ['stop', 'move'], ['move', 'move'], ['move', 'move']].
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The basis for analysis: Our combat units are dispersed and attacking separately.
    """
    example_output_prompt3 = r"""
1. Micromanagement usage: Scattered Attack Micromanagement is used.
    """

    example_input_prompt4 = r"""
The two sides fighting: our side is three Stalkers, the opponent is three Zealots.
Description: This section primarily records and summarizes our observations.
The coordinate position sequence of our combat units: [[[16.44, 17.96], [20.44, 18.96]], [[20.88, 16.93], [16.88, 16.9]], [[17.3, 15.9], [16.3, 18.9]], [[20.9, 14.95], [17.9, 15.95]], [[18.36, 15.9], [22.36, 12.9]]].
The coordinate position sequence of enemy combat units: [[[16.44, 17.96], [16.44, 17.96]], [[16.88, 16.93], [16.88, 16.9]], [[17.3, 15.9], [17.3, 15.9]], [[17.9, 14.95], [17.9, 14.95]], [[18.36, 13.9], [18.36, 13.9]]].
The coordinate position sequence is a three-dimensional vector. The first dimension represents the passage of time steps, the second dimension represents multiple combat units, and the third dimension represents the x,y coordinates of each combat unit.
Action sequences of our combat units: [['move', 'attack123'], ['attack123', 'move'], ['move', 'attack123'], ['attack123', 'move'], ['move', 'attack123']].
The action sequences is a two-dimensional vector. The first dimension represents the passage of time steps, and the second dimension represents the actions performed by each combat unit. There are four types of actions: attack, move, stop and heal. The number spliced after attack represents the specific attack target number.
The basis for analysis: Our combat units take turns attacking the same local unit.
    """
    example_output_prompt4 = r"""
1. Micromanagement usage: Alternate Attack Micromanagement is used.
    """

    example_input_prompt_list = [example_input_prompt0, example_input_prompt1, example_input_prompt2, example_input_prompt3, example_input_prompt4]
    example_output_prompt_list = [example_output_prompt0, example_output_prompt1, example_output_prompt2, example_output_prompt3, example_output_prompt4]

    return system_prompt, example_input_prompt_list, example_output_prompt_list



