from app import socketio
from flask import session
from flask_socketio import emit
from datetime import datetime
from app.openai.chat import chatgpt_response

@socketio.on('connect', namespace='/game/Answerer')
def connect():
    print('Client connected')

@socketio.on('message', namespace='/game/Answerer')
def message(data):
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
    reply = chatgpt_response(history)
    session['messages'].append({"timestamp": datetime.utcnow(), "role": "assistant", "content": reply})
    emit('message', {'message': reply})