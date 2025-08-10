# Utility functions to validate report data, notify moderators, and automate report processing.

import re
import smtplib
from email.mime.text import MIMEText

def validate_report_data(data):
	"""Validate report data for required fields and basic format."""
	required = ['reporter_id', 'item_id', 'reason']
	for field in required:
		if field not in data or not data[field]:
			return False, f"Missing or empty field: {field}"
	# Example: check reason length
	if len(data['reason']) < 10:
		return False, "Reason must be at least 10 characters."
	# Example: check for inappropriate words
	banned = ['spam', 'abuse', 'scam']
	if any(word in data['reason'].lower() for word in banned):
		return False, "Reason contains inappropriate words."
	return True, "Valid"

def notify_moderators(report):
	"""Send notification to moderators (stub: prints, but can send email)."""
	# In production, send email or push notification
	print(f"Moderator notified: New report {report.id} for item {report.item_id}")
	# Example email notification (requires SMTP setup)
	# msg = MIMEText(f"New report: {report.reason}")
	# msg['Subject'] = "New Content Report"
	# msg['From'] = "noreply@lostfound.com"
	# msg['To'] = "moderator@lostfound.com"
	# with smtplib.SMTP('localhost') as server:
	#     server.sendmail(msg['From'], [msg['To']], msg.as_string())

def automate_report_processing(report):
	"""Automate report processing (stub: auto-resolve if reason contains 'test')."""
	if 'test' in report.reason.lower():
		report.status = 'resolved'
		print(f"Report {report.id} auto-resolved.")
		return True
	return False
