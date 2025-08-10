from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
import qrcode

qr_routes_bp = Blueprint('qr_routes', __name__)

@qr_routes_bp.route('/generate_qr', methods=['POST'])
def generate_qr():
	data = request.json
	info_url = data.get('info_url')
	if not info_url:
		return jsonify({'error': 'Missing info_url'}), 400
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(info_url)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	buf = BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	# Return as image file
	return send_file(buf, mimetype='image/png')

@qr_routes_bp.route('/generate_qr_data_url', methods=['POST'])
def generate_qr_data_url():
	data = request.json
	info_url = data.get('info_url')
	if not info_url:
		return jsonify({'error': 'Missing info_url'}), 400
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(info_url)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")
	buf = BytesIO()
	img.save(buf, format='PNG')
	buf.seek(0)
	import base64
	data_url = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')
	return jsonify({'data_url': data_url})
