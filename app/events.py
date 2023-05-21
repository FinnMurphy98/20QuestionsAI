from app import socketio, db
from flask import session
from flask_socketio import emit
from datetime import datetime
from app.openai.chat import chatgpt_response
from app.models import Message
from flask_login import current_user

@socketio.on('message', namespace='/game/Answerer')
@socketio.on('message', namespace='/game/Questioner')
def message(data):
    """
    Handler function for message events. 
    First it gets the message that was sent by the client, and adds it to the list of session messages. 
    Then feeds the message history (session messages) to ChatGPT for a response.
    Then adds the response to the list of session messages. 
    Then broadcasts the response back to the client.
    """
    message = Message(timestamp=datetime.now(), game_id=session['game_id'], role='user', content=data['message'])
    db.session.add(message)
    db.session.commit()
    history = []
    for message in Message.query.filter_by(game_id=session['game_id']).all():
        history.append({'role': message.role, 'content': message.content})
    reply = chatgpt_response(history)
    message = Message(timestamp=datetime.now(), game_id=session['game_id'], role='assistant', content=reply)
    db.session.add(message)
    db.session.commit()
    emit('message', {'message': reply})