def get_tool_calls_and_args(response):
    if "tool_calls" in response["choices"][0]["message"]:
        tool_calls = response["choices"][0]["message"]["tool_calls"]

        for tool_call in tool_calls:
            args = json.loads(tool_call["function"]["arguments"])

            return tool_call, args


def structured_messages(response):
    user_messages = []

    for message in data['data']:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'text':
                    user_messages.append({"role": "user", "content": content['text']['value']})

    return user_messages
