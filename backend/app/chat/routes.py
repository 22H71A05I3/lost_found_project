from flask import Blueprint, request, jsonify
from .models import Message, SessionLocal

chat_bp = Blueprint('chat', __name__)

# Send a message
@chat_bp.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    session = SessionLocal()
    msg = Message(
        sender_id=data.get('sender_id'),
        receiver_id=data.get('receiver_id'),
        content=data.get('content')
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    session.close()
    return jsonify({'id': msg.id}), 201

# List messages for a user (sent or received)
@chat_bp.route('/messages', methods=['GET'])
def list_messages():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    start_date = request.args.get('start_date')  # ISO format string
    end_date = request.args.get('end_date')      # ISO format string
    order = request.args.get('order', 'desc')
    session = SessionLocal()
    query = session.query(Message)
    if sender_id:
        query = query.filter(Message.sender_id == int(sender_id))
    if receiver_id:
        query = query.filter(Message.receiver_id == int(receiver_id))
    if start_date:
        from datetime import datetime
        query = query.filter(Message.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        from datetime import datetime
        query = query.filter(Message.timestamp <= datetime.fromisoformat(end_date))
    if order == 'asc':
        query = query.order_by(Message.timestamp.asc())
    else:
        query = query.order_by(Message.timestamp.desc())
    messages = query.all()
    session.close()
    return jsonify([
        {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'content': msg.content,
            'timestamp': msg.timestamp
        } for msg in messages
    ])

# Retrieve a specific message
@chat_bp.route('/messages/<int:msg_id>', methods=['GET'])
def get_message(msg_id):
    session = SessionLocal()
    msg = session.query(Message).get(msg_id)
    session.close()
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify({
        'id': msg.id,
        'sender_id': msg.sender_id,
        'receiver_id': msg.receiver_id,
        'content': msg.content,
        'timestamp': msg.timestamp
    })
