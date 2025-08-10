import re

def format_message(msg):
	"""Format a message for display."""
	return {
		'id': msg.id,
		'sender_id': msg.sender_id,
		'receiver_id': msg.receiver_id,
		'content': msg.content,
		'timestamp': msg.timestamp
	}

def is_spam(content):
	"""Basic spam check: returns True if message contains banned words or repeated characters."""
	banned_words = ['spam', 'buy now', 'free', 'click here']
	content_lower = content.lower()
	if any(word in content_lower for word in banned_words):
		return True
	if re.search(r'(.)\1{5,}', content):  # 6+ repeated chars
		return True
	return False

def sanitize_input(content):
	"""Sanitize input to prevent XSS and strip unwanted characters."""
	# Remove HTML tags
	content = re.sub(r'<.*?>', '', content)
	# Optionally, escape quotes
	content = content.replace('"', '').replace("'", '')
	return content.strip()
