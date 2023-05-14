from app import socketio, openai
from flask import session
from flask_socketio import emit
from datetime import datetime
from openai import ChatCompletion


@socketio.on('message', namespace='/game')
def handle_message(data):
    """
    Handler function for message events. 
    First it gets the message that was sent by the client, and adds it to the list of session messages. 
    Then feeds the message history (session messages) to ChatGPT for a response.
    Then adds the response to the list of session messages. 
    Then broadcasts the response back to the client.
    """
    session['messages'].append({"timestamp": datetime.utcnow(), "role": "user", "content": data['message']})
    history = []
    for message in session['messages']:
        history.append({'role': message['role'], 'content': message['content']})
    completion = ChatCompletion.create(model="gpt-3.5-turbo", messages=history)
    reply = completion['choices'][0]['message']['content']
    session['messages'].append({"timestamp": datetime.utcnow(), "role": "assistant", "content": reply})
    emit('message', {'message': reply}, broadcast=True)