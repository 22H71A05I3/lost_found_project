# Utility functions for notifications: sending emails, formatting messages, and scheduling alerts.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

def send_email(to_email, subject, html_content, from_email=None):
	"""Send an email notification."""
	msg = MIMEMultipart()
	msg['From'] = from_email or 'noreply@lostfound.com'
	msg['To'] = to_email
	msg['Subject'] = subject
	msg.attach(MIMEText(html_content, 'html'))
	try:
		with smtplib.SMTP('localhost') as server:
			server.sendmail(msg['From'], to_email, msg.as_string())
		return True
	except Exception as e:
		print(f"Email send failed: {e}")
		return False

def format_notification(title, message, timestamp=None):
	"""Format notification message for display or email."""
	if not timestamp:
		timestamp = datetime.datetime.utcnow()
	return {
		'title': title,
		'message': message,
		'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
	}

def schedule_alert(user_id, title, message, alert_time):
	"""Schedule an alert for a user at a specific time (stub)."""
	# This is a stub. In production, use a task queue like Celery or APScheduler.
	print(f"Scheduled alert for user {user_id} at {alert_time}: {title} - {message}")
	return True
