from openai import ChatCompletion

def chatgpt_response(messages):
    """
    Uses the ChatCompletion.create() function with ChatGPT 3.5 Turbo model. 
    Takes a list of messages and returns a response from the model. 
    """
    completion = ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response = completion['choices'][0]['message']['content']
    return response