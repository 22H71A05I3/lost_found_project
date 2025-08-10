# Flask routes to handle notification API endpoints: sending notifications, fetching user notifications, and marking them as read.
from flask import Blueprint, request, jsonify
from .models import Notification, SessionLocal

notifications_bp = Blueprint('notifications', __name__)

# Send a notification
@notifications_bp.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    session = SessionLocal()
    notif = Notification(
        user_id=data.get('user_id'),
        title=data.get('title'),
        message=data.get('message'),
        type=data.get('type', 'in-app')  # e.g., 'email' or 'in-app'
    )
    session.add(notif)
    session.commit()
    session.refresh(notif)
    session.close()
    return jsonify({'id': notif.id}), 201

# Fetch notifications for a user
@notifications_bp.route('/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')
    session = SessionLocal()
    query = session.query(Notification)
    if user_id:
        query = query.filter(Notification.user_id == int(user_id))
    notifications = query.order_by(Notification.timestamp.desc()).all()
    session.close()
    return jsonify([
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'timestamp': n.timestamp,
            'read': n.read,
            'type': n.type
        } for n in notifications
    ])

# Mark a notification as read
@notifications_bp.route('/notifications/<int:notif_id>/read', methods=['POST'])
def mark_notification_read(notif_id):
    session = SessionLocal()
    notif = session.query(Notification).get(notif_id)
    if not notif:
        session.close()
        return jsonify({'error': 'Notification not found'}), 404
    notif.read = True
    session.commit()
    session.close()
    return jsonify({'message': 'Notification marked as read'})