# Flask routes to submit reports for inappropriate content, list reports for moderators, and resolve flags.

from flask import Blueprint, request, jsonify
from .models import Report, SessionLocal

reports_bp = Blueprint('reports', __name__)

# Submit a report
@reports_bp.route('/reports', methods=['POST'])
def submit_report():
	data = request.json
	session = SessionLocal()
	report = Report(
		reporter_id=data.get('reporter_id'),
		item_id=data.get('item_id'),
		reason=data.get('reason'),
		status='pending'
	)
	session.add(report)
	session.commit()
	session.refresh(report)
	session.close()
	return jsonify({'id': report.id}), 201

# List all reports (for moderators)
@reports_bp.route('/reports', methods=['GET'])
def list_reports():
	session = SessionLocal()
	reports = session.query(Report).order_by(Report.created_at.desc()).all()
	session.close()
	return jsonify([
		{
			'id': r.id,
			'reporter_id': r.reporter_id,
			'item_id': r.item_id,
			'reason': r.reason,
			'status': r.status,
			'created_at': r.created_at,
			'updated_at': r.updated_at
		} for r in reports
	])

# Resolve a report (moderator action)
@reports_bp.route('/reports/<int:report_id>/resolve', methods=['POST'])
def resolve_report(report_id):
	session = SessionLocal()
	report = session.query(Report).get(report_id)
	if not report:
		session.close()
		return jsonify({'error': 'Report not found'}), 404
	report.status = 'resolved'
	session.commit()
	session.close()
	return jsonify({'message': 'Report resolved'})
