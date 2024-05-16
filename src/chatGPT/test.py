from zhipuai import ZhipuAI
client = ZhipuAI(api_key="a3c183a89ea4824a5bfdb6a04b6a8f5d.ovvI1NlLpWhawuEH") # 填写您自己的APIKey
output = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "2018年nba冠军是谁"},
    ],
)
print(output.choices[0].message.content)